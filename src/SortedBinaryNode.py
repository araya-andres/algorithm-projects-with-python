from __future__ import annotations
from tkinter import messagebox
from tkinter import simpledialog
from typing import Optional, Tuple
import tkinter as tk

radius = 10  # Radius of a node’s circle
x_spacing = 20  # Horizontal distance between neighboring subtrees
y_spacing = 20  # Vertical distance between parent and child subtrees


class SortedBinaryNode:
    indent = "  "

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.h_left = 0
        self.h_right = 0

    def __len__(self):
        return size(self)

    def __str__(self, level=0) -> str:
        s = f"{SortedBinaryNode.indent * level}{self.value}"
        if not is_leaf(self):
            s += ":"
            if self.left:
                s += f"\n{self.left.__str__(level + 1)}"
            if self.right:
                s += f"\n{self.right.__str__(level + 1)}"
        return s


def size(p: SortedBinaryNode):
    if p is None:
        return 0
    return 1 + size(p.left) + size(p.right)


def find(current_node: Optional[SortedBinaryNode], value) -> Optional[SortedBinaryNode]:
    if current_node is None:
        return None
    if current_node.value > value:
        return find(current_node.left, value)
    if current_node.value < value:
        return find(current_node.right, value)
    return current_node


def node_min(p: SortedBinaryNode):
    return p if p.left is None else node_min(p.left)


def put(root: Optional[SortedBinaryNode], value) -> SortedBinaryNode:
    new_root, _ = put_helper(root, value)
    return new_root


def put_helper(root: Optional[SortedBinaryNode], value) -> Tuple(SortedBinaryNode, int):
    if root is None:
        return (SortedBinaryNode(value), 0)
    if value < root.value:
        root.left, h_left = put_helper(root.left, value)
        root.h_left = max(h_left + 1, root.h_left)
    if value > root.value:
        root.right, h_right = put_helper(root.right, value)
        root.h_right = max(h_right + 1, root.h_right)
    if -2 < balance_factor(root) < 2:
        return (root, height(root))
    else:
        return rebalance(root)


def balance_factor(p: SortedBinaryNode):
    return p.h_left - p.h_right if p else 0


def rebalance(p: SortedBinaryNode):
    bf = balance_factor(p)
    bf_right = balance_factor(p.right)
    bf_left = balance_factor(p.left)
    if bf == -2 and bf_right == -1:
        p = single_left_rotation(p)
    elif bf == 2 and bf_left == 1:
        p = single_right_rotation(p)
    elif bf == 2 and bf_left == -1:
        p = left_right_rotation(p)
    elif bf == -2 and bf_right == 1:
        p = right_left_rotation(p)
    return (p, height(p))


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
def single_left_rotation(p: SortedBinaryNode) -> SortedBinaryNode:
    q = p.right
    p.right = q.left
    q.left = p
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
def single_right_rotation(p: SortedBinaryNode) -> SortedBinaryNode:
    q = p.left
    p.left = q.right
    q.right = p
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
def left_right_rotation(p: SortedBinaryNode) -> SortedBinaryNode:
    p.left = single_left_rotation(p.left)
    return single_right_rotation(p)


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
def right_left_rotation(p: SortedBinaryNode) -> SortedBinaryNode:
    p.right = single_right_rotation(p.right)
    return single_left_rotation(p)


def height(p: SortedBinaryNode):
    if p is None:
        return -1
    p.h_left = height(p.left) + 1
    p.h_right = height(p.right) + 1
    return max(p.h_left, p.h_right)


def is_leaf(p: SortedBinaryNode) -> bool:
    return p.left is None and p.right is None


def pop(p: SortedBinaryNode, value):
    if p is None:
        return None
    if value < p.value:
        p.left = pop(p.left, value)
    elif value > p.value:
        p.right = pop(p.right, value)
    else:
        if p.right is None:
            return p.left
        if p.left is None:
            return p.right
        t = p
        p = node_min(t.right)
        p.right = delete_min(t.right)
        p.left = t.left
        t.right = t.left = None
    return p


def delete_min(p: SortedBinaryNode):
    if p.left is None:
        return p.right
    p.left = delete_min(p.left)
    return p


def traverse_preorder(p: SortedBinaryNode):
    yield p
    if p.left:
        yield from traverse_preorder(p.left)
    if p.right:
        yield from traverse_preorder(p.right)


def traverse_inorder(p: SortedBinaryNode):
    if p.left:
        yield from traverse_inorder(p.left)
    yield p
    if p.right:
        yield from traverse_inorder(p.right)


def traverse_postorder(p: SortedBinaryNode):
    if p.left:
        yield from traverse_postorder(p.left)
    if p.right:
        yield from traverse_postorder(p.right)
    yield p


