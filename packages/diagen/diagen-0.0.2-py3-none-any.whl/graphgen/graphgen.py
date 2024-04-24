import dataclasses
import itertools
import sys
from collections import defaultdict
from enum import Enum
import networkx as nx
from typing import Iterable, Union, Sequence, Hashable, Dict, Set, Optional

import pydot
import matplotlib.cm as cm
import matplotlib.colors

from .nxgraph import nest

FONTSTYLE = dict(fontsize=25)


class GV_numbered_item:
    __seq = itertools.count()

    def __init__(self):
        self._seq = next(self.__seq)

    @property
    def gv_name(self):
        return self.__class__.__name__ + "_" + str(self._seq)

    def __repr__(self):
        return f"<{self.gv_name}>"


class Link(pydot.Edge):
    _required = False

    def __init__(self, src: 'Component', dst: 'Component', bidir=True, required=False, **attrs):
        self.src = src
        self.dst = dst
        self.required = required
        dir_style = "none" if bidir else "forward"

        self.bidir = bidir
        assert isinstance(src, Component), "Links only allow Components as src"
        assert isinstance(dst, Component), "Links only allow Components as dst"
        #
        pydot.Edge.__init__(self, src, dst, dir=dir_style, **attrs)  # type: ignore

    @property
    def required(self):
        return self._required

    @required.setter
    def required(self, v):
        self._required = v
        self.src.required |= v
        self.dst.required |= v


class Nestable(GV_numbered_item):
    # Current depth of this block
    depth = 0
    # Extra depth to be applied when entering this nestable (increases LOD)
    _more_depth:int = 0
    # Whether depth is to be ignored and this thing to be always rendered
    _required = False

    _children: Dict[str, 'Nestable']
    _links: Set[Link]

    _parent:Optional['Nestable'] = None
    _shown = False

    def __init__(self, label: str = "", more_depth: int = 0):
        # do not call constructor of Graph as it will break things
        object.__setattr__(self, '_children', {})
        object.__setattr__(self, '_links', set())

        GV_numbered_item.__init__(self)
        self.label = label
        self._more_depth = more_depth

    @property
    def required(self):
        return self._required

    @required.setter
    def required(self, v):
        self._required = v

        if self.parent is not None:
            self.parent.required = v

    @property
    def parent(self) -> Optional['Nestable']:
        return self._parent

    def __setattr__(self, key, value):
        if isinstance(value, Nestable):
            if value._parent is None:
                self.add_child(key, value)

        object.__setattr__(self, key, value)

    def add_child(self, key: str, value: 'Nestable'):
        assert isinstance(value, Nestable)
        assert value._parent is None
        # bypass setattr
        object.__setattr__(value, '_parent', self)
        for v in value.subtree():
            v.depth += 1
        # value.depth = self.depth + 1
        self._children[key] = value

    def children(self):
        """Iterator over all children"""
        for c in self._children:
            yield c

    def subtree(self):
        for c in self._children.values():
            yield from c.subtree()
            yield c

    def link(self, src: 'Component', dst: 'Component', required=False, bidir=True, **attrs):
        self._links.add(Link(src, dst, required=required, bidir=bidir, **attrs))

    def update_graph(self, graph: pydot.Graph, maxdepth=100):

        maxdepth += self._more_depth
        if self.depth < maxdepth or self.required:
            self._shown = True
            # print(self.gv_name, self.depth, self.required)
            if isinstance(self, Component):
                # print(f"Add node {self} to {graph}")
                # print("objdict", graph.obj_dict)
                # print("objdict", self.obj_dict)

                graph.add_node(self)
            else:
                # print(f"Add SG {self} to {graph}")
                # print("objdict", graph.obj_dict)
                graph.add_subgraph(self)

                for c in self._children.values():
                    c.update_graph(graph=self, maxdepth=maxdepth)

            for e in self._links:
                if e.src._shown and e.dst._shown:
                    graph.add_edge(e)

    def build_networkx_graph(self) -> nx.DiGraph:
        G = nx.DiGraph()
        G.add_node(self.gv_name, label=self.label, object=self)
        # link connectivity graphs
        for c in self._children.values():
            G = nest(G, c.build_networkx_graph(), self.gv_name, c.gv_name, inplace=True)

        for lnk in self._links:
            assert lnk.src.gv_name in G.nodes, f"Source {lnk.src.label} not inside current block {self.label}"
            assert lnk.dst.gv_name in G.nodes, f"Destination {lnk.dst.label} not inside current block {self.label}"
            G.add_edge(lnk.src.gv_name, lnk.dst.gv_name, weight=1)
            if lnk.bidir:
                G.add_edge(lnk.dst.gv_name, lnk.src.gv_name, weight=1)
        return G


