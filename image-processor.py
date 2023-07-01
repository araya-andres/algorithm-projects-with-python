import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog, colorchooser
from PIL import ImageTk, Image, ImageFilter, ImageEnhance, ImageOps
import math


def get_integer(parent_window, title, prompt, default, min, max):
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


def get_float(parent_window, title, prompt, default, min, max):
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
            kernel = list(map(float, kernel))
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
            self.original_pil_image = Image.open(fname)
            self.current_pil_image = self.original_pil_image # FIXME
            self.show_current_image()
            self.enable_menus()

    def ctrl_s_pressed(self, event):
        self.save_as()

    def save_as(self):
        pass

    def ctrl_r_pressed(self, event):
        self.reset()

    def reset(self):
        pass

    def montage(self):
        pass

    def make_montage(self, filenames):
        # Make a montage of files, four per row.
        pass

    # Geometry menu.
    def rotate(self):
        pass

    def scale(self):
        pass

    def resize(self):
        pass

    def stretch(self):
        pass

    def spread(self):
        pass

    def transpose(self):
        pass

    def crop(self):
        pass

    def crop_to_aspect(self):
        pass

    def mouse_down(self, event):
        pass

    def mouse_drag(self, event):
        pass

    def mouse_up(self, event):
        pass

    # Point Operations menu.
    def invert(self):
        pass

    def color_cutoff(self):
        pass

    def clear_red(self):
        pass

    def clear_green(self):
        pass

    def clear_blue(self):
        pass

    def average(self):
        pass

    def grayscale(self):
        pass

    def sepia(self):
        pass

    def color_tone(self):
        pass

    # Enhancements menu.
    def enhance_color(self):
        pass

    def enhance_contrast(self):
        pass

    def enhance_brightness(self):
        pass

    def enhance_sharpness(self):
        pass

    # ImageOps menu.
    def auto_contrast(self):
        pass

    def equalize(self):
        pass

    # Filters menu.
    def box_blur(self):
        pass

    def gaussian_blur(self):
        pass

    def unsharp_mask(self):
        pass

    def rank_filter(self):
        pass

    def median_filter(self):
        pass

    def min_filter(self):
        pass

    def max_filter(self):
        pass

    def mode_filter(self):
        pass

    # Custom Kernels menu.
    def user_entered_kernel(self):
        pass

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
        # print('apply_kernel')
        # print(f'  size:{size}')
        # print(f'  kernel:{kernel}')
        # print(f'  scale:{scale}')
        # print(f'  offset:{offset}')
        pass

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
