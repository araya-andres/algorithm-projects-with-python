import math
import random
import tkinter as tk

from PIL import Image, ImageTk

from common.point import Point, multiply


class App:
    def __init__(self):
        self.drawing = False

        # Make the tkinter window.
        self.window = tk.Tk()
        self.window.title("chaos_game")
        self.window.protocol("WM_DELETE_WINDOW", self.kill_callback)
        self.window.geometry("400x400")

        outer_frame = tk.Frame(self.window)
        outer_frame.pack(padx=10, pady=(10, 0), fill=tk.X, expand=False)

        frame = tk.Frame(outer_frame)
        frame.pack(fill=tk.X, pady=(0, 4))
        self.start_stop_button = tk.Button(
            frame, text="Start", width=8, command=self.start_stop
        )
        self.start_stop_button.pack(padx=(20, 0), side="top")

        self.canvas = tk.Canvas(
            self.window, bg="white", borderwidth=2, relief=tk.SUNKEN
        )
        self.canvas.pack(padx=10, pady=(0, 10), fill=tk.BOTH, expand=True)

        # Make some shortcuts.
        self.window.bind_all("<Return>", self.do_start_stop)

        self.window.focus_force()
        self.window.mainloop()

    def kill_callback(self):
        """A callback to destroy the tkinter window."""
        self.window.destroy()

    def do_start_stop(self, event):
        self.start_stop()

    def start_stop(self):
        if self.drawing:
            self.stop()
        else:
            self.start()

    def start(self):
        self.drawing = True
        self.start_stop_button.config(text="Stop")
        self.canvas.delete("all")

        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        self.scale = 0.9 * min(height, width)
        self.offset = Point((width - self.scale) / 2, (height - self.scale) / 2)
        self.num_dots = 0

        self.fractal_image = Image.new(mode="RGB", size=(width, height))
        self.pixels = self.fractal_image.load()

        h = math.sqrt(3) / 2
        self.points = [Point(0.0, h), Point(0.5, 0.0), Point(1.0, h)]
        for p in self.points:
            self.draw_dot(p)
        self.point = self.pick_initial_point()
        self.draw_dot(self.point)
        self.draw_dots()

    def stop(self):
        self.drawing = False
        self.start_stop_button.config(text="Start")
        print(self.num_dots)

    def draw_dots(self):
        if not self.drawing:
            return
        for _ in range(100):
            v = random.choice(self.points)
            self.point = multiply(0.5, self.point + v)
            self.draw_dot(self.point)
        self.photoimage = ImageTk.PhotoImage(self.fractal_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photoimage)
        self.window.after(10, self.draw_dots)

    def draw_dot(self, p: Point):
        q = multiply(self.scale, p) + self.offset
        self.pixels[q.x, q.y] = (128, 255, 128)
        self.num_dots += 1

    def pick_initial_point(self) -> Point:
        h = math.sqrt(3) / 2
        while True:
            p = Point(random.random(), random.random())
            if p.y < h and (
                (p.x < 0.5 and p.y > h * (1 - 2 * p.x))
                or (p.x > 0.5 and p.y > h * (2 * p.x - 1))
            ):
                return p


App()
