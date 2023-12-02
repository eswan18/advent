from dataclasses import dataclass

@dataclass
class Draw:
    RED: int
    BLUE: int
    GREEN: int

    @classmethod
    def from_str(cls, s: str) -> 'Draw':
        parts = s.split(', ')
        red = blue = green = 0
        for part in parts:
            part = part.strip()
            if part.endswith('red'):
                red = int(part.split(' ')[0])
            elif part.endswith('blue'):
                blue = int(part.split(' ')[0])
            elif part.endswith('green'):
                green = int(part.split(' ')[0])
        return cls(red, blue, green)

@dataclass
class Game:
    id: int
    draws: list[Draw]

    @classmethod
    def from_str(cls, s: str) -> 'Game':
        id_str, draws = s.split(':')
        id = int(id_str.split(' ')[1])
        draws = [Draw.from_str(draw.strip()) for draw in draws.split('; ')]
        return cls(id, draws)
    
    def possible_from_draw(self, test: Draw):
        for draw in self.draws:
            if draw.RED > test.RED:
                return False
            if draw.BLUE > test.BLUE:
                return False
            if draw.GREEN > test.GREEN:
                return False
        return True


TEST = Draw(12, 14, 13)
        

def a(input: str) -> str:
    id_sum = 0
    for line in input.splitlines():
        game = Game.from_str(line)
        if game.possible_from_draw(TEST):
            id_sum += game.id
    return str(id_sum)