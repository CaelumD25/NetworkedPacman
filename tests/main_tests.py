from time import sleep

import requests
import unittest
from random import randint


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

    def test_get_state(self):
        response = requests.get(f"{self.base_url}/game_state")
        print(response.text)
        self.assertEqual(200, response.status_code)
        # Add more assertions as needed

    # def test_random_post_request(self):
    #     dir1 = ["Right", "Up", "Left", "Down"][randint(0, 3)]
    #     dir2 = ["Right", "Up", "Left", "Down"][randint(0, 3)]
    #     response = move_players(dir1, dir2, self.base_url)
    #     self.assertEqual(200, response.status_code)
    #     # Add more assertions as needed

    # def test_100_random_post_requests(self):
    #     for x in range(100):
    #         dir1 = ["Right", "Up", "Left", "Down"][randint(0, 3)]
    #         dir2 = ["Right", "Up", "Left", "Down"][randint(0, 3)]
    #         response = move_players(dir1, dir2, self.base_url)
    #         self.assertEqual(200, response.status_code)

    # def test_manual_post_request(self):
    #     dir1 = input("Pacman dir(Left, Right, Up, Down): ")
    #     dir2 = input("Ghost dir(Left, Right, Up, Down): ")
    #     data = {"pacman": {"dir": dir1}, "ghost": {"dir": dir2}}
    #     response = requests.post(f"{self.base_url}/players", json=data)
    #     self.assertEqual(200, response.status_code)

    # def test_moving_on_path(self):
    #     moves = [("Right", "Down"),
    #              ("Right", "Down"),
    #              ("Right", "Down"),
    #              ("Down", "Right"),
    #              ("Down", "Right"),
    #              ("Down", "Right"),
    #              ("Right", "Right"),
    #              ("Right", "Right"),
    #              ("Right", "Right"),
    #              ("Up", "Right"),
    #              ("Up", "Right"),
    #              ("Up", "Right"),
    #              ("Up", "Right"),
    #              ("Up", "Right"),
    #              ("Up", "Right"),
    #              ("Left", "Down"),
    #              ("Left", "Down"),
    #              ("Left", "Down"),
    #              ("Down", "Left"),
    #              ("Down", "None"),
    #              ("Down", "None"),
    #              ("None", "Down"),
    #              ("None", "Down"),
    #              ("None", "Down"),
    #              ("None", "Down"), ]
    #     for pacman_dir, ghost_dir in moves:
    #         response = move_players(pacman_dir, ghost_dir, self.base_url)
    #         self.assertEqual(200, response.status_code)
    #         # sleep(0.5)

    def test_pacman_accuracy_on_path(self):
        moves = ["Right", "Right", "Right", "Down"]
        for pacman_dir in moves:
            move_players(pacman_dir, "None", self.base_url)
        data = get_game_state(self.base_url)
        new_x = 15 + 3
        new_y = 17 + 1
        self.assertEqual(new_x, data["pacman_location"]["x"])
        self.assertEqual(new_y, data["pacman_location"]["y"])

if __name__ == "__main__":
    unittest.main()
