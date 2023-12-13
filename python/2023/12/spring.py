from enum import StrEnum
from dataclasses import dataclass
from typing import Self


class SpringState(StrEnum):
    Operational = '.'
    Damaged = '#'

    def __str__(self) -> str:
        return self.value


@dataclass
class SpringArrangement:
    springs: list[SpringState]

    def damaged_counts(self) -> list[int]:
        counts = []
        i = 0
        while i < len(self.springs):
            count = 0
            spring = self.springs[i]
            while spring == SpringState.Damaged:
                i += 1
                count += 1
                if i == len(self.springs):
                    break
                spring = self.springs[i]
            if count > 0:
                counts.append(count)
            i += 1
        return counts

class SpringStateReading(StrEnum):
    Operational = '.'
    Damaged = '#'
    Unknown = '?'


@dataclass
class SpringArrangementReading:
    springs: list[SpringStateReading]
    damaged_counts: list[int]

    @classmethod
    def build_from_line(cls, line: str) -> Self:
        spring_part, count_part = line.split(' ')
        springs = [SpringStateReading(s) for s in spring_part]
        damaged_counts = [int(c) for c in count_part.split(',')]
        return cls(springs, damaged_counts)
    
    def __str__(self) -> str:
        return f'{"".join([str(s) for s in self.springs])} {",".join([str(c) for c in self.damaged_counts])}'
    
    def all_arrangements(self) -> list[SpringArrangement]:
        try:
            first_unknown = self.springs.index(SpringStateReading.Unknown)
        except ValueError:
            # This indicates there are no unknown springs.
            arrangement = SpringArrangement([SpringState(str(spring)) for spring in self.springs])
            if arrangement.damaged_counts() == self.damaged_counts:
                return [arrangement]
            else:
                return []
        else:
            first_unknown = self.springs.index(SpringStateReading.Unknown)
            arrangements = []
            for known_state in [SpringStateReading.Operational, SpringStateReading.Damaged]:
                springs = self.springs.copy()
                springs[first_unknown] = known_state
                arrangements.extend(SpringArrangementReading(springs, self.damaged_counts).all_arrangements())
            return arrangements
    
    def arrangement_count(self) -> int:
        return len(self.all_arrangements())
            