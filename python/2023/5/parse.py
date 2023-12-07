from dataclasses import dataclass


@dataclass
class MappingRange:
    source_start: int
    source_end: int
    delta: int

    def __post_init__(self):
        self.destination_start = self.source_start + self.delta
        self.destination_end = self.source_end + self.delta
        self.length = self.source_end - self.source_start + 1

    @classmethod
    def from_line(cls, line: str) -> 'MappingRange':
        destination_start, source_start, length = [int(s) for s in line.split()]
        source_end = source_start + length - 1
        delta = destination_start - source_start
        return cls(source_start, source_end, delta)
    
    def translate(self, source: int) -> int | None:
        if source < self.source_start or source > self.source_end:
            return None
        return source + self.delta
    
    def backward_translate(self, destination: int) -> int | None:
        if destination < self.destination_start or destination > self.destination_end:
            return None
        return destination - self.delta
    
    def destination_overlaps(self, other: 'MappingRange') -> bool:
        return (self.destination_start <= other.source_start <= self.destination_end) or (other.destination_start <= self.source_start <= other.destination_end)
    
    def reduce(self, other: 'MappingRange') -> list['MappingRange']:
        print(f'reducing {self} and {other}')
        # If the ranges don't overlap, just error.
        if not self.destination_overlaps(other):
            raise ValueError('Ranges do not overlap')
        if other.destination_start <= self.destination_start <= other.destination_end:
            beginning_of_overlap = self.source_start
        else:
            beginning_of_overlap = other.destination_start - self.delta
        if other.destination_start <= self.destination_end <= other.destination_end:
            end_of_overlap = self.source_end
        else:
            end_of_overlap = other.destination_end - self.delta
        overlap_range = MappingRange(beginning_of_overlap, end_of_overlap, self.delta + other.delta)
        new_ranges = [overlap_range]
        if self.source_start < beginning_of_overlap:
            new_ranges.append(MappingRange(self.source_start, beginning_of_overlap - 1, self.delta))
        if other.source_start < beginning_of_overlap:
            new_ranges.append(MappingRange(other.source_start, beginning_of_overlap - 1, other.delta))
        if self.source_end > end_of_overlap:
            new_ranges.append(MappingRange(end_of_overlap + 1, self.source_end, self.delta))
        if other.source_end > end_of_overlap:
            new_ranges.append(MappingRange(end_of_overlap + 1, other.source_end, other.delta))
        print('new ranges:')
        for range in new_ranges:
            print(range)
        return new_ranges

    def __str__(self) -> str:
        return f'[{self.source_start}-{self.source_end}]  ({"+" if self.delta > 1 else ""}{self.delta})'
    

@dataclass
class Mapping:
    ranges: list[MappingRange]

    def translate(self, source: int) -> int:
        # Search all the individual ranges for one that matches.
        for mapping_range in self.ranges:
            translation = mapping_range.translate(source)
            if translation is not None:
                return translation
        return source
    
    def backward_translate(self, destination: int) -> int:
        # Search all the individual ranges for one that matches.
        for mapping_range in self.ranges:
            translation = mapping_range.backward_translate(destination)
            if translation is not None:
                return translation
        return destination

    @classmethod
    def from_lines(cls, lines: list[str]) -> 'Mapping':
        ranges = sorted([MappingRange.from_line(line) for line in lines], key=lambda r: r.source_start)
        return cls(ranges)
    
    def reduce(self, other: 'Mapping') -> 'Mapping':
        ranges = sorted(self.ranges.copy(), key=lambda r: r.destination_start)
        other_ranges = sorted(other.ranges.copy(), key=lambda r: r.source_start)
        unused_other_ranges = []
        new_ranges = []
        self_idx = 0
        other_idx = 0
        while self_idx < len(ranges) and other_idx < len(other_ranges):
            range = ranges[self_idx]
            other_range = other_ranges[other_idx]
            if range.destination_overlaps(other_range):
                new_ranges.extend(range.reduce(other_range))
                self_idx += 1
                other_idx += 1
            else:
                # If the ranges don't overlap, just keep the one that starts first and repeat.
                if range.destination_start < other_range.destination_start:
                    new_ranges.append(range)
                    self_idx += 1
                else:
                    unused_other_ranges.append(other_range)
                    other_idx += 1
        # If we still have some leftover ranges, add them.
        remaining_ranges = ranges[self_idx:] + other_ranges[other_idx:]
        new_ranges.extend(remaining_ranges)
        return self.__class__(new_ranges)

   

@dataclass
class Game:
    seeds: list[int]
    maps: list[list[MappingRange]]

    @classmethod
    def from_str(cls, input: str, seeds_type: str = 'list') -> 'Game':
        input = input.strip()
        sections = input.split('\n\n')
        # The first line defines the seeds.
        seed_line, *sections = sections
        if seeds_type == 'list':
            seeds = [int(seed) for seed in seed_line.split(': ')[1].split()]
        elif seeds_type == 'range':
            seeds = []
            seed_entries = [int(seed) for seed in seed_line.split(': ')[1].split()]
            # Take two seeds at a time
            for start, length in zip(seed_entries[::2], seed_entries[1::2]):
                new_seeds = list(range(start, start + length - 1))
                seeds.extend(new_seeds)
            # Remove duplicates.
            seeds = list(set(seeds))
        else:
            raise ValueError(f'Unknown seeds type {seeds_type}')
        maps = [Mapping.from_lines(section.splitlines()[1:]) for section in sections]
        return cls(seeds=seeds, maps=maps)
    
    def get_final_translations(self) -> list[int]:
        translations = self.seeds
        for mapping in self.maps:
            translations = [mapping.translate(translation) for translation in translations]
        return translations
    
    def reduce(self) -> None:
        while len(self.maps) > 1:
            self.maps[0] = self.maps[0].reduce(self.maps[1])
            self.maps.pop(1)


def parse(input: str, seeds_type='list') -> Game:
    return Game.from_str(input, seeds_type=seeds_type)