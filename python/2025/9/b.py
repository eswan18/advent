from itertools import combinations, pairwise
from typing import Self, Iterator
from heapq import heappop, heappush

from dataclasses import dataclass

@dataclass(frozen=True)
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


@dataclass(frozen=True)
class Rectangle:
    a: Point
    b: Point

    def area(self) -> int:
        height = abs(self.a.y - self.b.y) + 1
        width = abs(self.a.x - self.b.x) + 1
        return width * height


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
    
    def contains_rectangle(self, r: Rectangle) -> bool:
        """Check if a rectangle is fully contained in the polygon, including edges."""
        corners = [r.a, r.b, Point(x=r.a.x, y=r.b.y), Point(x=r.b.x, y=r.a.y)]
        for c in corners:
            if not self.contains_point(c):
                return False
        # If all the corners were in the shape, we have to do more... but we'll skip for now.
        return True




def b(input: str) -> str:
    points = [Point.from_str(line) for line in input.splitlines()]
    shape = Polygon(points=points)

    rectangles: list[tuple[int, Rectangle]] = []

    max_area = -1
    rect_in_question = None
    for a, b in combinations(points, 2):
        rectangle = Rectangle(a, b)
        if shape.contains_rectangle(rectangle):
            if rectangle.area() > max_area:
                max_area = rectangle.area()
                rect_in_question = rectangle

    print(max_area)
    print(rect_in_question)

