from .hash import ascii_hash


def a(input: str) -> str:
    pieces = input.strip().split(",")
    hashes = list(ascii_hash(piece) for piece in pieces)
    result = sum(hashes)
    return str(result)