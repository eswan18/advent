from .parse import parse


def a(input: str) -> str:
   cards = parse(input)
   result = sum(c.points() for c in cards)
   return str(result)