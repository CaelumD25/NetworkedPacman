extends Area2D
@onready var walls = get_parent().get_node("walls")
var direction = Vector2(0,0)
var SPEED = 0
var CELL_SIZE = 8
var score = 0
var player_state = JSON.new()
var nonce = 0 
var timer = 0

# Called when the node enters the scene tree for the first time.
func _ready():
	$AnimatedSprite2D.play("moving")
	var res = walls.maze_to_matrix_representation()
	for x in range(res.size()):
		print(res[x])

func current_pos()-> Vector2:
	return position

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

func move_ghost(direction: Vector2, rot: float):
	rotation = rot
	if walls.is_vacant(position + (CELL_SIZE*direction)):
		position += CELL_SIZE * direction

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

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	player_ghost()
