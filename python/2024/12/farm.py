from typing import Self, NewType
from dataclasses import dataclass

PlantVariant = NewType('PlantVariant', str)

@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __str__(self) -> str:
        return f'({self.x}, {self.y})'

@dataclass(frozen=True)
class Region:
    plant: PlantVariant
    plots: frozenset[Point]

@dataclass
class Farm:
    regions: set[Region]

    def __str__(self) -> str:
        s = ''
        for region in self.regions:
            s += region.plant + ': '
            s += ', '.join(str(pt) for pt in region.plots)
            s += '\n'
        return s

@dataclass
class UnregionedFarm:
    """A farm that we haven't broken into regions yet."""
    plots: list[list[PlantVariant]]
    height: int
    width: int

    @classmethod
    def from_str(cls, s: str) -> Self:
        s = s.strip()
        plots: list[list[PlantVariant]] = []
        for y, line in enumerate(s.splitlines()):
            plots_in_row: list[PlantVariant] = []
            for x, c in enumerate(line):
                plots_in_row.append(PlantVariant(c))
            plots.append(plots_in_row)
            width = x + 1
        height = y + 1
        return cls(plots=plots, height=height, width=width)
    
    def points_reachable_from(self, pt: Point) -> set[Point]:
        reachable = set()
        if pt.x > 0:
            reachable.add(Point(pt.x - 1, pt.y))
        if pt.x < self.width - 1:
            reachable.add(Point(pt.x + 1, pt.y))
        if pt.y > 0:
            reachable.add(Point(pt.x, pt.y - 1))
        if pt.y < self.height - 1:
            reachable.add(Point(pt.x, pt.y + 1))
        return reachable
    
    def __getitem__(self, key: Point) -> PlantVariant:
        return self.plots[key.y][key.x]

    def to_farm(self) -> Farm:
        """Build a Farm object by grouping plots into regions."""
        uncovered = {Point(x, y) for y in range(self.height) for x in range(self.width)}
        regions: set[Region] = set()
        while len(uncovered) > 0:
            # Grab the first uncovered point and build from there.
            starting_plot = uncovered.pop()
            plant_variant = self[starting_plot]

            plots = {starting_plot}
            new_plots = plots
            while len(new_plots) > 0:
                reachable_from_last = {
                    reachable
                    for new_plot in new_plots
                    for reachable in self.points_reachable_from(new_plot)
                    if self[reachable] == plant_variant
                }
                # Only included plots we haven't covered yet.
                new_plots = reachable_from_last & uncovered
                # Update the set of still-uncovered plots.
                uncovered = uncovered.difference(new_plots)
                plots = plots.union(new_plots)
            new_region = Region(plant=plant_variant, plots=frozenset(plots))
            regions.add(new_region)

        return Farm(regions=frozenset(regions))