import ipc

JSON_LOCATION = "C:\\Users\\caelu\GodotProjects\\networked_pacman\\IPC.json"


def process():
    if ipc.correct_turn(JSON_LOCATION):
        ### AI PROCESSING STUFF
        data = ipc.read_game_state(JSON_LOCATION)
        print(data)
        ### AI SENDING STUFF
        ipc.move_players(JSON_LOCATION, "Left")
        ipc.swap_process(JSON_LOCATION)
        print("*"*20)
        print("Changed")
        print("*" * 20)
        exit()
    else:
        print("Not changed")


if __name__ == "__main__":
    while True:
        process()
