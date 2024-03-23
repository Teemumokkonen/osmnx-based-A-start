import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import math
import random

place_name = "Hervanta, Tampere, Finland"

def a_star(graph, source, target):
    open_list = [(0, source)]  # Priority queue with (f, node)
    closed_set = set()
    came_from = {}
    g_score = {node: float('inf') for node in graph.nodes()}
    g_score[source] = 0

    while open_list:
        _, current = min(open_list)
        open_list.remove((_, current))
        
        if current == target:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(source)
            return path[::-1]

        closed_set.add(current)

        for neighbor in graph.neighbors(current):
            if neighbor in closed_set:
                continue
            
            tentative_g_score = g_score[current] + graph[current][neighbor][0]['length']
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score = tentative_g_score
                open_list.append((f_score, neighbor))

    return None  # No path found

def main():
    graph = ox.graph_from_place(place_name, network_type="drive")
    source = random.choice(list(graph.nodes()))
    target = random.choice(list(graph.nodes()))
    
    shortest_path = a_star(graph, source, target)
    print("Shortest path:", shortest_path)
    nodes, _ = ox.graph_to_gdfs(graph)
    node_positions = {node: (data['x'], data['y']) for node, data in nodes.iterrows()}
    
    # Plot the graph and the shortest path
    fig, ax = ox.plot_graph(graph, show=False, close=False)
    node_colors = ['r' if node in shortest_path else 'b' for node in graph.nodes()]
    nx.draw_networkx_nodes(graph, pos=node_positions, ax=ax, node_color=node_colors)
    nx.draw_networkx_edges(graph, pos=node_positions, ax=ax)
    plt.show()

if __name__ == "__main__":
    main()
