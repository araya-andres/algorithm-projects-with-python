from __future__ import annotations
from tkinter import messagebox
from tkinter import simpledialog
from typing import Optional, Tuple
import tkinter as tk


class SortedBinaryNode:
    indent = "  "
    radius = 10  # Radius of a node’s circle
    x_spacing = 20  # Horizontal distance between neighboring subtrees
    y_spacing = 20  # Vertical distance between parent and child subtrees

    def __init__(self, value):
        self.value = value
        self.left_child = None
        self.right_child = None

    def add_node(self, child: SortedBinaryNode) -> None:
        pass

    def is_leaf(self) -> bool:
        return self.left_child is None and self.right_child is None

    def find_node(self, value) -> Optional[SortedBinaryNode]:
        pass

    def pop(self, target):
        pass

    def traverse_preorder(self):
        yield self
        if self.left_child:
            yield from self.left_child.traverse_preorder()
        if self.right_child:
            yield from self.right_child.traverse_preorder()

    def traverse_inorder(self):
        if self.left_child:
            yield from self.left_child.traverse_inorder()
        yield self
        if self.right_child:
            yield from self.right_child.traverse_inorder()

    def traverse_postorder(self):
        if self.left_child:
            yield from self.left_child.traverse_postorder()
        if self.right_child:
            yield from self.right_child.traverse_postorder()
        yield self

    def traverse_breadth_first(self):
        queue = [self]
        while queue:
            node = queue.pop(0)
            yield node
            if node.left_child:
                queue.append(node.left_child)
            if node.right_child:
                queue.append(node.right_child)

    def __str__(self, level=0) -> str:
        s = f"{SortedBinaryNode.indent * level}{self.value}:"
        if self.left_child:
            s += f"\n{self.left_child.__str__(level + 1)}"
        if self.right_child:
            s += f"\n{self.right_child.__str__(level + 1)}"
        return s

    def arrange_subtree(
        self, xmin: float, ymin: float
    ) -> Tuple[float, float, float, float]:
        r = SortedBinaryNode.radius
        cy = r + ymin

        if self.is_leaf():
            cx = r + xmin
            self.center = (cx, cy)
            self.subtree_bounds = (cx - r, cy - r, cx + r, cy + r)
            return self.subtree_bounds

        child_ymin = SortedBinaryNode.y_spacing + cy + r

        if self.left_child and self.right_child:
            xl0, yl0, xl1, yl1 = self.left_child.arrange_subtree(xmin, child_ymin)
            w = xl1 - xl0 + SortedBinaryNode.x_spacing
            xr0, yr0, xr1, yr1 = self.right_child.arrange_subtree(xmin + w, child_ymin)
            w = w + xr1 - xr0
            self.center = (xmin + w / 2, cy)
            self.subtree_bounds = (
                xmin,
                ymin,
                xmin + w,
                child_ymin + max(yl1 - yl0, yr1 - yr0),
            )
        else:
            child = self.left_child if self.left_child else self.right_child
            x0, y0, x1, y1 = child.arrange_subtree(xmin, child_ymin)
            self.center = ((x0 + x1) / 2, cy)
            self.subtree_bounds = (x0, ymin, x1, child_ymin + y1 - y0)

        return self.subtree_bounds

    def draw_subtree_links(self, canvas: tk.Canvas) -> None:
        if self.left_child:
            canvas.create_line(*self.center, *self.left_child.center)
            self.left_child.draw_subtree_links(canvas)
        if self.right_child:
            canvas.create_line(*self.center, *self.right_child.center)
            self.right_child.draw_subtree_links(canvas)

    def draw_subtree_nodes(self, canvas: tk.Canvas) -> None:
        cx, cy = self.center
        r = SortedBinaryNode.radius
        canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill="white")
        canvas.create_text(cx, cy, text=str(self.value))
        if self.left_child:
            self.left_child.draw_subtree_nodes(canvas)
        if self.right_child:
            self.right_child.draw_subtree_nodes(canvas)
        # Outline the subtree for debugging.
        canvas.create_rectangle(self.subtree_bounds, fill="", outline="red")

    def arrange_and_draw_subtree(
        self, canvas: tk.Canvas, xmin: float, ymin: float
    ) -> None:
        self.arrange_subtree(xmin, ymin)
        self.draw_subtree_links(canvas)
        self.draw_subtree_nodes(canvas)


