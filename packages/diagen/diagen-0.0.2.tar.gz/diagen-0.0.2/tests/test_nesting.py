from graphgen import Component, Graph, Path, Block
from graphgen.graphgen import Group



class InnerThingie(Block):
    def __init__(self, label, more_depth: int = 0, **attrs):
        super().__init__(label, more_depth, **attrs)
        self.foo= Component("foo")
        self.bar= Component("bar")

class Thingie(Block):
    def __init__(self, label,  more_depth: int = 0, **attr):
        Block.__init__(self, label,  **attr)
        self.inner_thingie = InnerThingie(label="Depth 2")
        self.foo= Component("foo")
        self.link(self.foo, self.inner_thingie.foo)
        self.link(self.foo, self.inner_thingie.bar)


def test_depth():
    G = Graph("test_depth")
    T = Thingie("Depth 1")
    G.t = T

    G.make_dot_file(maxdepth=1)

def test_autorouting():
    G = Graph("test_autorouting")
    grp = Block("Things")
    G.grp = grp
    T1 = Thingie("Thingie 1")
    G.grp.t1 = T1
    T2 = Thingie("Thingie 2")
    G.grp.t2 = T2
    grp.link(T1.foo, T2.foo)

    p = Path.auto(grp, T1.inner_thingie.foo,  T2.inner_thingie.bar ,
                  color="#30DD00", penwidth=4, )
    G.paths.append(p)
    #G.make_dot_file(maxdepth=1)
    G.make_dot_file()

