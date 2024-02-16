extends HTTPRequest
@onready var walls = get_parent().get_node("walls")
@onready var pacman = get_parent().get_node("pacman-area")
@onready var ghost = get_parent().get_node("ghost-area")
var connect_json = JSON.new()
var api_found = false
var timer = 0 

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
		
	# Will print the user agent string used by the HTTPRequest node (as recognized by httpbin.org).
	print(response)
	print(body)
	print("Response ^")

func _ready():
	# Create an HTTP request node and connect its completion signal.
	connect_to_api()

func _process(delta):
	if not api_found and delta > 1000:
		connect_to_api()
	timer += delta
	if timer > 0.01:
		api_pacman()
		timer = 0
	
func api_pacman(port=5000):
	var pacman_control_request = HTTPRequest.new()
	add_child(pacman_control_request)

	pacman_control_request.request_completed.connect(pacman.ai_pacman)
	
	var error = pacman_control_request.request("http://127.0.0.1:%d/players" % port, PackedStringArray(), HTTPClient.METHOD_GET)
	if error != OK:
		push_error("An error occurred in the HTTP request.")

func api_game_state(game_state: Dictionary, port=5000):
	var game_state_post = HTTPRequest.new()
	add_child(game_state_post)
	
	
	var json = JSON.stringify(game_state)
	var headers = ["Content-Type: application/json"]
	var error = game_state_post.request("http://127.0.0.1:%d/game_state" % port, headers, HTTPClient.METHOD_POST, json)
	if error != OK:
		push_error("An error occurred in the HTTP request.")
	

# Called when the HTTP request is completed.

