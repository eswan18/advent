from typing import Self, NewType
from dataclasses import dataclass
from itertools import combinations, pairwise

PlantVariant = NewType("PlantVariant", str)


@dataclass(frozen=True)
class BorderPoint:
    x: float
    y: float
    surrounds: 'Point'

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __repr__(self) -> str:
        return f"BorderPoint({self.x}, {self.y}, surrounds={self.surrounds})"


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"

    def touches(self, other: Self) -> bool:
        if self.x == other.x and abs(self.y - other.y) == 1:
            return True
        if self.y == other.y and abs(self.x - other.x) == 1:
            return True
        return False


@dataclass(frozen=True)
class Region:
    plant: PlantVariant
    plots: frozenset[Point]

    def area(self) -> int:
        return len(self.plots)

    def perimeter(self) -> int:
        # For every pair of points, if they touch, count 1 shared border.
        total_shared_borders = sum(
            int(pt_a.touches(pt_b)) for pt_a, pt_b in combinations(self.plots, 2)
        )
        total_borders = 4 * self.area() - 2 * total_shared_borders
        return total_borders

    def horizontal_borders(self) -> set[BorderPoint]:
        """Return all the horizontal borders this region has."""

        def pt_horizontal_borders(pt: Point) -> set[BorderPoint]:
            return {
                BorderPoint(pt.x, pt.y - 0.5, surrounds=pt),
                BorderPoint(pt.x, pt.y + 0.5, surrounds=pt),
        }

        borders = set()
        for pt in self.plots:
            # Using symmetric difference allows us to discard shared borders
            # (which are thus not borders at all).
            borders = borders.symmetric_difference(pt_horizontal_borders(pt))
        return borders

    def vertical_borders(self) -> set[BorderPoint]:
        """Return all the vertical borders this region has."""

        def pt_vertical_borders(pt: Point) -> set[BorderPoint]:
            return {
                BorderPoint(pt.x - 0.5, pt.y, surrounds=pt),
                BorderPoint(pt.x + 0.5, pt.y, surrounds=pt),
            }

        borders = set()
        for pt in self.plots:
            # Using symmetric difference allows us to discard shared borders
            # (which are thus not borders at all).
            borders = borders.symmetric_difference(pt_vertical_borders(pt))
        return borders

    def side_count(self) -> int:
        # Order the borders so we can easily see if they connect horizontally.
        horizontal_borders = sorted(self.horizontal_borders(), key=lambda b: (b.y, b.x))
        horizontal_side_count = 1
        for border_a, border_b in pairwise(horizontal_borders):
            x_offset = abs(border_a.x - border_b.x)
            if x_offset > 1:
                # We've hit a discontinuity in the side and will start a new one.
                horizontal_side_count += 1
                continue
            if border_a.y != border_b.y:
                # We've finished this horizontal edge entirely.
                horizontal_side_count += 1
                continue
            if x_offset == 1 and border_a.surrounds.y != border_b.surrounds.y:
                # This is a weird one: we're on the same horizontal line but a different side, as for A below.
                #   AAAAAA
                #   AAABBA
                #   AAABBA
                #   ABBAAA
                #   ABBAAA
                #   AAAAAA
                print(f'hor triggered on {self.plant}')
                print(border_a, border_b)
                horizontal_side_count += 1
                continue
        # Order the borders so we can easily see if they connect vertically.
        vertical_borders = sorted(self.vertical_borders(), key=lambda b: (b.x, b.y))
        vertical_side_count = 1
        for border_a, border_b in pairwise(vertical_borders):
            y_offset = abs(border_a.y - border_b.y)
            if y_offset > 1:
                vertical_side_count += 1
                continue
            if border_a.x != border_b.x:
                vertical_side_count += 1
                continue
            if y_offset == 1 and border_a.surrounds.x != border_b.surrounds.x:
                print(f'vert triggered on {self.plant}')
                print(border_a, border_b)
                vertical_side_count += 1
                continue
        return horizontal_side_count + vertical_side_count

    def price(self) -> int:
        return self.area() * self.perimeter()
    
    def price_by_sides(self) -> int:
        print(self.area(), self.side_count())
        return self.area() * self.side_count()


@dataclass
class Farm:
    regions: set[Region]

    def total_price(self) -> int:
        return sum(region.price() for region in self.regions)
    
    def total_price_by_sides(self) -> int:
        return sum(region.price_by_sides() for region in self.regions)

    def __str__(self) -> str:
        s = ""
        for region in self.regions:
            s += region.plant + ": "
            s += ", ".join(str(pt) for pt in region.plots)
            s += "\n"
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
