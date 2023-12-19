from dataclasses import dataclass
from typing import Literal

from .part import Part


@dataclass
class Test:
    field: Literal['x', 'm', 'a', 's']
    threshold: int
    isGt: bool
    # The name of the rule to send the result to, if it passes, or A(ccept)/R(eject).
    on_success: str

    def test(self, p: Part) -> bool:
        match self.field:
            case 'x':
                test_value = p.x
            case 'm':
                test_value = p.m
            case 'a':
                test_value = p.a
            case 's':
                test_value = p.s
        if self.isGt:
            return test_value > self.threshold
        else:
            return test_value < self.threshold
        
    @classmethod
    def build_from_str(cls, s: str) -> 'Test':
        field = s[0]
        isGt = s[1] == '>'
        threshold, on_success = s[2:].split(":")
        return cls(field, int(threshold), isGt, on_success)


@dataclass
class Rule:
    name: str
    tests: list[Test]
    fallback: str

    @classmethod
    def build_from_line(cls, line: str) -> 'Rule':
        parts = line.split("{")
        name = parts[0]
        tests_etc = parts[1].removesuffix("}")
        *tests, fallback = tests_etc.split(",")
        tests = [Test.build_from_str(test) for test in tests]
        return cls(name, tests, fallback)
    
    def route(self, part: Part) -> str:
        for test in self.tests:
            if test.test(part):
                return test.on_success
        return self.fallback


@dataclass
class Ruleset:
    rules: dict[str, Rule]

    @classmethod
    def from_rules(cls, rules: list[Rule]) -> 'Ruleset':
        return cls({rule.name: rule for rule in rules})
    
    @classmethod
    def build_from_str(cls, s: str) -> 'Ruleset':
        rules = [Rule.build_from_line(line) for line in s.splitlines()]
        return cls.from_rules(rules)
    
    def route(self, part: Part) -> bool:
        """Decides whether a part is accepted (true) or rejected (false)."""
        current_rule = self.rules["in"]
        while True:
            next_rule = current_rule.route(part)
            if next_rule == "A":
                return True
            elif next_rule == "R":
                return False
            else:
                current_rule = self.rules[next_rule]