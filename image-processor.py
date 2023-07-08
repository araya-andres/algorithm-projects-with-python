import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog, colorchooser
from PIL import ImageTk, Image, ImageFilter, ImageEnhance, ImageOps
import math


def array_from_list(lst, cols):
    return [lst[cols * i : cols * (i + 1)] for i in range(math.ceil(len(lst) / cols))]


def clamp(v, lo, hi):
    return max(lo, min(v, hi))


def get_integer(parent_window, title, prompt, default, min=None, max=None):
    # Let the user enter an integer.
    result = simpledialog.askstring(
        title, prompt, parent=parent_window, initialvalue=default
    )
    if not result:
        return None

    try:
        number = int(result)
    except Exception as e:
        messagebox.showinfo("Invalid Value", f"The value must be an integer.\n{e}")
        return None

    if (min != None) and (number < min):
        messagebox.showinfo("Invalid Value", f"The value must be at least {min}.")
        return None
    if (max != None) and (number > max):
        messagebox.showinfo("Invalid Value", f"The value must be at most {max}.")
        return None

    return number


def get_float(parent_window, title, prompt, default, min=None, max=None):
    # Let the user enter a float.
    result = simpledialog.askstring(
        title, prompt, parent=parent_window, initialvalue=default
    )
    if not result:
        return None

    try:
        number = float(result)
    except Exception as e:
        messagebox.showinfo("Invalid Value", f"The value must be a float.\n{e}")
        return None

    if (min != None) and (number < min):
        messagebox.showinfo("Invalid Value", f"The value must be at least {min}.")
        return None
    if (max != None) and (number > max):
        messagebox.showinfo("Invalid Value", f"The value must be at most {max}.")
        return None

    return number


def adjust_aspect(x0, y0, x1, y1, aspect_ratio):
    # Return (x1, y1) adjusted to fit the aspect ratio.
    width = abs(x1 - x0)
    height = abs(y1 - y0)

    # Do nothing if the height is zero.
    if height < 1:
        return x1, y1

    # See if we are too tall and thin or too short and wide.
    if width / height > aspect_ratio:
        # Too short and wide. Make it taller.
        height = width / aspect_ratio
    else:
        # Too tall and thin. Make it wider.
        width = height * aspect_ratio

    # Find the new values for x1 and x2.
    if x0 < x1:
        x1 = x0 + width
    else:
        x1 = x0 - width
    if y0 < y1:
        y1 = y0 + height
    else:
        y1 = y0 - height
    return x1, y1


