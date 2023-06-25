from PIL import Image, ImageTk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import simpledialog
import math
import tkinter as tk


# Fractal types.
MANDELBROT_SET = 0
JULIA_SET = 1
VORTEX_FRACTAL = 2


# Smoothing types.
SMOOTH_NOT = 0
SMOOTH_1 = 1
SMOOTH_2 = 2


MANDELBROT_BOUNDS = (-2.20, -1.2, 1.0, 1.2)
JULIA_BOUNDS = (-1.5, -1.5, 1.5, 1.5)
VORTEX_BOUNDS = (-1.5, -1.5, 2, 1.5)


# Define our colors as RGB tuples.
black   = (  0,   0,   0)
red     = (255,   0,   0)
orange  = (255, 128,   0)
yellow  = (255, 255,   0)
green   = (  0, 192,   0)
cyan    = (  0, 255, 255)
blue    = (  0,   0, 255)
fuchsia = (255,   0, 255)


class App:
    def __init__(self):
        # Define the drawing bounds.
        self.WXMIN, self.WYMIN, self.WXMAX, self.WYMAX = MANDELBROT_BOUNDS
        self.wxmin, self.wymin, self.wxmax, self.wymax = MANDELBROT_BOUNDS

        # Save a spot for the image.
        self.fractal_image = None

        # Set drawing parameters.
        self.max_iterations = 64
        self.z0 = 0 + 0j
        self.c0 = 0 - 1j
        self.max_magnitude = 2

        # Define the image's colors.
        self.colors = [black, red, orange, yellow, green, cyan, blue, fuchsia]
        self.num_colors = len(self.colors)

        # For smooth colors.
        self.log_escape = math.log(self.max_magnitude)

        # Make the main interface.
        self.window = tk.Tk()
        self.window.title('escape_fractals')
        self.window.protocol('WM_DELETE_WINDOW', self.kill_callback)
        self.window.geometry('300x300')

        # Build the menu.
        self.menubar = tk.Menu(self.window)

        self.menu_file = tk.Menu(self.menubar, tearoff=False)
        self.menu_file.add_command(label='Save As...', command=self.save_image, accelerator="Ctrl+S")
        self.menu_file.add_separator()
        self.menu_file.add_command(label='Exit', command=self.kill_callback)
        self.menubar.add_cascade(label='File', menu=self.menu_file)

        self.menu_settings = tk.Menu(self.menubar, tearoff=False)
        self.fractal_type = tk.IntVar(value=MANDELBROT_SET)
        self.menu_settings.add_radiobutton(label='Mandelbrot Set',
            variable=self.fractal_type, value=MANDELBROT_SET, command=self.changed_fractal)
        self.menu_settings.add_radiobutton(label='Julia Set',
            variable=self.fractal_type, value=JULIA_SET, command=self.changed_fractal)
        self.menu_settings.add_radiobutton(label='Vortex Fractal',
            variable=self.fractal_type, value=VORTEX_FRACTAL, command=self.changed_fractal)
        self.menu_settings.add_separator()
        self.smooth_type = tk.IntVar(value=SMOOTH_NOT)
        self.menu_settings.add_radiobutton(label='No Smoothing',
            variable=self.smooth_type, value=SMOOTH_NOT, command=self.changed_smooth_type)
        self.menu_settings.add_radiobutton(label='Smooth 1',
            variable=self.smooth_type, value=SMOOTH_1, command=self.changed_smooth_type)
        self.menu_settings.add_radiobutton(label='Smooth 2',
            variable=self.smooth_type, value=SMOOTH_2, command=self.changed_smooth_type)
        self.menu_settings.add_separator()
        self.menu_settings.add_command(label='Change Max Iterations', command=self.change_max_iterations)
        self.menubar.add_cascade(label='Settings', menu=self.menu_settings)
        
        self.menu_scale = tk.Menu(self.menubar, tearoff=False)
        self.menu_scale.add_command(label='Redraw', command=self.redraw)
        self.menu_scale.add_command(label='Scale x2', command=self.scale_2x)
        self.menu_scale.add_command(label='Scale x4', command=self.scale_4x)
        self.menu_scale.add_command(label='Scale x8', command=self.scale_8x)
        self.menu_scale.add_command(label='Full Scale', command=self.scale_full)
        self.menu_scale.add_separator()
        self.menu_scale.add_command(label='Enter Selected Area', command=self.enter_selected_area)
        self.menubar.add_cascade(label='Scale', menu=self.menu_scale)

        self.window.config(menu=self.menubar)

        # Bind menu accelerators.
        self.window.bind_all("<Control-s>", self.ctrl_s_pressed)
        self.window.bind_all("<Control-r>", self.ctrl_r_pressed)

        # Build the window surface.
        self.canvas = tk.Canvas(self.window, bg='white',
            borderwidth=2, relief=tk.SUNKEN, cursor="plus")
        self.canvas.pack(padx=10, pady=(0,10),
            side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self.mouse_down)

        self.window.update()
        self.redraw()

        # Display the window.
        self.window.focus_force()
        self.window.mainloop()

    def ctrl_r_pressed(self, event):
        self.redraw()

    def changed_fractal(self):
        # Change the selected fractal.
        if self.fractal_type.get() == MANDELBROT_SET:
            self.WXMIN, self.WYMIN, self.WXMAX, self.WYMAX = MANDELBROT_BOUNDS
        elif self.fractal_type.get() == JULIA_SET:
            self.WXMIN, self.WYMIN, self.WXMAX, self.WYMAX = JULIA_BOUNDS
        else:
            self.WXMIN, self.WYMIN, self.WXMAX, self.WYMAX = VORTEX_BOUNDS
        self.redraw()

    def redraw(self):
        # Redraw.
        self.draw_fractal(self.canvas)

    # Scale commands.
    def scale(self, factor):
        # Zoom out by a factor of factor.
        wid = (self.wxmax - self.wxmin) / 2 * factor
        hgt = (self.wymax - self.wymin) / 2 * factor
        cx = (self.wxmax + self.wxmin) / 2
        cy = (self.wymax + self.wymin) / 2
        self.wxmin = cx - wid
        self.wxmax = cx + wid
        self.wymin = cy - hgt
        self.wymax = cy + hgt
        self.redraw()

    def scale_2x(self):
        self.scale(2)

    def scale_4x(self):
        self.scale(4)

    def scale_8x(self):
        self.scale(8)

    def scale_full(self):
        # Reset the scale.
        self.wxmin = self.WXMIN
        self.wxmax = self.WXMAX
        self.wymin = self.WYMIN
        self.wymax = self.WYMAX
        self.redraw()

    def enter_selected_area(self):
        # Let the user enter the selected area textually.
        result = simpledialog.askstring('Enter Bounds',
            'Enter bounds (xmin, ymin, xmax, ymax):',
            parent=self.window)
        if not result: return None

        # Parse the selected text, which should be in the format xmin, ymin, xmax, ymax.
        try:
            self.wxmin, self.wymin, self.wxmax, self.wymax = [float(s) for s in result.split(',')]
        except Exception as e:
            messagebox.showinfo('Parse Error',
                f'Area bounds should have the format "xmin, ymin, xmax, ymax"\n{e}')
        self.redraw()

    def change_max_iterations(self):
        result = simpledialog.askstring('Max Iterations', 'Max Iterations',
            initialvalue=self.max_iterations, parent=self.window)
        if not result: return None

        self.max_iterations = int(result)
        self.redraw()

    def changed_smooth_type(self):
        # Change the smoothing type.
        self.redraw()

    def ctrl_s_pressed(self, event):
        self.save_image()

    def save_image(self):
        file_types = [
            ('PNG', '*.png'),
            ('JPG', '*.jpg'),
            ('BMP', '*.bmp'),
            ('GIF', '*.gif')]
        filename = filedialog.asksaveasfilename(
            defaultextension='.png', filetypes=file_types,
            initialdir='.',
            title="Save As")
        if not filename: return
        try:
            self.fractal_image.save(filename)
        except Exception as e:
            messagebox.showinfo('Error Saving Image', e)

    def select_area(self):
        # Get the selected area in pixels.
        x0, y0, x1, y1 = self.canvas.coords(self.selection_rectangle)

        # Make sure the area is at least one pixel wide and tall.
        if x1 <= x0: x1 = x0 + 1
        if y1 <= y0: y1 = y0 + 1

        # Calculate scale factors to convert into world coordinates.
        avail_wid = self.canvas.winfo_width()
        avail_hgt = self.canvas.winfo_height()
        scale_x = (self.wxmax - self.wxmin) / avail_wid
        scale_y = (self.wymax - self.wymin) / avail_hgt

        # Convert the selected area into world coordinates.
        wxmin = self.wxmin + x0 * scale_x
        wymin = self.wymin + y0 * scale_y
        wxmax = self.wxmin + x1 * scale_x
        wymax = self.wymin + y1 * scale_y

        self.wxmin, self.wymin, self.wxmax, self.wymax = wxmin, wymin, wxmax, wymax
        self.redraw()

    def draw_fractal(self,  canvas):
        self.canvas.delete(tk.ALL)
        self.canvas.update()

        # Create the new image.
        avail_wid = canvas.winfo_width()
        avail_hgt = canvas.winfo_height()
        self.fractal_image = Image.new(mode='RGB', size=(avail_wid, avail_hgt))
        pixels = self.fractal_image.load()

        # Adjust the selected area to match the canvas's size.
        self.adjust_aspect(avail_wid, avail_hgt)
        print(f'{self.wxmin}, {self.wymin}, {self.wxmax}, {self.wymax}')

        # Find scale factors to map pixels onto the selected area.
        dx = (self.wxmax - self.wxmin) / avail_wid
        dy = (self.wymax - self.wymin) / avail_hgt

        if self.fractal_type.get() == MANDELBROT_SET:
            self.draw_mandelbrot(pixels, avail_wid, avail_hgt, dx, dy)
        elif self.fractal_type.get() == JULIA_SET:
            self.draw_julia(pixels, avail_wid, avail_hgt, dx, dy)
        else:
            self.draw_vortex(pixels, avail_wid, avail_hgt, dx, dy)

        # Display the image on the canvas. 
        self.mandelbrot_photoimage = ImageTk.PhotoImage(self.fractal_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.mandelbrot_photoimage)

    def adjust_aspect(self, avail_wid, avail_hgt):
        # Enlarge (wxmin, wymin, wxmax, wymax) so it has the same aspect ratio as the canvas.
        wid = self.wxmax - self.wxmin
        hgt = self.wymax - self.wymin

        # Compare aspect ratios.
        if (wid / hgt > avail_wid / avail_hgt):
            # The area is too wide and short. Make it taller.
            hgt = wid / (avail_wid / avail_hgt)
            cy = (self.wymax + self.wymin) / 2
            self.wymin = cy - hgt / 2
            self.wymax = self.wymin + hgt
        else:
            # The area is too tall and thin. Make it wider.
            wid = hgt * (avail_wid / avail_hgt)
            cx = (self.wxmax + self.wxmin) / 2
            self.wxmin = cx - wid / 2
            self.wxmax = self.wxmin + wid

    def draw_mandelbrot(self, pixels, avail_wid, avail_hgt, dx, dy):
        for ix in range(avail_wid):
            for iy in range(avail_hgt):
                c = complex(self.wxmin + ix * dx, self.wymin + iy * dy)
                z = complex()
                step_num = 0
                while z.real**2 + z.imag**2 <= 4 and step_num < self.max_iterations:
                    z = z**2 + c
                    step_num += 1
                self.color_pixel(pixels, ix, iy, z, c, step_num)

    def draw_julia(self, pixels, avail_wid, avail_hgt, dx, dy):
        #c = -.1226 + .7449j # corabbit
        c = .4 - .325j
        for ix in range(avail_wid):
            for iy in range(avail_hgt):
                z = complex(self.wxmin + ix * dx, self.wymin + iy * dy)
                step_num = 0
                while z.real**2 + z.imag**2 <= 4 and step_num < self.max_iterations:
                    z = z**2 + c
                    step_num += 1
                self.color_pixel(pixels, ix, iy, z, c, step_num)

    def draw_vortex(self, pixels, avail_wid, avail_hgt, dx, dy):
        c = .6 - .9j
        for ix in range(avail_wid):
            for iy in range(avail_hgt):
                z0 = complex(self.wxmin + ix * dx, self.wymin + iy * dy)
                z1 = z0
                step_num = 0
                while step_num < self.max_iterations:
                    z = z1**2 + c.real + c.imag * z0
                    step_num += 1
                    if z.real**2 + z.imag**2 > 4: break
                    z0 = z1
                    z1 = z
                self.color_pixel(pixels, ix, iy, z, c, step_num)

    def color_pixel(self, pixels, ix, iy, z, c, step_num):
        pixels[ix, iy] = self.colors[step_num % self.num_colors] if self.smooth_type.get() == SMOOTH_NOT else self.smooth_color(z, c, step_num)

    def smooth_color(self, z, c, step_num):
        if step_num == self.max_iterations: return self.colors[0]
        for _ in range(3):
            z = z**2 + c
            step_num += 1
        mu = step_num + 1 - math.log(math.log(abs(z))) / self.log_escape
        if self.smooth_type.get() == SMOOTH_2:
            mu *= self.num_colors / self.max_iterations
        return self.mu_to_color(mu)

    def mu_to_color(self, mu):
        clr1 = int(mu)
        t2 = mu - clr1
        t1 = 1 - t2
        clr1 = clr1 % self.num_colors
        clr2 = (clr1 + 1) % self.num_colors

        r = int(self.colors[clr1][0] * t1 + self.colors[clr2][0] * t2)
        g = int(self.colors[clr1][1] * t1 + self.colors[clr2][1] * t2)
        b = int(self.colors[clr1][2] * t1 + self.colors[clr2][2] * t2)
        return (r, g, b)

    def kill_callback(self):
        """A callback to destroy the tkinter window."""
        self.window.destroy()

    def mouse_down(self, event):
        self.canvas.bind("<B1-Motion>", self.mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.mouse_up)
        self.drag_x0 = event.x
        self.drag_y0 = event.y
        self.drag_x1 = event.x
        self.drag_y1 = event.y
        self.selection_rectangle = self.canvas.create_rectangle(
            self.drag_x0, self.drag_y0,
            self.drag_x1, self.drag_y1,
            dash=(2,2), outline='white')

    def mouse_up(self, event):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.select_area()

    def mouse_drag(self, event):
        self.drag_x1 = event.x
        self.drag_y1 = event.y
        self.position_drag_rectangle()

    def position_drag_rectangle(self):
        x0 = min(self.drag_x0, self.drag_x1)
        y0 = min(self.drag_y0, self.drag_y1)
        x1 = max(self.drag_x0, self.drag_x1)
        y1 = max(self.drag_y0, self.drag_y1)
        self.canvas.coords(self.selection_rectangle, x0, y0, x1, y1)


App()