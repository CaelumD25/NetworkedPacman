extends HTTPRequest
@onready var walls = get_parent().get_node("walls")
@onready var pacman = get_parent().get_node("pacman-area")
@onready var ghost = get_parent().get_node("ghost-area")
var connect_json = JSON.new()
var api_found = false
var timer = 0 
var pid = 0
var game_state

func _ready():
	# Create an HTTP request node and connect its completion signal.
	pid = OS.create_process("python", ["../relay.py", "--port", str(5000)])
	print("Intermediary relay server running at PID: ", pid)
	connect_to_api()

func _process(delta):
	if not api_found and delta > 1000:
		connect_to_api()
	timer += delta
	if timer > 0.05:
		ai()
		game_state = compile_game_state(walls.get_map_state())
		update_game_state(game_state)
		timer = 0

func _notification(what):
	if what == NOTIFICATION_WM_CLOSE_REQUEST:
		OS.kill(pid)
		get_tree().quit() # default behavior

func compile_game_state(game_state: Dictionary):
	game_state["ghost_location"]["x"] = pacman.get_current_pos()[0]
	game_state["ghost_location"]["y"] = pacman.get_current_pos()[1]
	game_state["pacman_location"]["x"] = ghost.get_current_pos()[0]
	game_state["pacman_location"]["y"] = ghost.get_current_pos()[1]
	game_state["score"] = pacman.get_score()
	return game_state

func connect_to_api(port=5000):
	var http_request = HTTPRequest.new()
	add_child(http_request)
	http_request.request_completed.connect(_http_connected_completed)
	print("Ready")
	
	# Perform a GET request. The URL below returns JSON as of writing.
	var error = http_request.request("http://127.0.0.1:%d/connect" % port, PackedStringArray(), HTTPClient.METHOD_GET)
	if error != OK:
		push_error("An error occurred in the HTTP request.")
	print("Error %d" % error)

func _http_connected_completed(result, response_code, headers, body):
	print("http request complete")
	connect_json.parse(body.get_string_from_utf8())
	var response = connect_json.get_data()
	if response:
		if response[0]["connect_code"] == "Imagines3-Payday-Impish":
			api_found = true

func ai(port=5000):
	var player_control_request = HTTPRequest.new()
	add_child(player_control_request)

	player_control_request.request_completed.connect(pacman.ai_pacman)
	player_control_request.request_completed.connect(ghost.ai_ghost)
	
	var error = player_control_request.request("http://127.0.0.1:%d/players" % port, PackedStringArray(), HTTPClient.METHOD_GET)
	if error != OK:
		push_error("An error occurred in the HTTP request.")

func finished_turn(port=5000):
	var finish_turn_request = HTTPRequest.new()
	add_child(finish_turn_request)
	var error = finish_turn_request.request("http://127.0.0.1:%d/done" % port, PackedStringArray(), HTTPClient.METHOD_GET)
	if error != OK:
		push_error("An error occurred in the HTTP request.")

func update_game_state(game_state: Dictionary, port=5000):
	var game_state_post = HTTPRequest.new()
	add_child(game_state_post)
	
	var json = JSON.stringify(game_state)
	var headers = ["Content-Type: application/json"]
	var error = game_state_post.request("http://127.0.0.1:%d/game_state" % port, headers, HTTPClient.METHOD_POST, json)
	if error != OK:
		push_error("An error occurred in the HTTP request.")
	

# Called when the HTTP request is completed.