class KernelDialog:
    def __init__(self, app, default_kernel, default_scale, default_offset):
        self.window = tk.Toplevel(app.window)
        self.window.title("Kernel")
        self.window.protocol("WM_DELETE_WINDOW", self.kill_callback)
        self.window.resizable(False, False)
        self.window.attributes("-topmost", "true")
        self.app = app

        # Make the entry area.
        outer_frame = tk.Frame(self.window)
        outer_frame.pack(padx=10, pady=10, expand="True")

        frame = tk.Frame(outer_frame)
        frame.pack(fill="x", side="top")
        label_text = "Enter 3x3 or 5x5 kernel values separated by commas."
        tk.Label(frame, text=label_text, anchor="w").pack(padx=5, pady=2, side="left")

        frame = tk.Frame(outer_frame)
        frame.pack(fill="x", side="top")
        self.kernel_text = tk.Text(frame, height=6, width=30)
        self.kernel_text.pack(padx=5, pady=2, side="left")
        self.kernel_text.insert(1.0, default_kernel)

        frame = tk.Frame(outer_frame)
        frame.pack(fill="x", side="top")
        tk.Label(frame, text="Scale:", width=8, anchor="w").pack(
            padx=5, pady=2, side="left"
        )
        self.scale_entry = tk.Entry(frame, width=6)
        self.scale_entry.pack(padx=5, pady=2, side="left")
        self.scale_entry.insert(0, default_scale)

        frame = tk.Frame(outer_frame)
        frame.pack(fill="x", side="top")
        tk.Label(frame, text="Offset:", width=8, anchor="w").pack(
            padx=5, pady=2, side="left"
        )
        self.offset_entry = tk.Entry(frame, width=6)
        self.offset_entry.pack(padx=5, pady=2, side="left")
        self.offset_entry.insert(0, default_offset)

        frame = tk.Frame(outer_frame)
        frame.pack(padx=(50, 0), pady=(10, 0), fill="both", side="right", expand="True")
        cancel_button = tk.Button(
            frame, text="Cancel", command=self.cancel, height=1, width=8
        )
        cancel_button.pack(padx=5, pady=2, side="right")
        ok_button = tk.Button(frame, text="OK", command=self.ok, height=1, width=8)
        ok_button.pack(padx=5, pady=2, side="right")

        self.scale_entry.bind("<Return>", self.return_pressed)
        self.offset_entry.bind("<Return>", self.return_pressed)
        self.window.bind("<Escape>", self.escape_pressed)

        self.window.grab_set()
        self.window.focus_force()
        self.is_running = True
        self.window.mainloop()
        if self.is_running:
            self.window.destroy()

    def kill_callback(self):
        self.is_running = False
        self.window.destroy()

    def return_pressed(self, event):
        self.ok()

    def ok(self):
        # Get the values.
        try:
            # Prepare the kernel.
            kernel = self.kernel_text.get("1.0", "end")
            kernel = kernel.replace("\n", ",")
            kernel = kernel.replace("\t", ",")
            kernel = kernel.replace(" ", ",")
            kernel = kernel.replace(";", ",")
            kernel = kernel.split(",")
            kernel = list(filter(None, kernel))
            kernel = list(map(int, kernel))
            width = int(math.sqrt(len(kernel)))
            if ((width != 3) and (width != 5)) or (width * width != len(kernel)):
                messagebox.showinfo(
                    "Kernel Error", f"The kernel must have dimension 3x3 or 5x5."
                )
                return
            size = (width, width)
        except Exception as e:
            messagebox.showinfo("Kernel Error", f"Invalid kernel.\n{e}")
            return

        try:
            scale = int(self.scale_entry.get())
        except Exception as e:
            messagebox.showinfo("Scale Error", f"Invalid scale.\n{e}")
            return

        try:
            offset = int(self.offset_entry.get())
        except Exception as e:
            messagebox.showinfo("Offset Error", f"Invalid offset.\n{e}")
            return

        # Make the app apply the kernel.
        self.app.apply_kernel(size, kernel, scale, offset)
        self.window.quit()

    def escape_pressed(self, event):
        self.cancel()

    def cancel(self):
        self.window.quit()


def prepare_pixels(image):
    # For the image, return:
    #     width
    #     height
    #     input pixels
    #     result image
    #     result image pixels
    width = image.width
    height = image.height
    input_pixels = image.load()
    result_image = Image.new(mode="RGB", size=(width, height))
    result_pixels = result_image.load()
    return width, height, input_pixels, result_image, result_pixels


def apply_func_to_pixels(image, func):
    # Apply a function to each of an image's pixels.
    width, height, input_pixels, result_image, result_pixels = prepare_pixels(image)
    for x in range(width):
        for y in range(height):
            r, g, b = input_pixels[x, y]
            result_pixels[x, y] = func(input_pixels[x, y])
    return result_image


def average_pixel(p):
    ave = int(sum(p) / 3)
    return (ave, ave, ave)


def grayscale_pixel(p):
    ave = int(0.3 * p[0] + 0.5 * p[1] + 0.2 * p[2])
    # ave = int(0.2126 * p[0] + 0.7152 * p[1] + 0.0722 * p[2])
    return (ave, ave, ave)


def sepia_pixel(p):
    r = int(p[0] * 0.393 + p[1] * 0.769 + p[2] * 0.189)
    g = int(p[0] * 0.349 + p[1] * 0.686 + p[2] * 0.168)
    b = int(p[0] * 0.272 + p[1] * 0.534 + p[2] * 0.131)
    return (r, g, b)


