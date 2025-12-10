from itertools import combinations, pairwise
from typing import Self, Iterator, Protocol
from heapq import heappop, heappush
from functools import cache, cached_property

from dataclasses import dataclass

class HasEdges(Protocol):
    def edges(self) -> Iterator['Line']:
        ...

def intersects(a: HasEdges, b: HasEdges) -> bool:
    for a_edge in a.edges():
        for b_edge in b.edges():
            if a_edge.crosses(b_edge):
                return True
    return False

@dataclass(frozen=True, order=True)
class Point:
    x: int
    y: int

    @classmethod
    def from_str(cls, s: str) -> Self:
        str_x, str_y = s.strip().split(',')
        return cls(x=int(str_x), y=int(str_y))

    #@cache
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
    
    def line_between(self, other: Self) -> Iterator[Self]:
        """
        Get the points that compose the line between this and another point.
        
        The points must have the same x coordinate or y coordinate. Again, sorry.
        """
        if self.x == other.x:
            start_y = min(self.y, other.y)
            end_y = max(self.y, other.y)
            for y in range(start_y, end_y+1):
                yield Point(self.x, y)
        elif self.y == other.y:
            start_x = min(self.x, other.x)
            end_x = max(self.x, other.x)
            for x in range(start_x, end_x+1):
                yield Point(x, self.y)
        else:
            raise ValueError("these points aren't aligned horizontally or vertically.")


@dataclass(frozen=True)
class Line:
    a: Point
    b: Point

    def is_x_line(self) -> bool:
        return self.a.x == self.b.x
    
    def is_y_line(self) -> bool:
        return self.a.y == self.b.y
    
    def crosses(self, other: Self) -> bool:
        x_line = None
        y_line = None
        if self.is_x_line():
            x_line = self
        elif other.is_x_line():
            x_line = other
        if self.is_y_line():
            y_line = self
        elif other.is_y_line():
            y_line = other
        if x_line is None or y_line is None:
            return False # the lines aren't perpendicular

        min_x = min(y_line.a.x, y_line.b.x)
        max_x = max(y_line.a.x, y_line.b.x)
        min_y = min(x_line.a.y, x_line.b.y)
        max_y = max(x_line.a.y, x_line.b.y)
        return (
            min_x < x_line.a.x < max_x and
            min_y < y_line.a.y < max_y
        )

@dataclass(frozen=True, order=True)
class Rectangle:
    a: Point
    b: Point

    def area(self) -> int:
        height = abs(self.a.y - self.b.y) + 1
        width = abs(self.a.x - self.b.x) + 1
        return width * height
    
    def edges(self) -> Iterator[Line]:
        c1 = self.a
        c2 = Point(self.a.x, self.b.y)
        c3 = self.b
        c4 = Point(self.b.x, self.a.y)
        yield Line(c1, c2)
        yield Line(c2, c3)
        yield Line(c3, c4)
        yield Line(c4, c1)
    
    def corners(self) -> Iterator[Point]:
        yield self.a
        yield Point(self.a.x, self.b.y)
        yield self.b
        yield Point(self.b.x, self.a.y)

    

@dataclass(frozen=True)
class Polygon:
    points: tuple[Point]

    @cached_property
    def max_y(self):
        return max(pt.y for pt in self.points)
    
    def edges(self) -> Iterator[Line]:
        """Get all edges around the Polygon."""
        for a, b in pairwise(self.points):
            yield Line(a, b)
        # The final point connects back to the first.
        yield Line(self.points[-1], self.points[0])
        return
    
    def edges_contain_point(self, pt: Point) -> bool:
        """Check if a point is on one of the edges."""
        for line in self.edges():
            if pt.is_on_line(line.a, line.b):
                return True
        return False
    
    @cache
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

        while y <= (self.max_y + 1):
            if self.edges_contain_point(Point(x, y)):
                n_edge_crosses += 1
            y += 1
        return (n_edge_crosses % 2) ==1
    

def b(input: str) -> str:
    points = [Point.from_str(line) for line in input.splitlines()]
    shape = Polygon(points=tuple(points))

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
        if intersects(rectangle, shape):
            continue # The rectangle is partly-in, partly-out, of the shape.
        # If it doesn't intersect, it's either all-inside or all-outside the shape.
        # We have to check all four corners. I think.
        a, b, c, d = rectangle.corners()
        if not shape.contains_point(a):
            continue
        if not shape.contains_point(b):
            continue
        if not shape.contains_point(c):
            continue
        if not shape.contains_point(d):
            continue

        return str(area * -1)

