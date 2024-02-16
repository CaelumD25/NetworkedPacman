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

### Networking Idea
Current networking idea

![doc_assets/network_diagram.png](https://github.com/CaelumD25/networked_pacman/blob/main/doc_assets/network_diagram.png)

The current plan is to implent this using [gdextension](https://docs.godotengine.org/en/stable/tutorials/scripting/gdextension/what_is_gdextension.html) and Godot Rust

This plan should definitely be changed if some other type of Interprocess Communication can be done in a better way
