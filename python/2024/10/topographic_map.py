from dataclasses import dataclass
from typing import Self

@dataclass(frozen=True)
class Point:
    x: int
    y: int

@dataclass
class TopographicMap:
    elevation: list[list[int]]
    width: int
    height: int

    @classmethod
    def from_str(cls, s: str) -> Self:
        lines = s.splitlines()
        return cls(
            elevation=[
                [int(p) for p in line] for line in s.splitlines()
            ],
            width=len(lines[0]),
            height=len(lines),
        )
    
    def __getitem__(self, index: Point) -> int:
        '''Implement coordinate lookup'''
        return self.elevation[index.y][index.x]
    
    def nadirs(self) -> list[Point]:
        pts = []
        for y, line in enumerate(self.elevation):
            for x, elev in enumerate(line):
                if elev == 0:
                    pts.append(Point(x, y))
        return pts
    
    def pts_reachable_from(self, pt: Point) -> set[Point]:
        reachable = set()
        if pt.x >= 1:
            reachable.add(Point(pt.x - 1, pt.y))
        if pt.x < self.width - 1:
            reachable.add(Point(pt.x + 1, pt.y))
        if pt.y >= 1:
            reachable.add(Point(pt.x, pt.y - 1))
        if pt.y < self.height - 1:
            reachable.add(Point(pt.x, pt.y + 1))
        return reachable
    
    def reachable_peaks(self, from_: Point) -> set[Point]:
        if self[from_] != 0:
            raise RuntimeError("Can't start from non-nadir")
        at_value = 0
        at_locations: set[Point] = {from_}
        while at_value < 9:
            next_at_value = at_value + 1
            next_at_locations = set()
            # For each point we're at, look for all reachable points from there that
            # have the elevation value we need.
            for pt in at_locations:
                for next_pt in self.pts_reachable_from(pt):
                    if self[next_pt] == next_at_value:
                        next_at_locations.add(next_pt)
            at_value = next_at_value
            at_locations = next_at_locations
        return next_at_locations
    
    def trailhead_score(self, pt: Point) -> int:
        if not self[pt] == 0:
            raise RuntimeError("Trailhead must be a nadir")
        return len(self.reachable_peaks(pt))