using Godot;
using System;

public partial class game : Node2D
{
	// Called when the node enters the scene tree for the first time.
	public override void _Ready()
	{
		Console.WriteLine("Hello, world!");
	}

	// Called every frame. 'delta' is the elapsed time since the previous frame.
	public override void _Process(double delta)
	{
		Console.WriteLine("Hello, world! Process");
	}
}
