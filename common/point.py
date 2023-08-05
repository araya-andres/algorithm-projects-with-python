from __future__ import annotations


class Point:
    def __init__(self, x: float = 0.0, y: float = 0.0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __repr__(self):
        return "Point(%f, %f)" % (self.x, self.y)


def multiply(k: float, p: Point) -> Point:
    return Point(k * p.x, k * p.y)


def squared_distance(p: Point, q: Point) -> float:
    return (p.x - q.x) ** 2 + (p.y - q.y) ** 2
