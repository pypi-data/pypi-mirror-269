from graphgen import Graph, Path, PortBlock, Component
from graphgen.graphgen import GV_numbered_item
from graphgen.networking import *






def test_switches():
    G = Graph("switches")
    G.A = Switch("sw A")
    G.B = Switch("sw B")
    G.C = Switch("sw C")
    G.D = Switch("sw D")
    G.c1 = Path(G.A.ports[1], G.B.ports[3], G.B.fabric, G.B.ports[5], G.C.ports[2])
    G.c2 = Path(G.C.ports[1], G.B.ports[1], G.B.fabric, G.B.ports[2], G.C.ports[3])
    G.c3 = Path(G.C.ports[1], G.B.ports[3], G.B.fabric, G.B.ports[5], G.C.ports[2])
    G.c4 = Path(G.D.ports[0], G.D.fabric, G.D.ports[4])
    G.make_dot_file()
