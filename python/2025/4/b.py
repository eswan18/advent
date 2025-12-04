from dataclasses import dataclass

Point = tuple[int, int]


@dataclass
class Grid:
    width: int
    height: int
    paper: set[Point]

    def neighbors(self, p: Point, wraparound: bool = False) -> list[Point]:
        xs = [p[0] - 1, p[0], p[0] + 1]
        ys = [p[1] - 1, p[1], p[1] + 1]
        all_pts = [(x, y) for x in xs for y in ys]
        # Eliminate the original point
        all_pts = [pt for pt in all_pts if pt != p]
        # Eliminate boundary-crossing
        if not wraparound:
            all_pts = [pt for pt in all_pts if 0 <= pt[0] < self.width]
            all_pts = [pt for pt in all_pts if 0 <= pt[1] < self.height]
        else:
            # in theory we could allow negative indices as wraparounds but ... nope.
            raise NotImplementedError
        return all_pts

    @classmethod
    def from_str(cls, s: str) -> 'Grid':
        paper = set()
        for y, line in enumerate(s.splitlines()):
            height = y + 1
            width = len(line)
            for x, c in enumerate(line):
                if c == '@':
                    paper.add((x, y))
        return cls(width=width, height=height, paper=paper)

def try_remove(grid: Grid) -> set[Point]:
    accessible = set()
    for p in grid.paper:
        neighbors = grid.neighbors(p)
        paper_neighbors = [n for n in neighbors if n in grid.paper]
        if len(paper_neighbors) < 4:
            accessible.add(p)
    return accessible

def b(input: str) -> str:
    grid = Grid.from_str(input)
    total_removed = 0

    while True:
        removable = try_remove(grid)
        if len(removable) == 0:
            break
        total_removed += len(removable)
        grid.paper = grid.paper.difference(removable)

    return total_removed
