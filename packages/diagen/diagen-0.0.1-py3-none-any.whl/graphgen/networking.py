import pydot

from graphgen import Block, Component
from graphgen.graphgen import PortBlock




class Switch(Block):
    def __init__(self, label, num_ports=6, port_fstring="eth{p}"):
        Block.__init__(self, label, nodesep="0.01")

        self.fabric = Component("Fabric", shape="hexagon")

        idents = list(range(num_ports))
        self.ports = PortBlock(port_idents=idents, port_fstring=port_fstring)
