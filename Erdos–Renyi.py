import itertools
import logging
import random

import matplotlib.pyplot as plt
import networkx as nx

import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)


def generate_graph(nodes, edges):
    if nodes < 5 or nodes > 10:
        raise ValueError("Broj cvorova treba da bude izmedju 5 i 10!")

    # The maximum number of edges a graph can have depends on the number of nodes in the graph.
    # For an undirected graph with n nodes,
    # there can be at most n(n-1) / 2 edges.This is the maximum number of edges for a complete graph,
    # where every node is connected to every other node.
    if (nodes * (nodes - 1)) / 2 < edges:
        raise ValueError('Broj ivica je preveliki za zadati broj cvorova!')

    # Generate a random graph with n nodes and m edges
    graph = nx.gnm_random_graph(nodes, edges)

    # Assign random weights to edges
    for u, v in graph.edges():
        graph[u][v]['weight'] = round(random.uniform(5, 10), 4)

    return graph


# First, assign colors to the nodes in a cyclic manner, such that no two adjacent nodes have the same color.

# Next, you can use a greedy algorithm to re-color the nodes if there are any conflicts. The algorithm starts from the
# first node and checks if its color is the same as any of its neighbors. If it is, it changes the color to the next
# available color in the list of colors. The algorithm continues until there are no more conflicts.
# def color_nodes(Graph, colors_input):
#     # Assign colors to nodes in a cyclic manner
#     node_colors = {node: color for node, color in zip(Graph.nodes(), colors_input * (len(Graph.nodes()) // len(colors_input) + 1))}
#
#     # Use a greedy algorithm to resolve conflicts
#     for node in Graph.nodes():
#         neighbors = [n for n in G.neighbors(node)]
#         for neighbor in neighbors:
#             if node_colors[node] == node_colors[neighbor]:
#                 color_index = colors_input.index(node_colors[node]) + 1
#                 node_colors[node] = colors_input[color_index % len(colors_input)]
#
#     # Draw the graph with nodes colored
#     nx.draw(Graph, node_color=[node_colors[node] for node in G.nodes()])
#     plt.show()

def skip_combination(combination, colors_input):
    color_list_temp = colors_input.copy()
    for item in combination:
        if color_list_temp.__contains__(item):
            color_list_temp.remove(item)
    return len(color_list_temp) > 0


def color_graph(Graph, colors_input):
    n_nodes = len(Graph.nodes())
    # boje * cvorovi
    color_combinations = list(itertools.product(colors_input, repeat=n_nodes))
    print("Kombinacije boja: " + color_combinations.__len__().__str__())

    for combination in color_combinations:
        if skip_combination(combination, colors_input):
            continue

        valid = True
        for node in Graph.nodes():
            node_color = combination[node]
            neighbors = [n_nodes for n_nodes in Graph.neighbors(node)]
            for neighbor in neighbors:
                if combination[neighbor] == node_color:
                    valid = False
                    break
            if not valid:
                break

        if valid:
            return combination
    raise ValueError("Ne postoji kombinacija boja za dato n i m, gde su sve boje ukljucene u kombinaciju!")


# Note that the code finds the pair of nodes with the largest distance in terms of number of edges
# (i.e., shortest path length), but not necessarily the pair of nodes with the largest Euclidean distance
# if the graph is embedded in a 2D or 3D space.
def furthest_red_nodes(Graph, red_nodes):
    max_distance = 0
    node1, node2 = -1, -1
    for node in red_nodes:
        # uzimamo sve distance od trenutnog crvenog cvora do svih ostalih cvorova
        distances = nx.single_source_shortest_path_length(Graph, node)
        for other_node, distance in distances.items():
            # filtriramo da distance od trenutnog cvora budu u odnosu na crveni cvor
            # i da distanca od jednog do drugog bude veca od trenutne najvece distance
            if other_node in red_nodes and (
                    distance > max_distance or (distance == max_distance and other_node > node2)):
                max_distance = distance
                node1, node2 = node, other_node
    print(
        "Najveca distanca izmedju crvenih cvorova po broju grana izmedju njih: |N(" + node1.__str__() + ") - N(" + node2.__str__() + ")| = " + max_distance.__str__())
    return node1, node2, max_distance


