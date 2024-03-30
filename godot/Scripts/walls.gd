extends TileMap

var VACANT_TILE = Vector2i(37, 5)
var PILL_TILE = Vector2i(38, 5)
var TILE_SIZE = 8

# Represents tile types
class TileRepr:
	var id
	var type
	func _init(type_id: int):
		id = type_id
		type = ""
		if type_id == 0:
			# Pacman should always be on a 0 or 2
			type = "Vacant"
		elif type_id == 1:
			type = "Wall"
		elif type_id == 2:
			# Pacman should always be on a 0 or 2
			type = "Pill"
		elif type_id == -1:
			type = "Invalid"
	
	func get_id():
		return id
	
	func get_type():
		return type


# There could be a better way of determining tile types but here is how I figured
# it out.
# Tiles can be defined by their location within the tile atlas, this is something
# in the godot editor, and it's kinda like the pallet of tiles. Their locations
# are defined at the top of this file if there is ever a need to change one of
# them.
# (A helpful analogy would be imagining a painting and painting pallet; 
# if you were color blind, you could technically figure out every color on a 
# painting if you were given the location of where each color came from on the 
# pallet providing it was labelled)
func get_tile_type(tile_coord: Vector2i) -> TileRepr:
	if tile_coord == Vector2i(-1,-1):
		# Invalid
		return TileRepr.new(-1)
	elif tile_coord == VACANT_TILE:
		# Vacant
		return TileRepr.new(0)
	elif tile_coord == PILL_TILE:
		# Pill
		return TileRepr.new(2)
	else:
		# Wall
		return TileRepr.new(1)

# This function maps the absolute position(players) from the origin to the 
# number of tiles
func map_abs_pos_to_tile(pos: Vector2) -> Vector2i:
	var modified_vector = Vector2i()
	modified_vector.x = int(pos.x)/float(TILE_SIZE)
	modified_vector.y = int(pos.y)/float(TILE_SIZE)
	return modified_vector

# This function gets a TileRepr(Tile Representation) of the tile at the 
# current absolute position from the orign
func get_tile_from_abs_pos(pos :Vector2i, layer=0)->TileRepr:
	var modified_vector = map_abs_pos_to_tile(pos)
	var atlas_coords = get_cell_atlas_coords(layer, modified_vector)
	return get_tile_type(atlas_coords)
	
# This funciton says if a tile at a absolute position is 
# traversable(vacant of walls) 
func is_vacant(pos: Vector2) -> bool:
	var tile_type_id = get_tile_from_abs_pos(Vector2i(int(pos.x), int(pos.y))).get_id()
	if tile_type_id == 2 or tile_type_id == 0:
		return true
	return false

# If the tile at the current position is a pill, the pill will be replaced with
# a basic vacant tile(the black square), it also returns the score incremented
func eat(pos: Vector2, score: int):
	# Max Score 266
	var cur_tile = get_tile_from_abs_pos(Vector2i(int(pos.x), int(pos.y)))
	if cur_tile.get_id() == 2:
		set_cell(0, map_abs_pos_to_tile(pos), 0, VACANT_TILE)
		score += 1
	return score

# Called every frame. 'delta' is the elapsed time since the previous frame.
func get_map_state():
	var martrix_repr = maze_to_matrix_representation()
	var maze = {
		"rows": martrix_repr.size(),
		"columns": martrix_repr[0].size(),
		"tiles": maze_to_matrix_representation(),
		"pacman_location": {
			"x": 0,
			"y": 0
			},
		"ghost_location": {
			"x": 0,
			"y": 0
			},
		"score": 0
		}
	return maze

# Since the tiles in godot are not a matrix, they need to be adapted so that 
# they can be added to the state
func maze_to_matrix_representation() -> Array:
	var mock_position = Vector2i(
		floor(TILE_SIZE/2.0),
		floor(TILE_SIZE/2.0)
	)
	var matrix = []
	var cur_tile_type = -1
	var row = 0
	while get_tile_from_abs_pos(mock_position).get_id() != -1:
		matrix.append([])
		while get_tile_from_abs_pos(mock_position).get_id() != -1:
			cur_tile_type = get_tile_from_abs_pos(mock_position)
			matrix[row].append(cur_tile_type.get_id())
			mock_position.x += TILE_SIZE
		mock_position.x = floor(TILE_SIZE/2.0)
		mock_position.y += TILE_SIZE
		row += 1
	return matrix
	
