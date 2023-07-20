import tkinter as tk
import math


class App:
    """Main class"""

    def __init__(self):
        # Make the tkinter window.
        self.window = tk.Tk()
        self.window.title("koch_curve")
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
        draw_koch_curve(
            canvas=self.canvas,
            depth=int(self.depth_entry.get()),
            angle=0.0,
            length=float(self.canvas.winfo_width()),
            x0=0.0,
            y0=0.8 * self.canvas.winfo_height(),
        )


def draw_koch_curve(
    canvas: tk.Canvas, depth: int, angle: float, length: float, x0: float, y0: float
):
    if depth == 0:
        x = x0 + length * math.cos(angle)
        y = y0 - length * math.sin(angle)
        canvas.create_line(x0, y0, x, y)
    else:
        draw_koch_curve(
            canvas=canvas, depth=depth - 1, angle=angle, length=length / 3, x0=x0, y0=y0
        )

        draw_koch_curve(
            canvas=canvas,
            depth=depth - 1,
            angle=angle + math.pi / 3,
            length=length / 3,
            x0=x0 + length * math.cos(angle) / 3,
            y0=y0 - length * math.sin(angle) / 3,
        )

        x = length / 2
        y = length * math.sqrt(3) / 6
        draw_koch_curve(
            canvas=canvas,
            depth=depth - 1,
            angle=angle - math.pi / 3,
            length=length / 3,
            x0=x0 + (x * math.cos(angle) - y * math.sin(angle)),
            y0=y0 - (x * math.sin(angle) + y * math.cos(angle)),
        )

        draw_koch_curve(
            canvas=canvas,
            depth=depth - 1,
            angle=angle,
            length=length / 3,
            x0=x0 + 2 * length * math.cos(angle) / 3,
            y0=y0 - 2 * length * math.sin(angle) / 3,
        )


App()
