# networked_pacman
A pacman game where both the ghost and pacman can be controlled by a rest api

## TODO
- [ ] Create a API for integration with other programs
- [ ] Handle a game over
- [ ] Handle a eventual reset(could be a restart from the program driving the API)

## Setup
You'll need [Godot +4.2.1](https://godotengine.org/download/) for the game, and rust +1.76.0

Rust can be installed via the methods below:

```zsh
# Linux (distro-independent)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Windows
winget install --id=Rustlang.Rustup -e

# macOS
brew install rustup
```


**Resources**
- [Godot rust book](https://godot-rust.github.io/book/index.html)
- [Learn Rust if you need it](https://www.rust-lang.org/learn)

### IPC is properly implemented!
After many headaches and lots of deliberation, we've got a nicely working form of IPC!

Using shared memory as a form of IPC seemed to only cause issues with race conditions, and it's behaviour was neither deterministic, nor as practical as it could have been.

Thanks to some great collaborative brainstorming, we've got a solution that works reliably and simply(Even if it is a little bit convoluted for the application).

#### The new plan
The new plan uses 3 independent processes which communicate through networking packets.
- The first process is the Game, which is the same as before, instead it now polls a relay server to communicate the information it needs to move the players while updating the game state.
- The second process is the AI process, which is the what decides what the players should be doing given a fresh game state representation.
- The third process is the Relay Intermediate Server, whish is what allows both the Game and AI proceses act as clients, bypassing the issues with godot we faced early on in our project.(This process is started and killed by the Game process)

Below are some charts to show how each process interacts in different scenarios

![doc_assets/inv_serv_typical_scenario](https://github.com/CaelumD25/networked_pacman/blob/main/doc_assets/inv_serv_typical_scenario.png)

![doc_assets/inv_serv_player_movements](https://github.com/CaelumD25/networked_pacman/blob/main/doc_assets/inv_serv_player_movements.png)

![doc_assets/inv_serv_ai_decisions](https://github.com/CaelumD25/networked_pacman/blob/main/doc_assets/inv_serv_ai_decisions.png)

Using this new architecture, it is now possible to run unit tests to verify it is all working properly

### Work to be done
- [ ] Figure out if it's possible to prevent race conditions when calling state after player multiple player movements(Only known issue with the IPC)
- [ ] Make the main framework for handling the map state, and the locations of the players
- [ ] Make the A* algorithm to drive the ghost
- [ ] Make the Minimax algorithm to drive pacman
