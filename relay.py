from flask import Flask, request, jsonify
import argparse


app = Flask(__name__)

connection = [{"connect_code": "Imagines3-Payday-Impish"}]

# Global recording state for the movement and game state
movement_instructions = {}
game_state = {}

# Flag to track whether there has been a POST request from the AI process and Godot Process
ai_process_posted = False
godot_process_posted = False

@app.route('/players', methods=['GET', 'POST'])
def movement():
    global movement_instructions, ai_process_posted, move_finished

    # Only the game process should be requesting get to players, this should not be called by the AI process
    if request.method == 'GET':
        if not ai_process_posted:
            return "AI hasn't posted yet. Access denied.", 403
        # Return the latest movement data to Godot game
        ai_process_posted = False
        return jsonify(movement_instructions)
    # Only the AI process should be updating the instructions of the players
    elif request.method == 'POST':
        # Receive movement data from Godot game
        if ai_process_posted:
            return "Godot hasn't moved yet, ignoring this could result in missed moves. Access denied.", 403
        movement_instructions = request.json
        # Forward movement data to AI process
        # Example: Forwarding movement data to AI process
        # forward_movement_to_ai(request.json)
        ai_process_posted = True
        return 'Movement data received and forwarded to AI'


@app.route('/game_state', methods=['GET', 'POST'])
def state():
    global godot_process_posted, game_state
    # Receive game state data from Godot game
    if request.method == 'GET':
        if not godot_process_posted:
            return "Game hasn't posted yet. Access denied.", 403
            # Return the latest movement data to Godot game
        godot_process_posted = False
        return jsonify(game_state)
    elif request.method == 'POST':
        game_state = request.json
        godot_process_posted = True
        # Forward game state data to AI process
        # Example: Forwarding game state data to AI process
        # forward_state_to_ai(request.json)
        return 'Game state data received and forwarded to AI'


@app.route('/connect', methods=['GET'])
def get_connection():
    return json.dumps(connection)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Start the intermediary relay server")
    parser.add_argument('--port', type=int, default=5000, help="Port number (default is 5000)")
    args = parser.parse_args()
    app.run(debug=True, port=args.port)  # You may want to set debug=False in production
