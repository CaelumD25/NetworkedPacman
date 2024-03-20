import json

def correct_turn(file_location: str) -> bool:
    result = False
    with open(file_location, "r") as file:
        try:
            data = json.load(file)
        except:
            print(file.read())
            data = None
        if data["ai_processing"] == 1:
            result = True
    return result

def read_game_state(file_location: str) -> dict:
    result = None
    with open(file_location, "r") as file:
        data = json.load(file)
        if data["ai_processing"] == 1:
            result = data
    return result

def move_players(file_location: str, pacman_dir="none", ghost_dir="none") -> dict:
    result = None
    with open(file_location, "r") as file:
        data = json.load(file)
    with open(file_location, "w") as file:
        try:
            if data["ai_processing"] == 1:
                result = True
            else:
                result = False
            data["game"]["players"]["pacman"]["dir"] = pacman_dir
            data["game"]["players"]["ghost"]["dir"] = ghost_dir
        except Exception as e:
            print("Error setting json values " + e)
        json.dump(data, file, indent=4)
    return result


def swap_process(file_location: str):
    result = False
    with open(file_location, "r") as file:
        data = json.load(file)
    with open(file_location, "w") as file:
        try:
            if data["game_processing"] == 1:
                result = True
            data["game_processing"] = 1
            data["ai_processing"] = 0
        except Exception as e:
            print("Error setting json values " + e)
        json.dump(data, file, indent=4)
    return result
