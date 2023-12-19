from typing import NamedTuple


class Part(NamedTuple):
    x: int
    m: int
    a: int
    s: int

    @classmethod
    def build_from_line(cls, line: str) -> 'Part':
        line = line.removeprefix("{").removesuffix("}")
        parts = line.split(",")
        as_dict = {}
        for key, part in zip("xmas", parts):
            part = part[2:]
            as_dict[key] = int(part)
        return cls(**as_dict)