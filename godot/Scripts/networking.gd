extends HTTPRequest
@onready var walls = get_parent().get_node("walls")
@onready var pacman = get_parent().get_node("pacman-area")
@onready var ghost = get_parent().get_node("ghost-area")
var connect_json = JSON.new()
var api_found = false
var timer = 0 
var pid = 0
var game_state_record

func _ready():
	# Starts the relay server and keeps track of it's PID for ending the process
	# Process should be ended when program is quit properly by invoking _notification 
	pid = OS.create_process("python", ["../relay.py", "--port", str(5000)])
	print("Intermediary relay server running at PID: ", pid)
	
	# connect_to_api verifies that the API/server exists and is the proper one, could be removed
	# For clarities sake, however it was already written and it should just make
	# sure the program is more reliable
	connect_to_api()

func _process(delta):
	# This part of process asserts that a relay server exists, if not it  
	# waits 1s before trying again
	if not api_found and delta > 1000:
		connect_to_api()
	# Timer is used to slow down the polling of requests to the server, 
	# delta is added to timer as delta is the difference of time between calls
	# to _process
	timer += delta
	if timer > 0.05:
		# request_get_ai_instruction is the get request to the relay server for
		# player movements. It's polled once the above time(ms) is elapsed
		request_get_ai_instruction()
		
		# Updates the game state to reflect the game after moves have been made
		var game_state = compile_game_state(walls.get_map_state())
		game_state_record = game_state
		# Posts the current game state to the relay server, to be provided to 
		# the AI
		request_post_update_game_state(game_state)
		timer = 0

# This function is used to gracefully KILL the relay server based on the stored
# PID. While I'm not certain, this process does not seem to be called if the
# game process is improperly ended(could result in alot of running python tasks)
func _notification(what):
	if what == NOTIFICATION_WM_CLOSE_REQUEST:
		OS.kill(pid)
		get_tree().quit() # default behavior

# This function simply updates the game state and returns it, this 
# could be one place to handle or record whether a game has been won or lost
func compile_game_state(game_state: Dictionary):
	game_state["ghost_location"]["x"] = ghost.get_current_pos().x
	game_state["ghost_location"]["y"] = ghost.get_current_pos().y
	game_state["pacman_location"]["x"] = pacman.get_current_pos().x
	game_state["pacman_location"]["y"] = pacman.get_current_pos().y
	game_state["score"] = pacman.get_score()
	return game_state

# Tests that the server exists 
func connect_to_api(port=5000):
	# Verifies that the server being connected to is the proper one and that it 
	# exists
	var http_request = HTTPRequest.new()
	add_child(http_request)
	
	# This ties the _http_connected_completed to be executed on the response of
	# a completed request
	http_request.request_completed.connect(_http_connected_completed)
	print("Ready") 
	
	# Perform a GET request. The URL below returns JSON as of writing.
	# Handling and logging of errors, after sending the request
	var error = http_request.request("http://127.0.0.1:%d/connect" % port, PackedStringArray(), HTTPClient.METHOD_GET)
	if error != OK:
		push_error("An error occurred in the HTTP request.")
		log_error("Error when connecting: {}".format([error]))
		
		
func _http_connected_completed(_result, _response_code, _headers, body):
	# Handles the response of the initial connection check, sets api_found's val
	print("http request, asserting that server is found complete")
	connect_json.parse(body.get_string_from_utf8())
	var response = connect_json.get_data()
	if response:
		if response[0]["connect_code"] == "Imagines3-Payday-Impish":
			api_found = true

# This function handles the get requests to the relay server, in order to direct
# the players
func request_get_ai_instruction(port=5000):
	var player_control_request = HTTPRequest.new()
	add_child(player_control_request)
	
	# Connects the two ai controls(pacman, ghost) to the same response
	player_control_request.request_completed.connect(pacman.ai_pacman)
	player_control_request.request_completed.connect(ghost.ai_ghost)
	
	# Handling and logging of errors, after sending the request
	var error = player_control_request.request("http://127.0.0.1:%d/players" % port, PackedStringArray(), HTTPClient.METHOD_GET)
	if error != OK:
		push_error("An error occurred in the HTTP request.")
		log_error("A error occured when trying to move the players: {}".format([error]))

# This function sends the post request, updating the game state on 
# the relay server
func request_post_update_game_state(game_state: Dictionary, port=5000):
	var game_state_post = HTTPRequest.new()
	add_child(game_state_post)
	
	# Conversion to json from dictionary
	var json = JSON.stringify(game_state)
	# Headers are needed to say what type of data is being sent
	var headers = ["Content-Type: application/json"]
	
	# Handling and logging of errors, after sending the request
	var error = game_state_post.request("http://127.0.0.1:%d/game_state" % port, headers, HTTPClient.METHOD_POST, json)
	if error != OK:
		push_error("An error occurred in the HTTP request.")
		log_error("Issue occurred when sending post request for game state")

# Quick helper function used to record any server issues on the godot side
func log_error(error: String):
	var f = FileAccess.open("res://log.txt", FileAccess.WRITE)
	f.store_line("{0}\n
		PID of Server(0 is not created): {1}\n
		Most Recent Game State:\n
		{3}".format([error, pid, game_state_record]))
	f.close()