class App:
    def __init__(self):
        # Make a sentinel root.
        self.root = SortedBinaryNode(-1)
        self.run_tests()

        # Make the tkinter window.
        self.window = tk.Tk()
        self.window.title("SortedBinaryNode")
        self.window.protocol("WM_DELETE_WINDOW", self.kill_callback)
        self.window.geometry("290x320")

        frame = tk.Frame(self.window)
        frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.value_entry = tk.Entry(frame, width=3)
        self.value_entry.pack(padx=(10, 0), side="left")
        self.value_entry.focus_set()

        self.add_button = tk.Button(frame, text="Add", width=8, command=self.add_value)
        self.add_button.pack(padx=(10, 0), side="left")

        self.pop_button = tk.Button(frame, text="Pop", width=8, command=self.pop_value)
        self.pop_button.pack(padx=(10, 0), side="left")

        self.find_button = tk.Button(
            frame, text="Find", width=8, command=self.find_value
        )
        self.find_button.pack(padx=(10, 0), side="left")

        self.canvas = tk.Canvas(
            self.window, bg="white", borderwidth=2, relief=tk.SUNKEN
        )
        self.canvas.pack(padx=10, pady=(0, 10), fill=tk.BOTH, expand=True)

        # Make some shortcuts.
        self.window.bind_all("<Control-a>", self.ctrl_a_pressed)
        self.window.bind_all("<Control-p>", self.ctrl_p_pressed)
        self.window.bind_all("<Control-f>", self.ctrl_f_pressed)

        # Draw the initial tree.
        self.draw_tree()

        self.window.focus_force()
        self.window.mainloop()

    def kill_callback(self):
        """A callback to destroy the tkinter window."""
        self.window.destroy()

    def draw_tree(self):
        # Remove any previous widgets.
        self.canvas.delete("all")
        if self.root != None:
            self.root.arrange_and_draw_subtree(self.canvas, 10, 10)

    def ctrl_a_pressed(self, event):
        self.add_value()

    def add_value(self):
        # Add a value to the tree.
        new_string = self.value_entry.get()
        if not new_string:
            return

        self.value_entry.delete(0, "end")
        self.value_entry.focus_set()

        try:
            new_value = int(new_string)
        except Exception as e:
            messagebox.showinfo(
                "Find Error", f"Value {new_string} must be an integer.\n{e}"
            )
            return

        if new_value <= 0:
            messagebox.showinfo(
                "Add Error", f"Value {new_value} must be a positive integer."
            )
            return

        try:
            new_node = SortedBinaryNode(new_value)
            self.root.add_node(new_node)
        except Exception as e:
            messagebox.showinfo(
                "Add Error", f"Error adding value {new_value} to the tree.\n{e}"
            )

        self.draw_tree()

    def ctrl_p_pressed(self, event):
        self.pop_value()

    def pop_value(self):
        # Remove a value from the tree.
        target_string = self.value_entry.get()
        if not target_string:
            return

        self.value_entry.delete(0, "end")
        self.value_entry.focus_set()

        try:
            target = int(target_string)
        except Exception as e:
            messagebox.showinfo(
                "Pop Error", f"Value {target_string} must be an integer.\n{e}"
            )
            return

        try:
            node = self.root.pop(target)
        except Exception as e:
            messagebox.showinfo(
                "Pop Error", f"Error removing value {target} from the tree.\n{e}"
            )

        self.draw_tree()

    def ctrl_f_pressed(self, event):
        self.find_value()

    def find_value(self):
        # Find the value's node.
        target_string = self.value_entry.get()
        if not target_string:
            return

        self.value_entry.delete(0, "end")
        self.value_entry.focus_set()

        try:
            target = int(target_string)
        except Exception as e:
            messagebox.showinfo(
                "Find Error", f"Value {target_string} must be an integer.\n{e}"
            )
            return

        try:
            node = self.root.find_node(target)
            if node == None:
                messagebox.showinfo(
                    "Not Found", f"The value {target} is not in the tree."
                )
            else:
                messagebox.showinfo(
                    "Value Found", f"Found node with value {node.value}."
                )
        except Exception as e:
            messagebox.showinfo(
                "Find Error", f"Error removing value {target} from the tree.\n{e}"
            )

        # Redraw the tree.
        self.draw_tree()

    def run_tests(self):
        pass


if __name__ == "__main__":
    App()
