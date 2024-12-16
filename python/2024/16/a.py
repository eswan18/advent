from .maze import Maze, find_shortest_path

def a(input: str) -> str:
    maze = Maze.from_str(input)
    return str(find_shortest_path(maze))
