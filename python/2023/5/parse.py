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
    

@dataclass
class Game:
    seeds: list[int] | list[(int, int)]
    maps: list[list[MappingRange]]
    seeds_type: str = 'list'

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
                seeds.append((start, start + length - 1))
            # Remove duplicates.
            seeds = list(set(seeds))
        else:
            raise ValueError(f'Unknown seeds type {seeds_type}')
        maps = [Mapping.from_lines(section.splitlines()[1:]) for section in sections]
        return cls(seeds=seeds, maps=maps, seeds_type=seeds_type)
    
    def get_final_translations(self) -> list[int]:
        translations = self.seeds
        for mapping in self.maps:
            translations = [mapping.translate(translation) for translation in translations]
        return translations
    
    def backward_translate(self, destination: int) -> int | None:
        # Start with the destination
        translation = destination
        for mapping in reversed(self.maps):
            translation = mapping.backward_translate(translation)
            if translation is None:
                return None
        return translation
    
    def destination_ranges(self) -> list[(int, int)]:
        ranges = []
        for range in self.maps[-1].ranges:
            ranges.append((range.destination_start, range.destination_end))
        ranges = sorted(ranges, key=lambda r: r[0])
        return ranges
    
    def has_seed(self, seed: int) -> bool:
        if self.seeds_type == 'list':
            return seed in self.seeds
        else:
            for start, end in self.seeds:
                if seed >= start and seed <= end:
                    return True
    

def parse(input: str, seeds_type='list') -> Game:
    return Game.from_str(input, seeds_type=seeds_type)