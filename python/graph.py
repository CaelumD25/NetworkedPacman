import math

import networkx as nx
import matplotlib.pyplot as plt


def create_graph(maze) -> nx.Graph:
    # documentation for this https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.shortest_paths.astar.astar_path.html

    # Each node has 3 properties: tile_id, row, and col. I beleive each node can also be referenced using by (row,col)
    # tile_ID:
    #    0 = free space
    #    1 = Wall
    #    2 = pellet

    G = nx.Graph()

    # Iterate through the maze to add nodes
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            G.add_node((row, col), tile_id=maze[row][col], row=row, col=col)  # Add the cell as a node

            # add neigherbour edges
            for d_row, d_col in [(-1, 0), (0, -1), (1, 0), (0, 1)]:  # Up, Left, Down, Right
                neighbor_row, neighbor_col = row + d_row, col + d_col
                if (0 <= neighbor_row < len(maze) and  # Row in bounds
                        0 <= neighbor_col < len(maze[0])):  # Col in bounds

                    # This part will create the adjacent node if it has not been created but properties will
                    # not get added/updated till add_node is called for adjecent node
                    G.add_edge((row, col), (neighbor_row, neighbor_col))
    return G


def create_minimalized_graph(maze: list):
    G = create_graph(maze)
    tmp_G = G.copy()
    for node in G.nodes(data=True):
        if node[1]["tile_id"] == 1:
            tmp_G.remove_node(node[0])
    return tmp_G


def convert_to_directions(node_initial, node_final) -> str:
    initial_x, intialx = node_initial
    final_x, final_y = node_final
    if intialx < final_y and initial_x == final_x:
        return "Left"
    elif intialx > final_y and initial_x == final_x:
        return "Right"
    elif intialx == final_y and initial_x < final_x:
        return "Up"
    elif intialx == final_y and initial_x > final_x:
        return "Down"
    else:
        return "None"


def get_node_given_coordinates(G: nx.Graph, coordinates):
    x, y = coordinates
    for i in G.nodes(data=True):
        if i[1]["row"] == y and i[1]["col"] == x:
            return i[0]


def a_star_directions(graph: nx.Graph, pacman_node, ghost_node):
    ghost_node = get_node_given_coordinates(graph, ghost_node)
    pacman_node = get_node_given_coordinates(graph, pacman_node)
    results = nx.astar_path(graph, pacman_node, ghost_node, a_star_heuristic)
    directions = []
    for node in range(len(results) - 1):
        print(f"Cur Node : {results[node]}, next node {results[node + 1]}")
        direction = convert_to_directions(results[node], results[node + 1])
        print("Direction", direction)
        directions.append(direction)
    return directions[::-1]


def a_star_heuristic(start_node, target_node) -> float:
    # Using Euclidean distance
    initial_x, initial_y = start_node
    final_x, final_y = target_node
    return math.sqrt((initial_x - final_x) ** 2 + (initial_y - final_y) ** 2)


def print_graph(G):
    print("Nodes:", list(G.nodes(data=True)))
    print("Edges:", list(G.edges()))


def show_graph(G):
    plt.figure(figsize=(20, 8))

    pos = {(row, col): (col, -row) for row, col in
           G.nodes()}  # Position nodes based on their (row, col) to preserve shape
    values = [G.nodes[node]['tile_id'] for node in G.nodes()]  # Get values for coloring

    # Prepare a color map, black for 0's (Free space), blue for 1's (wall), and yellow for 2's (pellet)
    color_map = []
    for node in G.nodes(data=True):
        if node[1]['tile_id'] == 0:  # Empty spot
            color_map.append('grey')
        elif node[1]['tile_id'] == 1:  # Wall
            color_map.append('pink')
        else:  # pellet
            color_map.append('yellow')

    nx.draw(G, pos, with_labels=True, node_color=color_map, cmap=plt.cm.Wistia, node_size=350, font_size=5)
    plt.show()


def main():
    maze = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
        [1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1],
        [1, 2, 1, 0, 0, 1, 2, 1, 0, 0, 0, 1, 2, 1, 1, 2, 1, 0, 0, 0, 1, 2, 1, 0, 0, 1, 2, 1],
        [1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1],
        [1, 2, 2, 2, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
        [1, 2, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 1],
        [1, 2, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 1],
        [1, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 1],
        [1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 2, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 2, 1, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 1, 2, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 2, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1],
        [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
        [1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1],
        [1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1],
        [1, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 1],
        [1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1],
        [1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1],
        [1, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 1],
        [1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1],
        [1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1],
        [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]

    G = create_graph(maze)
    print_graph(G)
    show_graph(G)


def find_pellet_locations(G):
    pellets = [node for node, data in G.nodes(data=True) if data['tile_id'] == 2]
    return pellets


# This function simulates a greedy choice by Pacman to move towards the nearest pellet.
# It assumes `G` is a graph representation of the maze, `pacman_location` is a tuple of Pacman's coordinates,
# and `pellets` is a list of tuples representing the coordinates of all pellets.
def find_nearest_pellet_path_greedy(G, pacman_location, pellets) -> list:
    # Find the nearest pellet by the shortest path length
    nearest_pellet, shortest_path = None, None
    pacman_location = get_node_given_coordinates(G, pacman_location)
    k = 20
    best_paths = []
    for pellet in pellets:
        try:
            path = nx.shortest_path(G, source=pacman_location, target=pellet, method='bellman-ford')
            best_paths = maintain_k_list(best_paths, path, k)
        except nx.NetworkXNoPath:
            # If there's no path to this pellet, skip it
            continue

    return best_paths


def greedy_algorithm(G: nx.Graph, pacman_location, ghost_location):
    pellets = find_pellet_locations(G)

    paths_to_nearest_pellets = find_nearest_pellet_path_greedy(G, pacman_location, pellets)
    # Assert to check paths
    assert (len(paths_to_nearest_pellets) <= 20)

    candidates = []
    for path in paths_to_nearest_pellets:
        pellet_node = path[-1]
        ghost_node = get_node_given_coordinates(G, ghost_location)
        cur_manhattan_distance = math.fabs(ghost_node[0] - pellet_node[0]) + math.fabs(ghost_node[1] - pellet_node[1])
        path_len = len(path)
        candidates.append([path, path_len, cur_manhattan_distance])
    #TODO Decision

    ghost_weight = 27
    path_len_weight = 1
    best_weight = float("inf")
    best_path = []
    for path in candidates:
        if path[2] == 0:
            weight = float("inf")
        else:
            weight = ((1/path[2]) * ghost_weight)
        if weight < best_weight:
            best_path = path[0]

    directions = []
    for node in range(len(best_path) - 1):
        direction = convert_to_directions(best_path[node+1], best_path[node])
        directions.append(direction)
    # TODO Check the direction
    return directions


def maintain_k_list(ls: list, new_entry: list, k: int) -> list:
    ls.append(new_entry)
    ls = sorted(ls, key=len)
    return ls[0:k]


if __name__ == "__main__":
    main()
