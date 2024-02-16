extends Area2D
@onready var walls = get_parent().get_node("walls")
@onready var ghost = get_parent().get_node("ghost-area")
var direction = Vector2(0,0)
var SPEED = 0
var CELL_SIZE = 8
var score = 0
var player_state = JSON.new()
var nonce = 0 
var ack = false

# Called when the node enters the scene tree for the first time.
func _ready():
	$AnimatedSprite2D.play("moving")

func current_pos()-> Vector2:
	return position

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
	
func move_pacman(direction: Vector2, rot: float):
	rotation = rot
	if walls.is_vacant(position + (CELL_SIZE*direction)):
		position += CELL_SIZE * direction
		score = walls.eat(position, score)


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
		
# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	player_pacman()
	if position == ghost.current_pos():
		pass
		#get_tree().quit()
	
	
	# This can be done better I'm sure
	
		
