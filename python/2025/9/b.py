from itertools import combinations, pairwise
from typing import Self, Iterator
from heapq import heappop, heappush

from dataclasses import dataclass

@dataclass(frozen=True, order=True)
class Point:
    x: int
    y: int

    @classmethod
    def from_str(cls, s: str) -> Self:
        str_x, str_y = s.strip().split(',')
        return cls(x=int(str_x), y=int(str_y))

    def is_on_line(self, a: Self, b: Self):
        """
        Check if a point is on the line defined by (a, b)

        The line must be perfectly vertical or horizontal. Sorry.
        """
        # If the line is vertical.
        if a.x == b.x:
            if self.x != a.x:
                return False
            if a.y <= self.y <= b.y:
                return True
            if b.y <= self.y <= a.y:
                return True
            return False
        # If the line is horizontal.
        if a.y == b.y:
            if self.y != a.y:
                return False
            if a.x <= self.x <= b.x:
                return True
            if b.x <= self.x <= a.x:
                return True
            return False
        raise ValueError("these points aren't a horizontal or vertical line")


@dataclass(frozen=True, order=True)
class Rectangle:
    a: Point
    b: Point

    def area(self) -> int:
        height = abs(self.a.y - self.b.y) + 1
        width = abs(self.a.x - self.b.x) + 1
        return width * height
    
    def as_points(self) -> Iterator[Point]:
        """Get all the points that compose the rectangle."""
        xs = (self.a.x, self.b.x)
        ys = (self.a.y, self.b.y)
        min_x = min(*xs)
        max_x = max(*xs)
        min_y = min(*ys)
        max_y = max(*ys)
        for x in range(min_x, max_x+1):
            for y in range(min_y, max_y+1):
                yield Point(x, y)


@dataclass
class Polygon:
    points: list[Point]
    _max_y: int = -1

    def __post_init__(self):
        self._max_y = max(pt.y for pt in self.points)
    
    def vertices(self) -> Iterator[tuple[Point, Point]]:
        """Get all vertices around the Polygon."""
        for a, b in pairwise(self.points):
            yield (a, b)
        # The final point connects back to the first.
        yield self.points[-1], self.points[0]
        return
    
    def edges_contain_point(self, pt: Point) -> bool:
        """Check if a point is on one of the edges."""
        for a, b in self.vertices():
            if pt.is_on_line(a, b):
                return True
        return False
    
    def contains_point(self, pt: Point) -> bool:
        """Check if a point is inside the shape or on its border."""
        # Start by checking if the point is on the border.
        if self.edges_contain_point(pt):
            return True

        # If it's not on the border, maybe it's in the shape. We use ray-casting.
        # We'll ray-cast by just incrementing the y value.
        n_edge_crosses = 0

        # Perturbing the x-coord very slightly keeps us from weird cases where we trace
        # the border of the shape and double-count crossings.
        x = pt.x + 0.5
        y = pt.y

        while y <= (self._max_y + 1):
            if self.edges_contain_point(Point(x, y)):
                n_edge_crosses += 1
            y += 1
        return (n_edge_crosses % 2) ==1
    
    def contains_rectangle_corners(self, r: Rectangle) -> bool:
        """Check if a rectangle is fully contained in the polygon, including edges."""
        # corners = [r.a, r.b, Point(x=r.a.x, y=r.b.y), Point(x=r.b.x, y=r.a.y)]
        # we know that the rectangles defining-corners will be on the border of the
        # shape, because that's where they came from. So only check the other two.
        corners = [Point(x=r.a.x, y=r.b.y), Point(x=r.b.x, y=r.a.y)]
        for c in corners:
            if not self.contains_point(c):
                return False
        return True
    
    def contains_all_rectangle_points(self, r: Rectangle) -> bool:
        for pt in r.as_points():
            if not self.contains_point(pt):
                return False
        return True
    

def b(input: str) -> str:
    points = [Point.from_str(line) for line in input.splitlines()]
    shape = Polygon(points=points)

    # Find the biggest rectangles; order them in a heap.
    rectangle_areas: list[tuple[int, Rectangle]] = []
    for a, b in combinations(points, 2):
        rectangle = Rectangle(a, b)
        area = rectangle.area()
        heappush(rectangle_areas, (-area, rectangle))

    # Now start at the biggest and keep going until we find one entirely within the
    # polygon.
    while rectangle_areas:
        (area, rectangle) = heappop(rectangle_areas)
        print(f'Checking rect of size {-1 * area}')
        if shape.contains_rectangle_corners(rectangle):
            # If we pass the faster check, do the full check.
            if shape.contains_all_rectangle_points(rectangle):
                return str(area * -1)

    raise RuntimeError

