from .maze import Maze, n_tiles_covered_by_shortest_path

def b(input: str) -> str:
    maze = Maze.from_str(input)
    return str(n_tiles_covered_by_shortest_path(maze))

