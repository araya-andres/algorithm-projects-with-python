import tkinter as tk
from tkinter import filedialog, messagebox

import common.serializer as serializer
from common.network import Network
from common.point import squared_distance


class App:
    # Create and manage the tkinter interface.
    def __init__(self):
        self.network = None

        # Make the main interface.
        self.window = tk.Tk()
        self.window.title("draw_network")
        self.window.protocol("WM_DELETE_WINDOW", self.kill_callback)
        self.window.geometry("300x300")

        # Build the menu.
        self.menubar = tk.Menu(self.window)
        self.menu_file = tk.Menu(self.menubar, tearoff=False)
        self.menu_file.add_command(
            label="Open...", command=self.open_network, accelerator="Ctrl+O"
        )
        self.menu_file.add_separator()
        self.menu_file.add_command(label="Exit", command=self.kill_callback)
        self.menubar.add_cascade(label="File", menu=self.menu_file)

        self.menu_options = tk.Menu(self.menubar, tearoff=False)
        self.shortest_path_algorithm = tk.IntVar(value=Network.LABEL_CORRECTING)
        self.menu_options.add_radiobutton(
            label="Label correcting",
            variable=self.shortest_path_algorithm,
            value=Network.LABEL_CORRECTING,
            command=self.check_for_path,
        )
        self.menu_options.add_radiobutton(
            label="Label setting",
            variable=self.shortest_path_algorithm,
            value=Network.LABEL_SETTING,
            command=self.check_for_path,
        )
        self.menubar.add_cascade(label="Options", menu=self.menu_options)

        self.window.config(menu=self.menubar)

        # Build the window surface.
        self.canvas = tk.Canvas(
            self.window, bg="white", borderwidth=2, relief=tk.SUNKEN
        )
        self.canvas.pack(
            padx=10, pady=(0, 10), side=tk.BOTTOM, fill=tk.BOTH, expand=True
        )
        self.window.bind("<Control-o>", self.ctrl_o_pressed)
        self.window.bind("<Button1-ButtonRelease>", self.select_start_node)
        self.window.bind("<Button3-ButtonRelease>", self.select_end_node)

        # Display the window.
        self.window.focus_force()
        self.window.mainloop()

    def kill_callback(self):
        self.window.destroy()

    def ctrl_o_pressed(self, event):
        self.open_network()

    def select_start_node(self, event):
        if self.network is None:
            return
        for node in self.network.nodes:
            if _was_selected(node, event):
                self.network.select_start_node(node)
                self.check_for_path()
                return

    def select_end_node(self, event):
        if self.network is None:
            return
        for node in self.network.nodes:
            if _was_selected(node, event):
                self.network.select_end_node(node)
                self.check_for_path()
                return

    def check_for_path(self):
        self.network.check_for_path(self.shortest_path_algorithm.get())
        self.draw_network()

    def open_network(self):
        if filename := filedialog.askopenfilename():
            try:
                self.network = serializer.load_from_file(filename)
                self.draw_network()
            except Exception as ex:
                messagebox.showinfo("", f"Could not open file '{filename}'\n{ex}")

    def draw_network(self):
        if self.network is not None:
            self.canvas.delete(tk.ALL)
            self.network.draw(self.canvas)


def _was_selected(node, event):
    return squared_distance(node.pos, event) <= node.radius**2


App()
