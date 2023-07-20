import tkinter as tk
import math


def get_string(n: int = 1) -> str:
    s = "a"
    for _ in range(n):
        s = s.replace("a", "+BF-AFA-FB+")
        s = s.replace("b", "-AF+BFB+FA-")
        s = s.lower()
    s = s.replace("a", "")
    s = s.replace("b", "")
    return s


class Point:
    def __init__(self, x: float = 0.0, y: float = 0.0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __repr__(self):
        return "Point(%i, %i)" % (self.x, self.y)


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


class App:
    """Main class"""

    def __init__(self):
        # Make the tkinter window.
        self.window = tk.Tk()
        self.window.title("hilbert_curve")
        self.window.protocol("WM_DELETE_WINDOW", self.kill_callback)
        self.window.geometry("300x350")

        outer_frame = tk.Frame(self.window)
        outer_frame.pack(padx=10, pady=(10, 0), fill=tk.X, expand=False)

        frame = tk.Frame(outer_frame)
        frame.pack(fill=tk.X, pady=(0, 4))
        label = tk.Label(frame, text="Depth:", width=7, anchor="w")
        label.pack(side="left")
        self.depth_entry = tk.Entry(frame, width=4)
        self.depth_entry.pack(side="left")
        self.depth_entry.insert(0, "0")

        frame.pack(fill=tk.X, pady=(0, 4))
        self.draw_button = tk.Button(
            frame, text="Draw", width=7, command=self.draw_curve
        )
        self.draw_button.pack(side="top")

        self.canvas = tk.Canvas(
            self.window, bg="white", borderwidth=2, relief=tk.SUNKEN
        )
        self.canvas.pack(padx=10, pady=(0, 10), fill=tk.BOTH, expand=True)

        # Make some shortcuts.
        self.window.bind_all("<Return>", self.return_pressed)

        self.depth_entry.focus_set()
        self.window.focus_force()
        self.window.mainloop()

    def kill_callback(self):
        """A callback to destroy the tkinter window."""
        self.window.destroy()

    def return_pressed(self, event):
        self.draw_curve()

    def draw_curve(self):
        # Remove any previous widgets.
        self.canvas.delete("all")
        draw_hilbert_curve(canvas=self.canvas, depth=int(self.depth_entry.get()))


def draw_hilbert_curve(canvas: tk.Canvas, depth: int):
    if depth < 1:
        return

    t = Turtle()
    points = [Point()]
    lowerLeft = Point()
    upperRight = Point()
    for c in get_string(depth):
        if c == "f":
            p = points[-1] + t.forward()
            points.append(p)
            lowerLeft.x = min(lowerLeft.x, p.x)
            lowerLeft.y = min(lowerLeft.y, p.y)
            upperRight.x = max(upperRight.x, p.x)
            upperRight.y = max(upperRight.y, p.y)
        else:
            t.turn(c)

    assert (
        -lowerLeft.x == upperRight.y
    )  # each curve is contained in a square with area 1
    assert lowerLeft.y == upperRight.x
    border = 10
    k = (min(canvas.winfo_width(), canvas.winfo_height()) - 2 * border) / upperRight.y
    offset_x = (canvas.winfo_width() - k * upperRight.y) / 2
    offset_y = (canvas.winfo_height() - k * upperRight.y) / 2
    for i in range(len(points) - 1):
        canvas.create_line(
            -k * points[i].x + offset_x,
            k * points[i].y + offset_y,
            -k * points[i + 1].x + offset_x,
            k * points[i + 1].y + offset_y,
        )


App()
