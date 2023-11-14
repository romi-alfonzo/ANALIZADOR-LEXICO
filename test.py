import networkx as nx
import matplotlib.pyplot as plt

# Crear un grafo dirigido para representar el AFN
G = nx.DiGraph()

# Agregar estados y transiciones
G.add_node("q0", initial=True)
G.add_node("qf", final=True)
G.add_edge("q0", "qf", label="a")
G.add_edge("q0", "q0", label="b")
G.add_edge("q0", "q0", label="d")
G.add_edge("q0", "q0", label="bda")
G.add_edge("q0", "q0", label="c")
G.add_edge("q0", "q0", label="baAc")
G.add_edge("q0", "q0", label="da")

# Dibuja el grafo
pos = nx.spring_layout(G, seed=7)
labels = {edge: G.edges[edge]["label"] for edge in G.edges}
nx.draw(G, pos, with_labels=True, node_size=500, node_color="lightblue", font_size=10)
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
plt.show()
