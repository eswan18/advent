from enum import StrEnum
from typing import Literal
from dataclasses import dataclass

class Direction(StrEnum):
    UP = "U"
    DOWN = "D"
    LEFT = "L"
    RIGHT = "R"


class Color:
    def __init__(self, r: int, g: int, b: int):
        self.r = r
        self.g = g
        self.b = b
    
    @classmethod
    def build_from_str(cls, color: str):
        color = color.removeprefix("#")
        r = int(color[0:2], 16)
        g = int(color[2:4], 16)
        b = int(color[4:6], 16)
        return cls(r, g, b)


@dataclass
class Instruction:
    direction: Direction
    distance: int
    color: Color

    @classmethod
    def build_from_line(cls, line: str, mode: Literal['naive', 'switched'] = 'naive'):
        parts = line.split(" ")
        direction = Direction(parts[0])
        distance = int(parts[1])
        color_string = parts[2].removeprefix("(").removesuffix(")")
        if mode == 'naive':
            color = Color.build_from_str(color_string)
            return cls(direction, distance, color)
        elif mode == 'switched':
            # We don't care about the color for anything, don't bother parsing it.
            color = None
            color_string = color_string.removeprefix("#")
            direction_code = color_string[-1]
            match int(direction_code):
                case 0:
                    direction = Direction.RIGHT
                case 1:
                    direction = Direction.DOWN
                case 2:
                    direction = Direction.LEFT
                case 3:
                    direction = Direction.UP
            distance = int(color_string[0:-1], 16)
            return cls(direction, distance, color)
        