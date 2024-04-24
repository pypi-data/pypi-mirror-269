import networkx as nx


def nest(Ghost: nx.DiGraph, Gchild: nx.DiGraph, n1, n2, weight=100, inplace=False) -> nx.DiGraph:
    G = Ghost if inplace else Ghost.copy()
    G.add_nodes_from(Gchild.nodes(data=True))
    G.add_weighted_edges_from(Gchild.edges(data='weight'))
    G.add_edge(n1, n2, weight=weight)
    G.add_edge(n2, n1, weight=weight)
    return G


def plot_graph(G):
    import matplotlib.pyplot as plt
    plt.figure()
    nx.draw_networkx(G)
    plt.show()


def test_nesting():
    G1 = nx.DiGraph()
    G1.add_node("root1")
    G1.add_node(1)
    G1.add_node(2)
    G1.add_edge("root1", 1)
    G1.add_edge("root1", 2)

    G2 = nx.DiGraph()
    G2.add_node("root2")
    G2.add_node(3)
    G2.add_node(4)
    G2.add_edge("root2", 3)
    G2.add_edge(3, "root2")
    G2.add_edge("root2", 4)
    G2.add_edge(4, "root2")
    G3 = nest(G1, G2, "root1", "root2")

    plot_graph(G3)
