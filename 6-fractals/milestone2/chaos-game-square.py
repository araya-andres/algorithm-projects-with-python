from PIL import ImageTk, Image
import math
import random
import tkinter as tk

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

class App:
    def __init__(self):
        self.drawing = False
        
        # Make the tkinter window.
        self.window = tk.Tk()
        self.window.title('chaos_game_square')
        self.window.protocol('WM_DELETE_WINDOW', self.kill_callback)
        self.window.geometry('400x400')

        outer_frame = tk.Frame(self.window)
        outer_frame.pack(padx=10, pady=(10, 0), fill=tk.X, expand=False)

        frame = tk.Frame(outer_frame)
        frame.pack(fill=tk.X, pady=(0,4))

        label = tk.Label(frame, text='Restriction:', width=12, anchor='w')
        label.pack(side='left')

        options = [x for x in range(6)]
        self.restriction_entry = tk.IntVar()
        self.restriction_entry.set(options[1])
        tk.OptionMenu(frame, self.restriction_entry, *options).pack(side='left')

        frame.pack(fill=tk.X, pady=(0,4))
        self.start_stop_button = tk.Button(frame, text='Start', width=8, command=self.start_stop)
        self.start_stop_button.pack(padx=(20, 0), side='top')

        self.canvas = tk.Canvas(self.window, bg='white', borderwidth=2, relief=tk.SUNKEN)
        self.canvas.pack(padx=10, pady=(0, 10), fill=tk.BOTH, expand=True)

        # Make some shortcuts.
        self.window.bind_all("<Return>", self.do_start_stop)
        
        self.window.focus_force()
        self.window.mainloop()

    def kill_callback(self):
        '''A callback to destroy the tkinter window.'''
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
        self.restriction = self.restriction_entry.get()
        self.canvas.delete('all')

        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        self.scale = 0.9 * min(height, width)
        self.offset = Point((width - self.scale) / 2, (height - self.scale) / 2)
        self.num_dots = 0

        self.fractal_image= Image.new(mode='RGB', size=(width, height))
        self.pixels = self.fractal_image.load()

        self.points = [Point(0, 0), Point(0, 1), Point(1, 1), Point(1, 0)]
        for p in self.points:
            self.draw_dot(p)
        self.point = self.pick_initial_point()
        self.last_vertex = None
        self.last_vertex_count = 0
        self.draw_dots()

    def stop(self):
        self.drawing = False
        self.start_stop_button.config(text="Start")
        print(self.num_dots)

    def draw_dots(self):
        if not self.drawing: return
        for _ in range(100):
            v = self.pick_vertice()
            self.point = multiply(.5, self.point + v)
            self.draw_dot(self.point)
            if v == self.last_vertex:
                self.last_vertex_count += 1
            else:
                self.last_vertex_count = 1
                self.last_vertex = v
        self.photoimage = ImageTk.PhotoImage(self.fractal_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photoimage)
        self.window.after(10, self.draw_dots)

    def draw_dot(self, p: Point):
        q = multiply(self.scale, p) + self.offset
        self.pixels[q.x, q.y] = (128, 255, 128)
        self.num_dots += 1

    def pick_initial_point(self) -> Point:
        return Point(random.random(), random.random())

    def pick_vertice(self) -> Point:
        if self.restriction == 1:
            while True:
                v = random.choice(self.points)
                if v != self.last_vertex:
                    return v
        elif self.restriction == 2:
            l = len(self.points)
            while True:
                i = random.randrange(l)
                if self.points[(l + i - 1) % l] != self.last_vertex:
                    return self.points[i]
        elif self.restriction == 3:
            while True:
                v = random.choice(self.points)
                p = multiply(.5, self.point + v) - Point(.5, .5)
                if p.x**2 + p.y**2 > .01:
                    return v
        elif self.restriction == 4:
            l = len(self.points)
            while True:
                i = random.randrange(l)
                if (self.points[(l + i - 2) % l] != self.last_vertex and
                    self.points[(i + 2) % l] != self.last_vertex):
                    return self.points[i]
        elif self.restriction == 5:
            l = len(self.points)
            while True:
                i = random.randrange(l)
                v = self.points[i]
                if v != self.last_vertex and self.last_vertex_count > 1:
                    if ((self.points[(l + i - 1) % l] != self.last_vertex) and
                        (self.points[(i + 1) % l] != self.last_vertex)):
                        return v
                else:
                    return v
        else:
            return random.choice(self.points)

App()