def furthest_red_nodes_weights(Graph, red_nodes):
    max_distance = 0
    node1, node2 = -1, -1
    for node in red_nodes:
        # uzimamo sve distance od trenutnog crvenog cvora do svih ostalih cvorova
        distances = nx.single_source_dijkstra_path_length(Graph, node)
        print("Dijkstra's(", node, "): ", distances)
        for other_node, distance in distances.items():
            # filtriramo da distance od trenutnog cvora budu u odnosu na crveni cvor
            # i da distanca od jednog do drugog bude veca od trenutne najvece distance
            if other_node in red_nodes and (
                    distance > max_distance or (distance == max_distance and other_node > node2)):
                max_distance = distance
                node1, node2 = node, other_node
    print(
        "Najveca distanca izmedju crvenih cvorova po dijkstrinom algoritmu: |N(" + node1.__str__() + ") - N(" + node2.__str__() + ")| = " + max_distance.__str__())
    return node1, node2, max_distance


def color_nodes(color_input):
    color_arr = []
    for i in range(color_input.__len__()):
        color_arr.append(color_input[i])
    return color_arr


def main():
    n = 7
    m = 12
    try:
        G = generate_graph(n, m)

        # TODO problem n=7, m=12, RGB
        # colors = ['red', 'green', 'blue']
        colors = ['red', 'green', 'blue', 'yellow']
        # colors = ['red', 'green', 'blue', 'yellow', 'black']

        coloring = color_graph(G, colors)
        coloring = color_nodes(coloring)
        colormap = [coloring[i] for i in range(len(G.nodes))]
        pos = nx.spring_layout(G)
        nx.draw(G, pos, node_color=colormap, with_labels=True)
        nx.set_node_attributes(G, {node: coloring[node] for node in G.nodes()}, 'color')

        # Show edge weights
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

        plt.show()

        red_nodes = [node for node in G.nodes if colormap[node] == 'red']
        red_node_count = len(red_nodes)

        if red_node_count <= 1:
            logging.getLogger("KTG-LOGGER").error("Ne postoji dovoljno crvenih cvorova da bi se racunala distanca!")
            return

        red_nodes = [node for node in G.nodes() if G.nodes[node].get('color') == 'red']
        furthest_red_nodes(G, red_nodes)
        furthest_red_nodes_weights(G, red_nodes)

    except ValueError as e:
        logging.getLogger("KTG-LOGGER").error("Erorr: " + e.__str__())


main()

# In this code, we first generate a random graph using the nx.gnm_random_graph function. The function takes two
# arguments: n, the number of nodes, and m, the number of edges.
# Next, we assign random weights to each edge using the random.uniform function. The weights are positive and between
# 5 and 10.
# We then check if the number of edges is appropriate for the number of nodes. If the number of edges is too large,
# we raise a ValueError.
# Finally, we define a color_nodes function to color the nodes in the graph. The function takes two arguments: the
# graph G and a list of colors colors. We create a dictionary node_colors to map each node to its color, and then use
# the nx.draw function to draw the graph with nodes colored. The node_color argument is set to a list of color values
# for each node in the graph.
# We call the color_nodes function with 3, 4, and 5 different colors to try different colorings of the graph. The
# resulting graphs are displayed using the plt.show function.
#
# No, in an undirected graph, not all edges have to be connected. An undirected graph can have disconnected edges,
# meaning that there are nodes in the graph that are not reachable from every other node in the graph.
#
# A disconnected graph can be represented by multiple connected components, where each component is a subgraph that
# is connected and contains one or more nodes. In such a graph, there can be edges that connect nodes within the same
# component but not between different components.
