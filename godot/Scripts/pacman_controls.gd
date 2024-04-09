extends Area2D
@onready var walls = get_parent().get_node("walls")

# Depending on how we detect the end game state, this ghost-area dependency can be removed
@onready var ghost = get_parent().get_node("ghost-area")

# GLOBAL VARIABLES for pacman
var CELL_SIZE = 8
var score = 0
var player_state = JSON.new()

# Called when the node enters the scene tree for the first time.
func _ready():
	$AnimatedSprite2D.play("moving")

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(_delta):
	player_pacman()
	if position == ghost.get_current_pos():
		pass
		#get_tree().quit()

# Returns the location of Pacman, rounded to the same value as a tile index in
# the game state matrix
func get_current_pos()-> Vector2:
	return floor(position/Vector2(CELL_SIZE,CELL_SIZE))

# Returns the current score of Pacman for adding to the game state
func get_score()-> int:
	return score

# Directs Pacman in a direction as in it faces Pacman in a direction and then moves
func direct_pacman(dir: String) -> bool:
	if dir == "Up":
		#move up 
		move_pacman(Vector2(0,-1), deg_to_rad(-90))
		return true
	elif dir == "Down":
		#move down
		move_pacman(Vector2(0,1), deg_to_rad(90))
		return true
	elif dir == "Left":
		#move left 
		move_pacman(Vector2(-1,0), deg_to_rad(180))
		return true
	elif dir == "Right":
		#move right 
		move_pacman(Vector2(1,0), 0)
		return true
	else:
		return false

# Does the moving of pacman, if we want to make the map 'infinite' in size
# We would have to add a condition here to check if the tile is outside of the
# Tile space(area with painted tiles) and change pacman's position to the other 
# side
func move_pacman(direction: Vector2, rot: float):
	rotation = rot
	if walls.is_vacant(position + (CELL_SIZE*direction)):
		position += CELL_SIZE * direction
		score = walls.eat(position, score)

# The AI version of player_pacman, this is called when a GET request is made to
# the relay server. This happens alot and should only happen once for each 
# instruction delivered by the AI, therefore if a new move instruction has not 
# been POSTed by the AI, a response code of FORBIDDEN(403) is returned until it
# has. This function is polled and connected in networking.gd in it's _process
func ai_pacman(_result, response_code, _headers, body):
	if response_code != 403:
		player_state.parse(body.get_string_from_utf8())
		var response = player_state.get_data()
		print(response)
		if response:
			direct_pacman(response["pacman"]["dir"])

func player_pacman():
	if Input.is_action_just_pressed("ui_up"):
		#move up 
		direct_pacman("Up")
	elif Input.is_action_just_pressed("ui_down"):
		#move down
		direct_pacman("Down")
	elif Input.is_action_just_pressed("ui_left"):
		#move left 
		direct_pacman("Left")
	elif Input.is_action_just_pressed("ui_right"):
		#move right 
		direct_pacman("Right")
		

