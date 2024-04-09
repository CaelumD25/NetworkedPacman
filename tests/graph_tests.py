from time import sleep

import requests
import unittest
import python.graph as graph

moves = 0


# Helper function to move the players given a direction, handles timeouts
def move_players(pacman_dir, ghost_dir, base_url):
    global moves
    data = {"pacman": {"dir": pacman_dir}, "ghost": {"dir": ghost_dir}}
    response = None
    sent = False
    tries = 0
    sleep(0.1)
    while not sent:
        if moves == 0:
            moves += 1
            while not sent and tries < 100:
                response = requests.post(f"{base_url}/players", json=data)
                sent = response.status_code == 200
                tries += 1
    moves -= 1

    return response


# Helper function to get the game state, handles timeouts
def get_game_state(base_url):
    response = None
    success = False
    tries = 0
    # This has to wait, feel free to ask me about it, but there's a race condition I don't think we can solve
    sleep(0.2)
    while not success and tries < 100:
        response = requests.get(f"{base_url}/game_state")
        success = response.status_code == 200
        tries += 1
    return response.json()


class TestServer(unittest.TestCase):
    base_url = "http://127.0.0.1:5000"

    # Test Generating the Graph from the Game, manual exploratory test
    def test_generate_graph(self):
        maze = get_game_state(self.base_url)["tiles"]
        G = graph.create_graph(maze)
        graph.print_graph(G)
        graph.show_graph(G)
        self.assertEqual(1, 1)

    def test_minimal_graph(self):
        maze = get_game_state(self.base_url)["tiles"]
        G = graph.create_minimalized_graph(maze)
        graph.print_graph(G)
        graph.show_graph(G)
        self.assertEqual(1, 1)

    def test_navigate_to_pacman(self):
        game_state = get_game_state(self.base_url)

        maze = game_state["tiles"]
        pacman_location = (game_state["pacman_location"]["x"], game_state["pacman_location"]["y"])
        ghost_location = (game_state["ghost_location"]["x"], game_state["ghost_location"]["y"])

        distance = 99
        while distance > 1:
            G = graph.create_minimalized_graph(maze)
            results = graph.a_star_directions(G, pacman_location, ghost_location)

            move_players("None", results[0], self.base_url)
            game_state = get_game_state(self.base_url)
            maze = game_state["tiles"]
            pacman_location = (game_state["pacman_location"]["x"], game_state["pacman_location"]["y"])
            ghost_location = (game_state["ghost_location"]["x"], game_state["ghost_location"]["y"])
            distance = len(results)

        pacman_location = (game_state["pacman_location"]["x"], game_state["pacman_location"]["y"])
        ghost_location = (game_state["ghost_location"]["x"], game_state["ghost_location"]["y"])

        graph.print_graph(G)
        self.assertEqual(pacman_location, ghost_location)

    def test_pacman_greedy_vs_ghost_a_star(self):
        game_state = get_game_state(self.base_url)

        maze = game_state["tiles"]
        pacman_location = (game_state["pacman_location"]["x"], game_state["pacman_location"]["y"])
        ghost_location = (game_state["ghost_location"]["x"], game_state["ghost_location"]["y"])
        pellets = []

        distance = 99
        while distance > 1:
            G = graph.create_minimalized_graph(maze)
            results = graph.a_star_directions(G, pacman_location, ghost_location)

            # Determine Pacman's move based on the greedy algorithm
            pellets = graph.find_pellet_locations(G)

            path_to_nearest_pellet = graph.find_nearest_pellet_path_greedy(G, pacman_location, pellets)
            if path_to_nearest_pellet and len(path_to_nearest_pellet) > 1:
                # Determine the direction based on the first step towards the pellet
                pacman_next_step = path_to_nearest_pellet[1]
                pacman_dir = graph.convert_to_directions(pacman_location,
                                                         pacman_next_step)  # Implement this function to determine direction
            else:
                pacman_dir = "None"
            move_players(pacman_dir, results[0], self.base_url)
            game_state = get_game_state(self.base_url)
            maze = game_state["tiles"]
            pacman_location = (game_state["pacman_location"]["x"], game_state["pacman_location"]["y"])
            ghost_location = (game_state["ghost_location"]["x"], game_state["ghost_location"]["y"])
            distance = len(results)

        pacman_location = (game_state["pacman_location"]["x"], game_state["pacman_location"]["y"])
        ghost_location = (game_state["ghost_location"]["x"], game_state["ghost_location"]["y"])

        graph.print_graph(G)
        self.assertEqual(pacman_location, ghost_location)

    def test_pacman_navigate(self):
        game_state = get_game_state(self.base_url)


        maze = game_state["tiles"]
        pacman_location = (game_state["pacman_location"]["x"], game_state["pacman_location"]["y"])
        ghost_location = (game_state["ghost_location"]["x"], game_state["ghost_location"]["y"])
        pellets = []

        distance = 99
        while distance > 1:
            G = graph.create_minimalized_graph(maze)

            # Determine Pacman's move based on the greedy algorithm
            pellets = graph.find_pellet_locations(G)

            path_to_nearest_pellet = graph.find_nearest_pellet_path_greedy(G, pacman_location, pellets)

            dirs = []
            print(path_to_nearest_pellet)
            for i in range(len(path_to_nearest_pellet) - 1):
                dirs.append(graph.convert_to_directions(path_to_nearest_pellet[i + 1], path_to_nearest_pellet[i]))
            print(dirs)
            for x in dirs:
                sleep(0.1)
                move_players(x, "None", self.base_url)
                game_state = get_game_state(self.base_url)
            pacman_location = (game_state["pacman_location"]["x"], game_state["pacman_location"]["y"])
            maze = game_state["tiles"]
            ghost_location = (game_state["ghost_location"]["x"], game_state["ghost_location"]["y"])

        graph.print_graph(G)
        self.assertEqual(1, 1)

    def test_greedy_algo(self):
        game_state = get_game_state(self.base_url)

        maze = game_state["tiles"]
        pacman_location = (game_state["pacman_location"]["x"], game_state["pacman_location"]["y"])
        ghost_location = (game_state["ghost_location"]["x"], game_state["ghost_location"]["y"])

        while game_state["score"] < 9999:
            G = graph.create_minimalized_graph(maze)
            path = graph.greedy_algorithm(G, pacman_location, ghost_location)
            print("Path:", path)
            for dir in path:
                sleep(0.5)
                print("Direction: ", dir)
                move_players(dir, "None", self.base_url)
            game_state = get_game_state(self.base_url)

            maze = game_state["tiles"]
            pacman_location = (game_state["pacman_location"]["x"], game_state["pacman_location"]["y"])
            ghost_location = (game_state["ghost_location"]["x"], game_state["ghost_location"]["y"])


if __name__ == "__main__":
    unittest.main()

# use any search algo to get the closest pellet
# run BFS
