import tkinter as tk
from tkinter import filedialog, messagebox

import grantt_chart
import po_sorter


class App:
    # Create and manage the tkinter interface.
    def __init__(self):
        # Make the main interface.
        self.window = tk.Tk()
        self.window.title("draw_grantt_chart")
        self.window.protocol("WM_DELETE_WINDOW", self.kill_callback)
        self.window.geometry("630x400")

        # Build the menu.
        self.menubar = tk.Menu(self.window)
        self.menu_file = tk.Menu(self.menubar, tearoff=False)
        self.menu_file.add_command(
            label="Open...", command=self.open_po, accelerator="Ctrl+O"
        )
        self.menu_file.add_separator()
        self.menu_file.add_command(label="Exit", command=self.kill_callback)
        self.menubar.add_cascade(label="File", menu=self.menu_file)
        self.window.config(menu=self.menubar)

        # Build the canvas.
        self.canvas = tk.Canvas(
            self.window, borderwidth=2, relief=tk.SUNKEN, bg="white"
        )
        self.canvas.pack(padx=10, pady=(0, 10), fill=tk.BOTH, expand=True)

        self.window.bind("<Control-o>", self.ctrl_o_pressed)

        # Display the window.
        self.window.focus_force()
        self.window.mainloop()

    def kill_callback(self):
        self.window.destroy()

    def ctrl_o_pressed(self, event):
        self.open_po()

    def open_po(self):
        if filename := filedialog.askopenfilename(
            defaultextension=".po",
            filetypes=[("Partial Ordering", "*.po")],
            initialdir=".",
            title="Open Partial Ordering",
        ):
            tasks = po_sorter.load_po_file(filename)
            _ = po_sorter.build_pert_chart(tasks)
            self.canvas.delete("all")
            grantt_chart.draw(self.canvas, tasks)


if __name__ == "__main__":
    App()
