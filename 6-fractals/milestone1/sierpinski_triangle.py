import math
import tkinter as tk


class App:
    """Main class"""

    def __init__(self):
        # Make the tkinter window.
        self.window = tk.Tk()
        self.window.title("sierpinski_triangle")
        self.window.protocol("WM_DELETE_WINDOW", self.kill_callback)
        self.window.geometry("300x350")

        outer_frame = tk.Frame(self.window)
        outer_frame.pack(padx=10, pady=(10, 0), fill=tk.X, expand=False)

        frame = tk.Frame(outer_frame)
        frame.pack(fill=tk.X, pady=(0, 4))
        label = tk.Label(frame, text="Depth:", width=7, anchor="w")
        label.pack(side="left", anchor="w", padx=(20, 0))
        self.depth_entry = tk.Entry(frame, width=4)
        self.depth_entry.pack(side="left")
        self.depth_entry.insert(0, "0")

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
        side = min(self.canvas.winfo_width(), self.canvas.winfo_height())
        height = math.sqrt(3) * side / 2
        x1 = self.canvas.winfo_width() / 2
        offset_y = (self.canvas.winfo_height() - height) / 2
        draw_sierpinski_triangle(
            canvas=self.canvas,
            depth=int(self.depth_entry.get()),
            x1=x1,
            y1=offset_y,
            x2=x1 - side / 2,
            y2=height + offset_y,
            x3=x1 + side / 2,
            y3=height + offset_y,
        )


def draw_sierpinski_triangle(
    canvas: tk.Canvas,
    depth: int,
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    x3: float,
    y3: float,
):
    if depth < 1:
        canvas.create_polygon([x1, y1, x2, y2, x3, y3], fill="black")
    else:
        draw_sierpinski_triangle(
            canvas,
            depth - 1,
            x1,
            y1,
            (x2 + x1) / 2,
            (y2 + y1) / 2,
            (x3 + x1) / 2,
            (y2 + y1) / 2,
        )
        draw_sierpinski_triangle(
            canvas, depth - 1, (x2 + x1) / 2, (y2 + y1) / 2, x2, y2, x1, y2
        )
        draw_sierpinski_triangle(
            canvas, depth - 1, (x3 + x1) / 2, (y2 + y1) / 2, x1, y3, x3, y3
        )


App()
