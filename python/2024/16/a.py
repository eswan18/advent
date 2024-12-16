from .maze import Maze, find_shortest_path
import sys

sys.setrecursionlimit(3000)


def a(input: str) -> str:
    maze = Maze.from_str(input)
    return str(find_shortest_path(maze))