class App:
    def __init__(self):
        self.original_pil_image = None

        self.window = tk.Tk()
        self.window.title("Image Processor")
        self.window.protocol("WM_DELETE_WINDOW", self.kill_callback)
        self.window.geometry("600x600")

        # Build the menu.
        self.menubar = tk.Menu(self.window)

        self.menu_file = tk.Menu(self.menubar, tearoff=False)
        self.menu_file.add_command(
            label="Open...", command=self.open, accelerator="Ctrl+O"
        )
        self.menu_file.add_command(
            label="Save As...", command=self.save_as, accelerator="Ctrl+S"
        )
        self.menu_file.add_separator()
        self.menu_file.add_command(
            label="Reset", command=self.reset, accelerator="Ctrl+R"
        )
        self.menu_file.add_separator()
        self.menu_file.add_command(label="Montage...", command=self.montage)
        self.menu_file.add_separator()
        self.menu_file.add_command(label="Exit", command=self.kill_callback)
        self.menubar.add_cascade(label="File", menu=self.menu_file)

        self.menu_geometry = tk.Menu(self.menubar, tearoff=False)
        self.menu_geometry.add_command(label="Rotate...", command=self.rotate)
        self.menu_geometry.add_command(label="Scale...", command=self.scale)
        self.menu_geometry.add_command(label="Resize...", command=self.resize)
        self.menu_geometry.add_command(label="Stretch...", command=self.stretch)
        self.menu_geometry.add_command(label="Spread...", command=self.spread)
        self.menu_geometry.add_command(label="Transpose...", command=self.transpose)
        self.menu_geometry.add_command(label="Crop", command=self.crop)
        self.menu_geometry.add_command(
            label="Crop to Aspect...", command=self.crop_to_aspect
        )
        self.menubar.add_cascade(label="Geometry", menu=self.menu_geometry)

        self.menu_point_operations = tk.Menu(self.menubar, tearoff=False)
        self.menu_point_operations.add_command(label="Invert", command=self.invert)
        self.menu_point_operations.add_command(
            label="Color Cutoff...", command=self.color_cutoff
        )
        self.menu_point_operations.add_command(
            label="Clear Red", command=self.clear_red
        )
        self.menu_point_operations.add_command(
            label="Clear Green", command=self.clear_green
        )
        self.menu_point_operations.add_command(
            label="Clear Blue", command=self.clear_blue
        )
        self.menu_point_operations.add_command(label="Average", command=self.average)
        self.menu_point_operations.add_command(
            label="Grayscale", command=self.grayscale
        )
        self.menu_point_operations.add_command(label="Sepia Tone", command=self.sepia)
        self.menu_point_operations.add_command(
            label="Color Tone...", command=self.color_tone
        )
        self.menubar.add_cascade(
            label="Point Operations", menu=self.menu_point_operations
        )

        self.menu_enhancements = tk.Menu(self.menubar, tearoff=False)
        self.menu_enhancements.add_command(label="Color...", command=self.enhance_color)
        self.menu_enhancements.add_command(
            label="Contrast...", command=self.enhance_contrast
        )
        self.menu_enhancements.add_command(
            label="Brightness...", command=self.enhance_brightness
        )
        self.menu_enhancements.add_command(
            label="Sharpness...", command=self.enhance_sharpness
        )
        self.menubar.add_cascade(label="Enhancements", menu=self.menu_enhancements)

        self.menu_ops = tk.Menu(self.menubar, tearoff=False)
        self.menu_ops.add_command(label="Auto Contrast...", command=self.auto_contrast)
        self.menu_ops.add_command(label="Equalize", command=self.equalize)
        self.menubar.add_cascade(label="ImageOps", menu=self.menu_ops)

        self.menu_filters = tk.Menu(self.menubar, tearoff=False)
        self.menu_filters.add_command(label="Box Blur...", command=self.box_blur)
        self.menu_filters.add_command(
            label="Gaussian Blur...", command=self.gaussian_blur
        )
        self.menu_filters.add_command(
            label="Unsharp Mask...", command=self.unsharp_mask
        )
        self.menu_filters.add_command(label="Rank Filter...", command=self.rank_filter)
        self.menu_filters.add_command(
            label="Median Filter...", command=self.median_filter
        )
        self.menu_filters.add_command(label="Min Filter...", command=self.min_filter)
        self.menu_filters.add_command(label="Max Filter...", command=self.max_filter)
        self.menu_filters.add_command(label="Mode Filter...", command=self.mode_filter)
        self.menubar.add_cascade(label="Filters", menu=self.menu_filters)

        self.menu_custom_kernels = tk.Menu(self.menubar, tearoff=False)
        self.menu_custom_kernels.add_command(
            label="User Entered...", command=self.user_entered_kernel
        )
        self.menu_custom_kernels.add_command(
            label="Emboss...", command=self.emboss_kernel
        )
        self.menu_custom_kernels.add_command(
            label="Emboss 2...", command=self.emboss_kernel2
        )
        self.menu_custom_kernels.add_command(
            label="Gaussian 5x5...", command=self.gaussian_5x5
        )
        self.menu_custom_kernels.add_command(
            label="Box Blur 5x5...", command=self.box_blur_5x5
        )
        self.menu_custom_kernels.add_command(
            label="Edge Detector UL to LR...", command=self.edge_detection_ul_to_lr
        )
        self.menu_custom_kernels.add_command(
            label="Edge Detector Top to Bottom...", command=self.edge_detection_t_to_b
        )
        self.menu_custom_kernels.add_command(
            label="Edge Detector Left to Right...", command=self.edge_detection_l_to_r
        )
        self.menu_custom_kernels.add_command(
            label="High Pass 3x3...", command=self.high_pass_3x3
        )
        self.menubar.add_cascade(label="Custom Kernels", menu=self.menu_custom_kernels)

        self.menu_special = tk.Menu(self.menubar, tearoff=False)
        self.menu_special.add_command(label="Mandelbrot...", command=self.mandelbrot)
        self.menu_special.add_command(label="Noise...", command=self.noise)
        self.menu_special.add_command(
            label="Linear Gradient", command=self.linear_gradient
        )
        self.menu_special.add_command(
            label="Radial Gradient", command=self.radial_gradient
        )
        self.quantize_command = self.menu_special.add_command(
            label="Quantize", command=self.quantize
        )
        self.menubar.add_cascade(label="Special", menu=self.menu_special)

        # Set the main menu.
        self.window.config(menu=self.menubar)

        # Disable initially disabled menus.
        self.disable_menus()

        # Bind menu accelerators.
        self.window.bind_all("<Control-o>", self.ctrl_o_pressed)

        # Build the window surface.
        self.canvas = tk.Canvas(
            self.window, bg="white", borderwidth=2, relief=tk.SUNKEN
        )
        self.canvas.pack(
            padx=10, pady=(0, 10), side=tk.BOTTOM, fill=tk.BOTH, expand=True
        )

        # Display the window.
        self.window.focus_force()
        self.window.mainloop()

    def kill_callback(self):
        # Destroy the tkinter window.
        self.window.destroy()

    def disable_menus(self):
        # Disable menus that should not be enabled while no image is loaded.
        self.menu_file.entryconfig("Save As...", state="disabled")
        self.menu_file.entryconfig("Reset", state="disabled")
        self.menubar.entryconfig("Geometry", state="disabled")
        self.menubar.entryconfig("Point Operations", state="disabled")
        self.menubar.entryconfig("Enhancements", state="disabled")
        self.menubar.entryconfig("ImageOps", state="disabled")
        self.menubar.entryconfig("Filters", state="disabled")
        self.menubar.entryconfig("Custom Kernels", state="disabled")
        self.menu_special.entryconfig("Quantize", state="disabled")

    def enable_menus(self):
        # Enable menus that should be enabled when an image is loaded.
        self.menu_file.entryconfig("Save As...", state="normal")
        self.menu_file.entryconfig("Reset", state="normal")
        self.menubar.entryconfig("Geometry", state="normal")
        self.menubar.entryconfig("Point Operations", state="normal")
        self.menubar.entryconfig("Enhancements", state="normal")
        self.menubar.entryconfig("ImageOps", state="normal")
        self.menubar.entryconfig("Filters", state="normal")
        self.menubar.entryconfig("Custom Kernels", state="normal")
        self.menu_special.entryconfig("Quantize", state="normal")
        self.window.bind_all("<Control-s>", self.ctrl_s_pressed)
        self.window.bind_all("<Control-r>", self.ctrl_r_pressed)

    def show_current_image(self):
        self.current_tk_image = ImageTk.PhotoImage(self.current_pil_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.current_tk_image)

    # File menu.
    def ctrl_o_pressed(self, event):
        self.open()

    def open(self):
        if fname := tk.filedialog.askopenfilename():
            MODE = "RGB"
            self.original_pil_image = Image.open(fname)
            if self.original_pil_image.mode != MODE:
                self.original_pil_image = self.original_pil_image.convert(mode=MODE)
            self.reset()
            self.enable_menus()

    def ctrl_s_pressed(self, event):
        self.save_as()

    def save_as(self):
        if fname := tk.filedialog.asksaveasfilename(defaultextension=".png"):
            self.current_pil_image.save(fname)

    def ctrl_r_pressed(self, event):
        self.reset()

    def reset(self):
        self.current_pil_image = self.original_pil_image.copy()
        self.show_current_image()

    def montage(self):
        if filenames := tk.filedialog.askopenfilenames():
            self.make_montage(filenames)

    def make_montage(self, filenames):
        # Make a montage of files, four per row.
        COLS = 4
        image_arr = [Image.open(f) for f in filenames]
        sz = (
            max(sum(w) for w in array_from_list([i.size[0] for i in image_arr], COLS)),
            sum(max(h) for h in array_from_list([i.size[1] for i in image_arr], COLS)),
        )
        self.original_pil_image = Image.new(mode="RGB", size=sz)
        y = 0
        for row in array_from_list(image_arr, COLS):
            x = 0
            max_height = 0
            for img in row:
                self.original_pil_image.paste(img, box=(x, y))
                x += img.size[0]
                max_height = max(max_height, img.size[1])
            y += max_height
        self.reset()
        self.enable_menus()

    # Geometry menu.
    def rotate(self):
        if angle := get_integer(self.window, "Rotate", "Degrees:", "30"):
            self.current_pil_image = self.current_pil_image.rotate(angle)
            self.show_current_image()

    def scale(self):
        if factor := get_float(self.window, "Scale", "Factor:", "1", 0.01, 100):
            w, h = self.current_pil_image.size
            self.__resize(w * factor, h * factor)

    def resize(self):
        w, h = self.current_pil_image.size
        if new_w := get_integer(self.window, "Resize", "Width:", w, 10, 1000):
            aspect_ratio = w / h
            self.__resize(new_w, new_w / aspect_ratio)

    def stretch(self):
        if s := simpledialog.askstring("Stretch", "Size", parent=self.window):
            try:
                self.__resize(*[int(x) for x in s.split(",")])
            except Exception as ex:
                print(ex)

    def __resize(self, w, h):
        self.current_pil_image = self.current_pil_image.resize(size=(int(w), int(h)))
        self.show_current_image()

    def spread(self):
        if spread_val := get_integer(self.window, "Spread", "Value:", 5):
            self.current_pil_image = self.current_pil_image.effect_spread(spread_val)
            self.show_current_image()

    def transpose(self):
        msg = "1) Flip Left/Right\n2) Flip Top/Bottom\n3) Rotate 90\n4) Rotate 180\n5) Rotate 270"
        if idx := get_integer(self.window, "Transpose", msg, 1, 1, 5):
            ops = (
                Image.FLIP_LEFT_RIGHT,
                Image.FLIP_TOP_BOTTOM,
                Image.ROTATE_90,
                Image.ROTATE_180,
                Image.ROTATE_270,
            )
            self.current_pil_image = self.current_pil_image.transpose(ops[idx - 1])
            self.show_current_image()

    def crop(self, aspect_ratio=None):
        self.aspect_ratio = aspect_ratio
        self.canvas.config(cursor="tcross")
        self.canvas.bind("<Button-1>", self.mouse_down)

    def crop_to_aspect(self):
        if aspect_ratio := get_float(
            self.window, "Crop to aspect", "Aspect ratio:", "1.333", min=0.1, max=5
        ):
            self.crop(aspect_ratio)

    def mouse_down(self, event):
        self.canvas.unbind("<Button-1>")
        self.canvas.bind("<B1-Motion>", self.mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.mouse_up)
        self.drag_x0 = self.drag_x1 = event.x
        self.drag_y0 = self.drag_y1 = event.y
        self.selection_rectangle = self.canvas.create_rectangle(
            self.drag_x0,
            self.drag_y0,
            self.drag_x1,
            self.drag_y1,
            dash=(2, 2),
            outline="white",
        )

    def mouse_drag(self, event):
        if self.aspect_ratio:
            self.drag_x1, self.drag_y1 = adjust_aspect(
                self.drag_x0,
                self.drag_y0,
                event.x,
                event.y,
                self.aspect_ratio,
            )
        else:
            self.drag_x1 = clamp(event.x, 0, self.current_tk_image.width())
            self.drag_y1 = clamp(event.y, 0, self.current_tk_image.height())
        self.canvas.coords(
            self.selection_rectangle,
            self.drag_x0,
            self.drag_y0,
            self.drag_x1,
            self.drag_y1,
        )

    def mouse_up(self, event):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.config(cursor="")
        self.current_pil_image = self.current_pil_image.crop(
            (
                min(self.drag_x0, self.drag_x1),
                min(self.drag_y0, self.drag_y1),
                max(self.drag_x0, self.drag_x1),
                max(self.drag_y0, self.drag_y1),
            )
        )
        self.show_current_image()

    # Point Operations menu.
    def invert(self):
        self.current_pil_image = Image.eval(self.current_pil_image, lambda x: 255 - x)
        self.show_current_image()

    def color_cutoff(self):
        if val := get_integer(self.window, "Color cutoff", "Value", 100, 0, 255):
            self.current_pil_image = Image.eval(
                self.current_pil_image, lambda x: 0 if x < val else 255
            )
            self.show_current_image()

    def clear_red(self):
        self.current_pil_image = apply_func_to_pixels(
            self.current_pil_image, lambda px: (0, px[1], px[2])
        )
        self.show_current_image()

    def clear_green(self):
        self.current_pil_image = apply_func_to_pixels(
            self.current_pil_image, lambda px: (px[0], 0, px[2])
        )
        self.show_current_image()

    def clear_blue(self):
        self.current_pil_image = apply_func_to_pixels(
            self.current_pil_image, lambda px: (px[0], px[1], 0)
        )
        self.show_current_image()

    def average(self):
        self.current_pil_image = apply_func_to_pixels(
            self.current_pil_image, average_pixel
        )
        self.show_current_image()

    def grayscale(self):
        self.current_pil_image = apply_func_to_pixels(
            self.current_pil_image, grayscale_pixel
        )
        self.show_current_image()

    def sepia(self):
        self.current_pil_image = apply_func_to_pixels(
            self.current_pil_image, sepia_pixel
        )
        self.show_current_image()

    def color_tone(self):
        if c := colorchooser.askcolor():
            width, height, input_pixels, result_image, result_pixels = prepare_pixels(
                self.current_pil_image
            )
            for x in range(width):
                for y in range(height):
                    brightness = sum(input_pixels[x, y]) / (3 * 255)
                    result_pixels[x, y] = tuple(int(brightness * x) for x in c[0])
            self.current_pil_image = result_image
            self.show_current_image()

    # Enhancements menu.
    def enhance_color(self):
        if factor := get_float(self.window, "Enhance Color", "Factor", "1.0"):
            new_img = ImageEnhance.Color(self.current_pil_image)
            self.current_pil_image = new_img.enhance(factor)
            self.show_current_image()

    def enhance_contrast(self):
        if factor := get_float(self.window, "Enhance Contrast", "Factor", "1.0"):
            new_img = ImageEnhance.Contrast(self.current_pil_image)
            self.current_pil_image = new_img.enhance(factor)
            self.show_current_image()

    def enhance_brightness(self):
        if factor := get_float(self.window, "Enhance Brightness", "Factor", "1.0"):
            new_img = ImageEnhance.Brightness(self.current_pil_image)
            self.current_pil_image = new_img.enhance(factor)
            self.show_current_image()

    def enhance_sharpness(self):
        if factor := get_float(self.window, "Enhance Sharpness", "Factor", "1.0"):
            new_img = ImageEnhance.Sharpness(self.current_pil_image)
            self.current_pil_image = new_img.enhance(factor)
            self.show_current_image()

    # ImageOps menu.
    def auto_contrast(self):
        if cutoff := get_integer(self.window, "Auto Contrast", "Cutoff", "1", 0, 49):
            self.current_pil_image = ImageOps.autocontrast(
                self.current_pil_image, cutoff
            )
            self.show_current_image()

    def equalize(self):
        self.current_pil_image = ImageOps.equalize(self.current_pil_image)
        self.show_current_image()

    # Filters menu.
    def box_blur(self):
        if r := get_integer(self.window, "Box Blur", "Radius", "3", 0):
            filter = ImageFilter.BoxBlur(r)
            self.current_pil_image = self.current_pil_image.filter(filter)
            self.show_current_image()

    def gaussian_blur(self):
        if r := get_integer(self.window, "Gaussian Blur", "Radius", "3", 0):
            filter = ImageFilter.GaussianBlur(r)
            self.current_pil_image = self.current_pil_image.filter(filter)
            self.show_current_image()

    def unsharp_mask(self):
        if s := simpledialog.askstring(
            "Unsharp Mask", "Radius,Percent,Threshold", parent=self.window
        ):
            radius, percent, threshold = s.split(",")
            filter = ImageFilter.UnsharpMask(
                float(radius), int(percent), int(threshold)
            )
            self.current_pil_image = self.current_pil_image.filter(filter)
            self.show_current_image()

    def rank_filter(self):
        if s := simpledialog.askstring("Rank Filter", "Size,Rank", parent=self.window):
            size, rank = [int(x) for x in s.split(",")]
            if size % 2 == 0:
                print("Size must be odd")
                return
            filter = ImageFilter.RankFilter(size, rank)
            self.current_pil_image = self.current_pil_image.filter(filter)
            self.show_current_image()

    def median_filter(self):
        self.__filter_helper("Median Filter", ImageFilter.MedianFilter)

    def min_filter(self):
        self.__filter_helper("Median Filter", ImageFilter.MinFilter)

    def max_filter(self):
        self.__filter_helper("Max Filter", ImageFilter.MaxFilter)

    def mode_filter(self):
        self.__filter_helper("Mode Filter", ImageFilter.ModeFilter)

    def __filter_helper(self, window_title: str, filter):
        if size := get_integer(self.window, window_title, "Size", "3", 3):
            if size % 2 == 0:
                print("size must be odd")
                return
            self.current_pil_image = self.current_pil_image.filter(filter(size))
            self.show_current_image()

    # Custom Kernels menu.
    def user_entered_kernel(self):
        KernelDialog(
            self,
            default_kernel="1, 1, 1\n1, 1, 1\n1, 1, 1",
            default_scale=9,
            default_offset=0,
        )

    def emboss_kernel(self):
        pass

    def emboss_kernel2(self):
        pass

    def gaussian_5x5(self):
        pass

    def box_blur_5x5(self):
        pass

    def edge_detection_ul_to_lr(self):
        pass

    def edge_detection_t_to_b(self):
        pass

    def edge_detection_l_to_r(self):
        pass

    def high_pass_3x3(self):
        pass

    def apply_kernel(self, size, kernel, scale, offset):
        filter = ImageFilter.Kernel(size, kernel, scale, offset)
        self.current_pil_image = self.current_pil_image.filter(filter)
        self.show_current_image()

    # Special menu.
    def mandelbrot(self):
        pass

    def noise(self):
        pass

    def linear_gradient(self):
        pass

    def radial_gradient(self):
        pass

    def quantize(self):
        pass


App()