def traverse_breadth_first(p: SortedBinaryNode):
    queue = [p]
    while queue:
        p = queue.pop(0)
        yield p
        if p.left:
            queue.append(p.left)
        if p.right:
            queue.append(p.right)


def arrange_subtree(
    p: SortedBinaryNode, xmin: float, ymin: float
) -> Tuple[float, float, float, float]:
    r = radius
    cy = r + ymin

    if is_leaf(p):
        cx = r + xmin
        p.center = (cx, cy)
        p.subtree_bounds = (cx - r, cy - r, cx + r, cy + r)
        return p.subtree_bounds

    child_x, child_y = xmin, y_spacing + cy + r
    ymax = 0

    if p.left:
        _, _, xmax, ymax = arrange_subtree(p.left, child_x, child_y)
        child_x = xmax + x_spacing
    if p.right:
        _, _, xmax, y = arrange_subtree(p.right, child_x, child_y)
        ymax = max(ymax, y)

    p.center = ((xmax + xmin) / 2, cy)
    p.subtree_bounds = (xmin, ymin, xmax, ymax)
    return p.subtree_bounds


def draw_subtree_links(p: SortedBinaryNode, canvas: tk.Canvas) -> None:
    if p.left:
        canvas.create_line(*p.center, *p.left.center)
        draw_subtree_links(p.left, canvas)
    if p.right:
        canvas.create_line(*p.center, *p.right.center)
        draw_subtree_links(p.right, canvas)


def draw_subtree_nodes(p: SortedBinaryNode, canvas: tk.Canvas) -> None:
    if p is None:
        return
    cx, cy = p.center
    r = radius
    canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill="white")
    canvas.create_text(cx, cy, text=str(p.value))
    draw_subtree_nodes(p.left, canvas)
    draw_subtree_nodes(p.right, canvas)
    # Outline the subtree for debugging.
    # canvas.create_rectangle(p.subtree_bounds, fill="", outline="red")


def arrange_and_draw_subtree(root, canvas: tk.Canvas, xmin: float, ymin: float) -> None:
    arrange_subtree(root, xmin, ymin)
    draw_subtree_links(root, canvas)
    draw_subtree_nodes(root, canvas)


class App:
    def __init__(self):
        # Make a sentinel root.
        self.root = None
        self.run_tests()

        # Make the tkinter window.
        self.window = tk.Tk()
        self.window.title("SortedBinaryNode")
        self.window.protocol("WM_DELETE_WINDOW", self.kill_callback)
        self.window.geometry("390x320")

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
            arrange_and_draw_subtree(self.root, self.canvas, 10, 10)

    def ctrl_a_pressed(self, event):
        self.add_value()

    def add_value(self):
        # Add a value to the tree.
        if new_string := self.value_entry.get():
            self.value_entry.delete(0, "end")
            self.value_entry.focus_set()
            try:
                new_value = int(new_string)
                self.root = put(self.root, new_value)
                self.draw_tree()
            except ValueError as e:
                messagebox.showinfo(
                    "Find Error", f"Value {new_string} must be an integer.\n{e}"
                )
            except Exception as e:
                messagebox.showinfo(
                    "Add Error", f"Error adding value {new_value} to the tree.\n{e}"
                )

    def ctrl_p_pressed(self, event):
        self.pop_value()

    def pop_value(self):
        # Remove a value from the tree.
        if target_string := self.value_entry.get():
            self.value_entry.delete(0, "end")
            self.value_entry.focus_set()

            try:
                target = int(target_string)
                self.root = pop(self.root, target)
                height(self.root)
                self.draw_tree()
            except ValueError as e:
                messagebox.showinfo(
                    "Pop Error", f"Value {target_string} must be an integer.\n{e}"
                )
            except Exception as e:
                messagebox.showinfo(
                    "Pop Error", f"Error removing value {target} from the tree.\n{e}"
                )

    def ctrl_f_pressed(self, event):
        self.find_value()

    def find_value(self):
        # Find the value's node.
        if target_string := self.value_entry.get():
            self.value_entry.delete(0, "end")
            self.value_entry.focus_set()

            try:
                target = int(target_string)
                node, _ = find(self.root, target)
                if node is None:
                    messagebox.showinfo(
                        "Not Found", f"The value {target} is not in the tree."
                    )
                self.draw_tree()
            except ValueError as e:
                messagebox.showinfo(
                    "Find Error", f"Value {target_string} must be an integer.\n{e}"
                )
                return
            except Exception as e:
                messagebox.showinfo(
                    "Find Error", f"Error removing value {target} from the tree.\n{e}"
                )

    def run_tests(self):
        for x in [60, 35, 76, 21, 42, 71, 89, 17, 24, 74, 11, 23, 72, 75]:
            self.root = put(self.root, x)


if __name__ == "__main__":
    App()
