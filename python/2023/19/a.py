from .rule import Ruleset
from .part import Part

def a(input: str) -> str:
    rules_section, parts_section = input.split("\n\n")
    ruleset = Ruleset.build_from_str(rules_section)
    parts = [Part.build_from_line(line) for line in parts_section.splitlines()]
    running_sum = 0
    for p in parts:
        if ruleset.route(p):
            running_sum += p.x + p.m + p.a + p.s
    return str(running_sum)