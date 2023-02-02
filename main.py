import networkx as nx
import matplotlib.pyplot as plt
import random

# This code generates a random graph with n vertices and m edges. The edge weights are assigned random values between
# 5 and 10. The graph is represented graphically using NetworkX and Matplotlib libraries. The edge weights are also
# displayed next to the edges.

n = 7  # number of vertices
m = 12  # number of edges

if m > (n * (n - 1)) // 2:
    print("Number of edges is not possible for a simple undirected graph.")

G = nx.Graph()
G.add_nodes_from(range(n))

# Generate edges
edges = []
for i in range(m):
    u = random.randint(0, n - 1)
    v = random.randint(0, n - 1)
    if u != v and (u, v) not in edges and (v, u) not in edges:
        edges.append((u, v))
        G.add_edge(u, v, weight=random.uniform(5, 10))

colors = ['red', 'green', 'blue', 'yellow', 'black'] * (len(G.nodes) // 3 + 1)
color_count = 3

# color_map = []
# i = 0
# for node in G:
#     if i == color_count:
#         i = 0
#     print(colors[i])
#     # if node % 2 == 0:
#     color_map.append(colors[i])
#     i = i + 1
# print(color_map)

# Graph representation
pos = nx.spring_layout(G)
nx.draw(G, pos, node_colors=colors[:len(G.nodes)], with_labels=True)

# Show edge weights
# labels = nx.get_edge_attributes(G, 'weight')
# nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

plt.show()
