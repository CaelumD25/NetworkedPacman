from time import sleep

import requests
import unittest
import python.graph as graph

# Helper function to move the players given a direction, handles timeouts
def move_players(pacman_dir, ghost_dir, base_url):
    data = {"pacman": {"dir": pacman_dir}, "ghost": {"dir": ghost_dir}}
    response = None
    sent = False
    tries = 0
    while not sent and tries < 100:
        response = requests.post(f"{base_url}/players", json=data)
        sent = response.status_code == 200
        tries += 1
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



if __name__ == "__main__":
    unittest.main()

