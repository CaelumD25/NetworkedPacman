from time import sleep

import requests

from python import graph

moves = 0

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


def main():
    base_url = "http://127.0.0.1:5000"
    game_state = get_game_state(base_url)

    maze = game_state["tiles"]
    pacman_location = (game_state["pacman_location"]["x"], game_state["pacman_location"]["y"])
    ghost_location = (game_state["ghost_location"]["x"], game_state["ghost_location"]["y"])

    while pacman_location != ghost_location:
        game_state = get_game_state(base_url)
        maze = game_state["tiles"]
        pacman_location = (game_state["pacman_location"]["x"], game_state["pacman_location"]["y"])
        ghost_location = (game_state["ghost_location"]["x"], game_state["ghost_location"]["y"])
        G = graph.create_minimalized_graph(maze)
        sleep(0.5)
        pacman_path = graph.greedy_algorithm(G, pacman_location, ghost_location)
        ghost_path = graph.a_star_directions(G, pacman_location, ghost_location)

        move_players(pacman_path[0],ghost_path[0], base_url)


if __name__ == "__main__":
    main()
