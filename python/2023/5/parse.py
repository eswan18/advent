from dataclasses import dataclass


@dataclass
class MappingRange:
    source_start: int
    destination_start: int
    length: int

    @classmethod
    def from_line(cls, line: str) -> 'MappingRange':
        destination_start, source_start, length = line.split()
        return cls(int(source_start), int(destination_start), int(length))
    
    def translate(self, source: int) -> int | None:
        if source < self.source_start or source >= self.source_start + self.length:
            return None
        translation_factor = self.destination_start - self.source_start
        return source + translation_factor
    
    def backward_translate(self, destination: int) -> int | None:
        if destination < self.destination_start or destination >= self.destination_start + self.length:
            return None
        translation_factor = self.destination_start - self.source_start
        return destination - translation_factor


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
        return cls([MappingRange.from_line(line) for line in lines])
    

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


def parse(input: str, seeds_type='list') -> Game:
    return Game.from_str(input, seeds_type=seeds_type)