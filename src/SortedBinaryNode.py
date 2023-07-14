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
        self.h_left = 0
        self.h_right = 0

    def add_node(self, node: SortedBinaryNode) -> Tuple(SortedBinaryNode, int):
        if node.value < self.value:
            if self.left_child:
                self.left_child, h_left = self.left_child.add_node(node)
                self.h_left = max(h_left + 1, self.h_left)
            else:
                self.left_child = node
                self.h_left = 1
        if node.value > self.value:
            if self.right_child:
                self.right_child, h_right = self.right_child.add_node(node)
                self.h_right = max(h_right + 1, self.h_right)
            else:
                self.right_child = node
                self.h_right = 1
        if self.bf() < -1 or self.bf() > 1:
            return self.__rebalance()
        else:
            return (self, self.height())

    def height(self):
        return max(self.h_left, self.h_right)

    def bf(self):
        return self.h_left - self.h_right

    def __get_new_hight(self):
        self.h_left = self.h_right = 0
        if self.is_leaf():
            return 0
        else:
            if self.h_left:
                self.left_child = self.left_child.__get_new_hight() + 1
            if self.h_right:
                self.h_right = self.right_child.__get_new_hight() + 1
            return max(self.h_left, self.h_right)

    def __rebalance(self):
        bf = self.bf()
        bf_right = self.right_child.bf() if self.right_child else 0
        bf_left = self.left_child.bf() if self.left_child else 0
        if bf == -2 and bf_right == -1:
            new_root = self.single_left_rotation(self)
        elif bf == 2 and bf_left == 1:
            new_root = self.single_right_rotation(self)
        elif bf == 2 and bf_left == -1:
            new_root = self.left_right_rotation(self)
        elif bf == -2 and bf_right == 1:
            new_root = self.right_left_rotation(self)
        return (new_root, new_root.__get_new_hight())

    #
    #  p (1) bf = -2               q (2)
    #    / \                         / \
    #  pl   \                       /   \
    #        \                     /     \
    #      q (2) bf = -1       p (1)   r (3)
    #        / \                 / \
    #      ql   \              pl   ql
    #            \
    #          r (3) bf = 0
    #
    def single_left_rotation(self, p: SortedBinaryNode) -> SortedBinaryNode:
        q = p.right_child
        p.right_child = q.left_child
        q.left_child = p
        return q

    #
    #          p (3) bf = 2        q (2)
    #            / \                 / \
    #           /   pr              /   \
    #          /                   /     \
    #      q (2) bf = 1        r (1)   p (3)
    #        / \                         / \
    #       /   qr                     qr   pr
    #      /
    #  r (1) bf = 0
    #
    def single_right_rotation(self, p: SortedBinaryNode) -> SortedBinaryNode:
        q = p.left_child
        p.left_child = q.right_child
        q.right_child = p
        return q

    #
    #          p (3) bf = 2            p (3) bf = 2        r (2)
    #            /                       /                   / \
    #           /                       /                   /   \
    #          /                       /                   /     \
    #      q (1) bf = -1           r (2) bf = 1        q (1)   p (3)
    #          \                     /
    #           \                   /
    #            \                 /
    #          r (2) bf = 0    q (1) bf = 0
    #
    def left_right_rotation(self, p: SortedBinaryNode) -> SortedBinaryNode:
        p.left_child = self.single_left_rotation(p.left_child)
        return self.single_right_rotation(p)

    #
    #  p (1) bf = -2       p (1) bf = -2               r (2)
    #    / \                   \                         / \
    #  pl   \                   \                       /   \
    #        \                   \                     /     \
    #      q (3) bf = 1        r (2) bf = -1       q (1)   p (3)
    #        /                     \
    #       /                       \
    #      /                         \
    #  r (2) bf = 0                q (3) bf = 0
    #
    def right_left_rotation(self, p: SortedBinaryNode) -> SortedBinaryNode:
        p.right_child = self.single_right_rotation(p.right_child)
        return self.single_left_rotation(p)

    def is_leaf(self) -> bool:
        return self.left_child is None and self.right_child is None

    def find_node(self, value) -> Optional[SortedBinaryNode]:
        if value == self.value:
            return self
        if value < self.value and self.left_child is not None:
            return self.left_child.find_node(value)
        if value > self.value and self.right_child is not None:
            return self.right_child.find_node(value)
        return None

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

        child_x, child_y = xmin, SortedBinaryNode.y_spacing + cy + r
        xmax, ymax = 0, 0

        if self.left_child:
            _, _, xmax, ymax = self.left_child.arrange_subtree(child_x, child_y)
            child_x = xmax + SortedBinaryNode.x_spacing
        if self.right_child:
            _, _, xmax, y = self.right_child.arrange_subtree(child_x, child_y)
            ymax = max(ymax, y)

        self.center = ((xmax + xmin) / 2, cy)
        self.subtree_bounds = (xmin, ymin, xmax, ymax)
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
        self.root = None
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
            if self.root:
                self.root, _ = self.root.add_node(new_node)
            else:
                self.root = new_node
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