class Group(Nestable, pydot.Subgraph):
    """Group objects together but do not add any labels"""
    def __init__(self, **attrs):
        Nestable.__init__(self)
        pydot.Subgraph.__init__(self, graph_name=self.gv_name, **attrs)


class Block(Nestable, pydot.Cluster):
    """Named group of objects. Must have at least one component."""
    def __init__(self, label, more_depth: int = 0, **attrs):
        Nestable.__init__(self, label, more_depth)
        attrs.update(FONTSTYLE)
        pydot.Cluster.__init__(self, graph_name=self.gv_name, label=str(label), **attrs)


class Component(Nestable, pydot.Node):
    """Smallest unit of detail in the diagram"""
    def __init__(self, label: str, **attrs):
        Nestable.__init__(self, label)
        attrs.update(FONTSTYLE)
        attrs.setdefault("shape", "component")
        pydot.Node.__init__(self, name=self.gv_name, label=label, **attrs)



class Path(pydot.Subgraph):
    __idx = itertools.count()  # paths have their own numbering for the sake of colormapping

    def __init__(self, *hops: Nestable, color=None, cmap=cm.Set1, **attr):
        pydot.Subgraph.__init__(self)
        if color is None:
            cm_idx = next(self.__idx)
            color = cmap(cm_idx)
            color = matplotlib.colors.to_hex(color, keep_alpha=False)
            print(color)
        for s, d in itertools.pairwise(hops):
            s.required = True
            d.required = True
            self.add_edge(pydot.Edge(s, d, color=color, **attr))

    @classmethod
    def auto(cls, block: Block, src: Component, dst: Component, color=None, cmap=cm.Set1, **attr):
        G = block.build_networkx_graph()
        print("find shortest path in G", src.gv_name, dst.gv_name)
        path = nx.shortest_path(G, source=src.gv_name, target=dst.gv_name, weight='weight')
        print(path)
        hops = [G.nodes[h]['object'] for h in path]
        return cls(*hops, color=color, cmap=cmap, **attr)


class Graph:
    def __init__(self, name, layout="osage", nodesep=0.1):
        self.name = name
        self.layout = layout
        self.nodesep = nodesep
        self.splines = "ortho" if layout == "osage" else "spline"
        self.blocks = {}
        self.paths = []

    def __setattr__(self, key, value):
        if isinstance(value, Block):
            self.blocks[key] = value
        elif isinstance(value, Path):
            self.paths.append(value)
        object.__setattr__(self, key, value)

    def make_dot_file(self, maxdepth=100):
        graph = pydot.Dot('D', graph_type='digraph',
                          splines=self.splines,
                          rankdir="LR",
                          esep=0.5,
                          nodesep=self.nodesep,
                          overlap="vpsc",
                          compound=True,
                          layout=self.layout,
                          pack=50,
                          **FONTSTYLE,
                          concentrate=False,
                          )

        for name, block in self.blocks.items():
            block.update_graph(graph, maxdepth=maxdepth)

        for c in self.paths:
            graph.add_subgraph(c)

        graph.write_raw(f'{self.name}.dot') #type:ignore
        graph.write_png(f'{self.name}.png') #type:ignore


class PortBlock(Block, GV_numbered_item):
    KEY_TYPE = Union[int, str, Hashable]

    def __init__(self, label: str = "Ports", port_idents: Union[Sequence[KEY_TYPE], Dict[KEY_TYPE, str]] = range(4),
                 port_fstring="{p}", align="c", port_type=None, **attrs):
        self.port_type = port_type
        attrs.update(FONTSTYLE)
        Block.__init__(self, label, packmode=f"array_{align}u{len(port_idents)}", pack=5, **attrs)

        if isinstance(port_idents, dict):
            port_labels = [str(port_idents[k]) for k in port_idents]
        else:
            port_labels = [port_fstring.format(p=i) for i in port_idents]

        self.ports = {}
        for num, (ident, label) in enumerate(zip(port_idents, port_labels), start=1):
            n = Component(bgcolor="#ffff00", label=label,
                          shape="box", group=f"{self.gv_name}", sortv=num)
            self.ports[ident] = n
            self.add_child(f"port_{num}", n)

    def __getitem__(self, item):
        try:
            return self.ports[item]
        except KeyError:
            print(f"Tried accessing port {item} on {self.label}, available ports are {list(self.ports.keys())} ")
            raise
