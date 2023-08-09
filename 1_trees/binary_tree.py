from __future__ import annotations

import tkinter as tk
from typing import Optional, Tuple

from draw_binary_tree import arrange_and_draw_subtree


class Node:
    indent = "  "

    def __init__(
        self,
        value,
        left: Optional[Node] = None,
        right: Optional[Node] = None,
    ):
        self.value = value
        self.left = left
        self.right = right

    def add_left(self, left: Node):
        self.left = left

    def add_right(self, right: Node):
        self.right = right

    def is_leaf(self) -> bool:
        return self.left is None and self.right is None

    def find_node(self, value) -> Optional[Node]:
        if self.value == value:
            return self
        if self.left:
            if node := self.left.find_node(value):
                return node
        if self.right:
            if node := self.right.find_node(value):
                return node
        return None

    def __str__(self, level=0) -> str:
        s = f"{Node.indent * level}{self.value}:"
        if self.left:
            s += f"\n{self.left.__str__(level + 1)}"
        if self.right:
            s += f"\n{self.right.__str__(level + 1)}"
        return s


def find_value(root: Node, value) -> None:
    if root.find_node(value):
        print(f"Found {value}")
    else:
        print(f"Value {value} not found")


a = Node("A")
b = Node("B")
c = Node("C")
d = Node("D")
e = Node("E")
f = Node("F")
g = Node("G")
h = Node("H")
i = Node("I")
j = Node("J")
k = Node("K")
l = Node("L")

a.add_left(b)
a.add_right(c)
b.add_left(d)
b.add_right(e)
c.add_left(f)
c.add_right(g)
e.add_left(h)
e.add_right(i)
g.add_left(j)
j.add_left(k)
j.add_right(l)

print(a)


def kill_callback():
    """A callback to destroy the tkinter window."""
    window.destroy()


# Make the tkinter window.
window = tk.Tk()
window.title("binary_node5")
window.protocol("WM_DELETE_WINDOW", kill_callback)
window.geometry("260x220")

canvas = tk.Canvas(window, bg="white", borderwidth=2, relief=tk.SUNKEN)
canvas.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Draw the tree.
arrange_and_draw_subtree(a, canvas, 10, 10)

window.focus_force()
window.mainloop()
