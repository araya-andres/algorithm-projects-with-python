import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

import serializer


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
        self.window.config(menu=self.menubar)

        # Build the window surface.
        self.canvas = tk.Canvas(
            self.window, bg="white", borderwidth=2, relief=tk.SUNKEN
        )
        self.canvas.pack(
            padx=10, pady=(0, 10), side=tk.BOTTOM, fill=tk.BOTH, expand=True
        )
        self.window.bind("<Control-o>", self.ctrl_o_pressed)

        # Display the window.
        self.window.focus_force()
        self.window.mainloop()

    def kill_callback(self):
        self.window.destroy()

    def ctrl_o_pressed(self, event):
        self.open_network()

    def open_network(self):
        if filename := tk.filedialog.askopenfilename():
            try:
                self.network = serializer.load_from_file(filename)
                self.draw_network()
            except Exception as ex:
                messagebox.showinfo("", f"Could not open file '{filename}'\n{ex}")

    def draw_network(self):
        if self.network is not None:
            self.canvas.delete(tk.ALL)
            self.network.draw(self.canvas)


App()
