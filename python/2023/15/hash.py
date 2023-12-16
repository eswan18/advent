from dataclasses import dataclass
from typing import Literal
from collections import defaultdict, OrderedDict


class State:
    boxes: dict[int, OrderedDict[str, int]]

    def __init__(self):
        self.boxes = defaultdict(OrderedDict)
    
    def __str__(self):
        s = ''
        for box in sorted(self.boxes.keys()):
            s += f'Box {box}: {self.boxes[box]}\n'
        return s
    
    def execute(self, i: 'Instruction'):
        box_num = i.box()
        match i:
            case Instruction(label, '-', None):
                if label in self.boxes[box_num]:
                    self.boxes[box_num].pop(label)
            case Instruction(label, '=', focal_length):
                self.boxes[box_num][label] = focal_length
            case _:
                raise RuntimeError(f'Invalid instruction: {i}')
    
    def focusing_power(self) -> int:
        sum = 0
        for box_num, lenses in self.boxes.items():
            for slot_num, label in enumerate(lenses):
                focus_power = (slot_num + 1) * lenses[label] * (box_num + 1)
                sum += focus_power
        return sum


@dataclass
class Instruction:
    label: str
    operation: Literal['=', '-']
    focal_length: int | None

    @classmethod
    def build_from_string(cls, s: str) -> 'Instruction':
        parts = s.split('=')
        if len(parts) == 1:
            # this means we're on a dash step
            label = s[:-1]
            return cls(label, '-', None)
        else:
            label, focal_length = parts
            return cls(label, '=', int(focal_length))
    
    def box(self) -> int:
        return ascii_hash(self.label)


def ascii_hash(s: str) -> int:
    current_val = 0
    # Get the ascii code of each character in the string
    for c in s:
        current_val += ord(c)
        current_val *= 17
        current_val %= 256
    return current_val
