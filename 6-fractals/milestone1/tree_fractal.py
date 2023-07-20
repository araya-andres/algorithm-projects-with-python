import tkinter as tk
import math


class App:
    """Main class"""

    def __init__(self):
        # Make the tkinter window.
        self.window = tk.Tk()
        self.window.title("tree_fractal")
        self.window.protocol("WM_DELETE_WINDOW", self.kill_callback)
        self.window.geometry("300x350")

        outer_frame = tk.Frame(self.window)
        outer_frame.pack(padx=10, pady=(10, 0), fill=tk.X, expand=False)

        frame = tk.Frame(outer_frame)
        frame.pack(fill=tk.X, pady=(0, 4))
        label = tk.Label(frame, text="Angle 1:", width=7, anchor="w")
        label.pack(side="left")
        self.angle1_entry = tk.Entry(frame, width=4)
        self.angle1_entry.pack(side="left")
        self.angle1_entry.insert(0, "30")

        label = tk.Label(frame, text="Angle 2:", width=7, anchor="w")
        label.pack(side="left", padx=(20, 0))
        self.angle2_entry = tk.Entry(frame, width=4)
        self.angle2_entry.pack(side="left")
        self.angle2_entry.insert(0, "-30")

        frame = tk.Frame(outer_frame)
        frame.pack(fill=tk.X, pady=(0, 4))
        label = tk.Label(frame, text="Length:", width=7, anchor="w")
        label.pack(side="left")
        self.length_entry = tk.Entry(frame, width=4)
        self.length_entry.pack(side="left")
        self.length_entry.insert(0, "60")

        label = tk.Label(frame, text="Scale:", width=7, anchor="w")
        label.pack(side="left", padx=(20, 0))
        self.scale_entry = tk.Entry(frame, width=4)
        self.scale_entry.pack(side="left")
        self.scale_entry.insert(0, "0.75")

        label = tk.Label(frame, text="Depth:", width=7, anchor="w")
        label.pack(side="left", anchor="w", padx=(20, 0))
        self.depth_entry = tk.Entry(frame, width=4)
        self.depth_entry.pack(side="left")
        self.depth_entry.insert(0, "9")

        frame = tk.Frame(outer_frame)
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

        self.angle1_entry.focus_set()
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
        draw_branch(
            canvas=self.canvas,
            depth=int(self.depth_entry.get()),
            scale=float(self.scale_entry.get()),
            angle1=float(self.angle1_entry.get()),
            angle2=float(self.angle2_entry.get()),
            current_angle=90.0,
            current_length=float(self.length_entry.get()),
            current_x=self.canvas.winfo_width() // 2,
            current_y=self.canvas.winfo_height(),
        )


def draw_branch(
    canvas: tk.Canvas,
    depth: int,
    scale: float,
    angle1: float,
    angle2: float,
    current_angle: float,
    current_length: float,
    current_x: float,
    current_y: float,
):
    if depth <= 0:
        return
    angle = math.radians(current_angle)
    x = current_x + current_length * math.cos(angle)
    y = current_y - current_length * math.sin(angle)
    canvas.create_line(current_x, current_y, x, y)
    draw_branch(
        canvas,
        depth - 1,
        scale,
        angle1,
        angle2,
        current_angle + angle1,
        scale * current_length,
        x,
        y,
    )
    draw_branch(
        canvas,
        depth - 1,
        scale,
        angle1,
        angle2,
        current_angle + angle2,
        scale * current_length,
        x,
        y,
    )


App()
