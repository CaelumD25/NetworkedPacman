extends CanvasLayer

class_name ui
signal game_started
var game_points = 0

@onready var gameover_screen = $gameover_screen

func _ready():
	pass
	
func update_points(points: int):
	game_points = points
	

func on_game_over():
	gameover_screen.visible = true
	$gameover_screen/gameover_message/score.text = "Score: %d" % game_points
	

func _on_reset_button_pressed():
	get_tree().reload_current_scene()
