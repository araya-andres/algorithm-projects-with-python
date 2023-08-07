import tkinter as tk
from tkinter import filedialog, messagebox

import po_sorter


class App:
    # Create and manage the tkinter interface.
    def __init__(self):
        self.unordered_tasks = None

        # Make the main interface.
        self.window = tk.Tk()
        self.window.title("topological_sorting")
        self.window.protocol("WM_DELETE_WINDOW", self.kill_callback)
        self.window.geometry("400x300")

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

        # Build the item lists.
        frame = tk.Frame(self.window)
        frame.pack(padx=10, pady=(0, 10), side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(3, weight=1)
        frame.rowconfigure(1, weight=1)

        # Unsorted list.
        inner_frame = tk.Frame(frame)
        inner_frame.grid(row=1, column=1, padx=3, pady=3, sticky="nsew")
        inner_frame.columnconfigure(1, weight=1)
        inner_frame.rowconfigure(1, weight=1)
        self.unordered_list = tk.Listbox(inner_frame)
        self.unordered_list.grid(row=1, column=1, sticky="nsew")
        scrollbar = tk.Scrollbar(inner_frame)
        scrollbar.grid(row=1, column=2, sticky="nse")
        self.unordered_list.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.unordered_list.yview)

        # Sort button.
        sort_button = tk.Button(frame, text="Sort", width=6, command=self.sort)
        sort_button.grid(row=1, column=2, padx=3)

        # Sorted list.
        inner_frame = tk.Frame(frame)
        inner_frame.grid(row=1, column=3, padx=3, pady=3, sticky="nsew")
        inner_frame.columnconfigure(1, weight=1)
        inner_frame.rowconfigure(1, weight=1)
        self.ordered_list = tk.Listbox(inner_frame)
        self.ordered_list.grid(row=1, column=1, sticky="nsew")
        scrollbar = tk.Scrollbar(inner_frame)
        scrollbar.grid(row=1, column=2, sticky="nse")
        self.ordered_list.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.ordered_list.yview)

        self.window.bind("<Control-o>", self.ctrl_o_pressed)

        # Display the window.
        self.window.focus_force()
        self.window.mainloop()

    def kill_callback(self):
        self.window.destroy()

    def ctrl_o_pressed(self, _event):
        self.open_po()

    def open_po(self):
        if filename := filedialog.askopenfilename(
            defaultextension=".po",
            filetypes=[("Partial Ordering", "*.po")],
            initialdir=".",
            title="Open Partial Ordering",
        ):
            self.unordered_list.delete(0, "end")
            self.ordered_list.delete(0, "end")
            self.unordered_tasks = po_sorter.load_po_file(filename)
            self.unordered_list.insert("end", *self.unordered_tasks)

    def sort(self):
        if self.unordered_tasks:
            sorted_tasks = po_sorter.topo_sort(self.unordered_tasks)
            self.ordered_list.insert("end", *sorted_tasks)


if __name__ == "__main__":
    App()
