from itertools import product

from .part import Part
from .rule import Ruleset


def b(input: str) -> str:
    rules_section, parts_section = input.split("\n\n")
    ruleset = Ruleset.build_from_str(rules_section)
    count = 0
    for x, m, a, s in product(range(4000), repeat=4):
        p = Part(x, m, a, s)
        if ruleset.route(p):
            count += 1

    return str(count)