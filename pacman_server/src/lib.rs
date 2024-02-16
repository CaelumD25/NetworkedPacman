use godot::prelude::*;
struct MyExtension;

#[gdextension]
unsafe impl ExtensionLibrary for MyExtension {}


use std::cell::Ref;
use std::sync::{Arc, Mutex};
use godot::log::print;
use warp::{Filter, Reply};
use godot::prelude::{ToGodot, Variant};
use godot::engine::Area2D;
use godot::engine::Node2D;
use godot::sys::uint_fast8_t;

#[derive(GodotClass)]
#[class(base=Node2D)]
struct Network {
    started: uint_fast8_t,
    #[base]
    node2d: Base<Node2D>
}

async fn move_players(node: Ref<'_, Node2D>, data: RequestData) -> Result<impl Reply, warp::Rejection>{
    println!("{:?}", "Hello World, this is a post request");
    println!("{:?}", data.pacman.dir);
    crate::move_pacman(data.pacman.dir, node);
    Ok(warp::reply::json(&"Item added successfully"))
}


fn move_pacman(dir: String, node: Ref<Node2D>){
    let dir_unsafe = dir.to_variant();
}

// Handler for getting all items from the database
async fn game_state(node: Ref<'_, Node2D>) -> Result<impl Reply, warp::Rejection> {
    println!("{:?}", "Hello World, this is a get request");
    Ok(warp::reply::json(&"HELLO!"))
}

#[tokio::main]
async fn net_main() {
    // Shared state for the database
    // POST /item
    let post_item = warp::path!("POST")
        .and(warp::post())
        .and(warp::body::json()) //TODO ADD Passing in of var
        .and_then(move_players);

    // GET /items
    let get_items = warp::path!("GET")
        .and(warp::get())
        .and_then(crate::game_state);

    // Combine routes
    let routes = post_item.or(get_items);

    println!("Server running on http://localhost:8000/");

    // Start the server
    warp::serve(routes).run(([127, 0, 0, 1], 8000)).await;
}

#[godot_api]
impl INode2D for Network {
    fn init(node2d: Base<Self::Base>) -> Self {
        println!("Hello!");
        Self { started };
        Self { node2d }
    }
    fn start_net(&self) {
        let node = self.base().get_node_as::<Node3D>("Child");
        net_main(node);
    }
    fn process(&mut self, delta: f64){
        godot_print!("Hello from process");
    }

// Define a custom filter to share the database state between handler

}

#[derive(Debug, serde::Serialize, serde::Deserialize)]
struct RequestData {
    pacman: PlayerData,
    ghost: PlayerData,
}

#[derive(Debug, serde::Serialize, serde::Deserialize)]
struct PlayerData {
    dir: String,
    nonce: i32,
}

#[derive(Debug, serde::Serialize, serde::Deserialize)]
struct PacmanLocation {
    x: usize,
    y: usize,
}

#[derive(Debug, serde::Serialize, serde::Deserialize)]
struct GhostLocation {
    x: usize,
    y: usize,
}

#[derive(Debug, serde::Serialize, serde::Deserialize)]
struct ResponseData {
    rows: usize,
    columns: usize,
    tiles: Vec<Vec<i32>>, // Assuming the tiles are represented as a matrix of integers
    pacman_location: PacmanLocation,
    ghost_location: GhostLocation,
}





