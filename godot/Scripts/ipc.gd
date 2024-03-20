extends Node
@onready var pacman = get_parent().get_node("pacman")
@onready var walls = get_parent().get_node("walls")
@onready var ghost = get_parent().get_node("ghost")

# Called when the node enters the scene tree for the first time.
func _ready():
	# Replace with function body.
	var file = FileAccess.open("res://IPC.json", FileAccess.READ_WRITE)
	file.seek(0)
	assert(file != null)
	var json_text = file.get_as_text(true).replace("\n","")
	print(json_text)
	var data = JSON.parse_string(file.get_as_text())
	assert(file != null && data != null)
	var map_state = walls.get_map_state()
	data["map"]["rows"] = map_state["rows"]
	data["map"]["columns"] = map_state["columns"]
	data["map"]["tiles"] = map_state["tiles"]
	var pacman_tile_position = pacman.get_location()
	data["map"]["pacman_location"]["x"] = pacman_tile_position[0]
	data["map"]["pacman_location"]["y"] = pacman_tile_position[1]
	var ghost_tile_position = ghost.get_location()
	data["map"]["pacman_location"]["x"] = ghost_tile_position[0]
	data["map"]["pacman_location"]["y"] = ghost_tile_position[1]
	data["game_processing"] = 1
	data["ai_processing"] = 0
	file.store_string(JSON.stringify(data))
	# Close the file
	file.close()

func correct_turn():
	var result = false
	var file = FileAccess.open("res://IPC.json", FileAccess.READ)
	var data = JSON.parse_string(file.get_as_text())
	if data["game_processing"]==1 and data["ai_processing"]==0:
		result = true
	file.close()
	return result

func swap_process():
	var result = false
	var file = FileAccess.open("res://IPC.json", FileAccess.READ_WRITE)
	var data = JSON.parse_string(file.get_as_text())
	if data["game_processing"]==1 and data["ai_processing"]==0:
		data["game_processing"]=0
		data["ai_processing"]=1
		file.store_string(JSON.stringify(data))
		result = true
	file.close()
	return result

func update_json_state():
	pass
	
func move_players():
	var result = false
	var file = FileAccess.open("res://IPC.json", FileAccess.READ_WRITE)
	var data = JSON.parse_string(file.get_as_text())
	if data["game_processing"]==1 and data["ai_processing"]==0:
		pacman.direct_pacman(data["game"]["players"]["pacman"]["dir"])
		ghost.direct_ghost(data["game"]["players"]["ghost"]["dir"])
		file.store_string(JSON.stringify(data))
		result = true
	file.close()
	return result
	
# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	if correct_turn():
		move_players()
		update_json_state()
		swap_process()
