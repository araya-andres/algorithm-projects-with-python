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
        self.left_child = None
        self.right_child = None
        self.h_left = 0
        self.h_right = 0

    def __str__(self, level=0) -> str:
        s = f"{SortedBinaryNode.indent * level}{self.value}:"
        if self.left_child:
            s += f"\n{self.left_child.__str__(level + 1)}"
        if self.right_child:
            s += f"\n{self.right_child.__str__(level + 1)}"
        return s


def find(
    value, node: SortedBinaryNode, parent: Optional[SortedBinaryNode] = None
) -> Tuple(Optional[SortedBinaryNode], Optional[SortedBinaryNode]):
    if node is None:
        return (None, None)
    if node.value > value:
        return find(value, node.left_child, node)
    if node.value < value:
        return find(value, node.right_child, node)
    return (node, parent)


def children(node: SortedBinaryNode) -> int:
    n = 0
    if node.left_child:
        n += 1
    if node.right_child:
        n += 1
    return n


def add_node(
    root: Optional[SortedBinaryNode], node: SortedBinaryNode
) -> Tuple(SortedBinaryNode, int):
    if root is None:
        return (node, 1)
    if node.value < root.value:
        root.left_child, h_left = add_node(root.left_child, node)
        root.h_left = max(h_left + 1, root.h_left)
    if node.value > root.value:
        root.right_child, h_right = add_node(root.right_child, node)
        root.h_right = max(h_right + 1, root.h_right)
    if balance_factor(root) < -1 or balance_factor(root) > 1:
        return rebalance(root)
    else:
        return (root, height(root))


def balance_factor(p: SortedBinaryNode):
    return p.h_left - p.h_right if p else 0


def rebalance(p: SortedBinaryNode):
    bf = balance_factor(p)
    bf_right = balance_factor(p.right_child)
    bf_left = balance_factor(p.left_child)
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
def single_right_rotation(p: SortedBinaryNode) -> SortedBinaryNode:
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
def left_right_rotation(p: SortedBinaryNode) -> SortedBinaryNode:
    p.left_child = single_left_rotation(p.left_child)
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
    p.right_child = single_right_rotation(p.right_child)
    return single_left_rotation(p)


def height(p: SortedBinaryNode):
    if p is None:
        return 0
    p.h_left = height(p.left_child) + 1
    p.h_right = height(p.right_child) + 1
    return max(p.h_left, p.h_right)


def is_leaf(p: SortedBinaryNode) -> bool:
    return p.left_child is None and p.right_child is None


def pop(t: SortedBinaryNode, p: Optional[SortedBinaryNode]):
    if t is None:
        return
    n = children(t)
    if n == 0:
        if p.left_child == t:
            p.left_child = None
        else:
            p.right_child = None
    elif n == 1:
        s = t.left_child if t.left_child else t.right_child
        if p.left_child == t:
            p.left_child = s
        else:
            p.right_child = s
        t.left_child = t.right_child = None
    else:
        pass


def traverse_preorder(p: SortedBinaryNode):
    yield p
    if p.left_child:
        yield from traverse_preorder(p.left_child)
    if p.right_child:
        yield from traverse_preorder(p.right_child)


def traverse_inorder(p: SortedBinaryNode):
    if p.left_child:
        yield from traverse_inorder(p.left_child)
    yield p
    if p.right_child:
        yield from traverse_inorder(p.right_child)


def traverse_postorder(p: SortedBinaryNode):
    if p.left_child:
        yield from traverse_postorder(p.left_child)
    if p.right_child:
        yield from traverse_postorder(p.right_child)
    yield p


def traverse_breadth_first(p: SortedBinaryNode):
    queue = [p]
    while queue:
        q = queue.pop(0)
        yield q
        if q.left_child:
            queue.append(q.left_child)
        if q.right_child:
            queue.append(q.right_child)


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

    if p.left_child:
        _, _, xmax, ymax = arrange_subtree(p.left_child, child_x, child_y)
        child_x = xmax + x_spacing
    if p.right_child:
        _, _, xmax, y = arrange_subtree(p.right_child, child_x, child_y)
        ymax = max(ymax, y)

    p.center = ((xmax + xmin) / 2, cy)
    p.subtree_bounds = (xmin, ymin, xmax, ymax)
    return p.subtree_bounds


def draw_subtree_links(p: SortedBinaryNode, canvas: tk.Canvas) -> None:
    if p.left_child:
        canvas.create_line(*p.center, *p.left_child.center)
        draw_subtree_links(p.left_child, canvas)
    if p.right_child:
        canvas.create_line(*p.center, *p.right_child.center)
        draw_subtree_links(p.right_child, canvas)


def draw_subtree_nodes(p: SortedBinaryNode, canvas: tk.Canvas) -> None:
    if p is None:
        return
    cx, cy = p.center
    r = radius
    canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill="white")
    canvas.create_text(cx, cy, text=str(p.value))
    draw_subtree_nodes(p.left_child, canvas)
    draw_subtree_nodes(p.right_child, canvas)
    # Outline the subtree for debugging.
    canvas.create_rectangle(p.subtree_bounds, fill="", outline="red")


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
                new_node = SortedBinaryNode(new_value)
                self.root, _ = add_node(self.root, new_node)
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
            node, parent = find(target, self.root)
            if node:
                pop(node, parent)
        except Exception as e:
            messagebox.showinfo(
                "Pop Error", f"Error removing value {target} from the tree.\n{e}"
            )

        self.draw_tree()

    def ctrl_f_pressed(self, event):
        self.find_value()

    def find_value(self):
        # Find the value's node.
        if target_string := self.value_entry.get():
            self.value_entry.delete(0, "end")
            self.value_entry.focus_set()

            try:
                target = int(target_string)
                node, _ = find(target, self.root)
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
        values = [60, 35, 76, 21, 42, 71, 89, 17, 24, 74, 11, 23, 72, 75]
        for x in values:
            self.root, _ = add_node(self.root, SortedBinaryNode(x))
        print(self.root)
        print(",".join(str(x.value) for x in traverse_preorder(self.root)))
        print(",".join(str(x.value) for x in traverse_inorder(self.root)))
        print(",".join(str(x.value) for x in traverse_postorder(self.root)))
        print(",".join(str(x.value) for x in traverse_breadth_first(self.root)))


if __name__ == "__main__":
    App()
