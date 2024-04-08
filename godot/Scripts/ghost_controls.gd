extends Area2D
@onready var walls = get_parent().get_node("walls")

# GLOBAL VARIABLES for pacman
var CELL_SIZE = 8
var player_state = JSON.new()

# Called when the node enters the scene tree for the first time.
func _ready():
	$AnimatedSprite2D.play("moving")
	var res = walls.maze_to_matrix_representation()
	for x in range(res.size()):
		print(res[x])

func _process(_delta):
	# Comment out this to disable controlling the ghost manually
	player_ghost()

# Returns the location of pacman, rounded to the same value as a tile index in
# the game state matrix
func get_current_pos()-> Vector2:
	return floor(position/Vector2(CELL_SIZE,CELL_SIZE))

func direct_ghost(dir: String):
	if dir == "Up":
		#move up 
		move_ghost(Vector2(0,-1), 0)
	elif dir == "Down":
		#move down
		move_ghost(Vector2(0,1), 0)
	elif dir == "Left":
		#move left 
		move_ghost(Vector2(-1,0), 0)
	elif dir == "Right":
		#move right 
		move_ghost(Vector2(1,0), 0)
	else:
		pass

# Does the moving of ghost, if we want to make the map 'infinite' in size
# We would have to add a condition here to check if the tile is outside of the
# Tile space(area with painted tiles) and change ghost's position to the other 
# side
func move_ghost(direction: Vector2, rot: float):
	rotation = rot
	if walls.is_vacant(position + (CELL_SIZE * direction)):
		position += CELL_SIZE * direction

# The AI version of player_ghost, this is called when a GET request is made to
# the relay server. This happens alot and should only happen once for each 
# instruction delivered by the AI, therefore if a new move instruction has not 
# been POSTed by the AI, a response code of FORBIDDEN(403) is returned until it
# has. This function is polled and connected in networking.gd in it's _process
func ai_ghost(_result, response_code, _headers, body):
	if response_code != 403:
		player_state.parse(body.get_string_from_utf8())
		var response = player_state.get_data()
		if response:
			direct_ghost(response["ghost"]["dir"])

func player_ghost():
	if Input.is_action_just_released("move_up"):
		#move up 
		direct_ghost("Up")
	elif Input.is_action_just_released("move_down"):
		#move down
		direct_ghost("Down")
	elif Input.is_action_just_released("move_left"):
		#move left 
		direct_ghost("Left")
	elif Input.is_action_just_released("move_right"):
		#move right 
		direct_ghost("Right")


