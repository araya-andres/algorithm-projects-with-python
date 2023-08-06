from .point import Point


class Turtle:
    def __init__(self):
        self.delta = [
            Point(0, 1),  # North
            Point(-1, 0),  # West
            Point(0, -1),  # South
            Point(1, 0),  # East
        ]
        self.idx = 0

    def turn(self, direction: str = "") -> None:
        if direction == "+":
            self.idx = (self.idx + 1) % len(self.delta)
        elif direction == "-":
            self.idx = (len(self.delta) + self.idx - 1) % len(self.delta)

    def forward(self) -> Point:
        return self.delta[self.idx]
