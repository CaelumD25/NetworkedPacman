from random import Random, randint

from flask import Flask, json, request, jsonify
from graph import create_graph, Node, print_graph

## Server for the inverted pacman

connection = [{"connect_code": "Imagines3-Payday-Impish"}]

app = Flask(__name__)
nonce = 1

state_read = True

@app.route('/connect', methods=['GET'])
def get_connection():
    return json.dumps(connection)

@app.route('/players', methods=['GET'])
def control_players():
    global nonce
    global next_state_ready
    dir = ["Right", "Up", "Left", "Down"][randint(0, 3)]
    dir2 = ["Right", "Up", "Left", "Down"][randint(0, 3)]
    tmp = json.dumps([{"pacman": {"dir": dir, "nonce": nonce}, "ghost": {"dir": dir2, "nonce": 1}}])
    nonce += 1
    if True:
        state_read = False
        return tmp
    else:
        return None

@app.route('/game_state', methods=['POST'])
def map_state():
    new_post_request = request.json
    global next_state_ready
    maze = new_post_request["tiles"]
    graph_repr = create_graph(maze)
    print_graph(graph_repr)
    next_state_ready = True
    return [{"Test": 1}]


@app.route('/player_positions', methods=['POST'])
def add_book():
    new_post_request = request.json
    print(new_post_request)

    # Generate a unique ID for the new book



if __name__ == '__main__':
    app.run()
