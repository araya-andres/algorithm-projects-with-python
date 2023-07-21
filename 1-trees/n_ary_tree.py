from __future__ import annotations

import tkinter as tk
from typing import List, Optional, Tuple


class NaryNode:
    indent = "  "
    radius = 10  # Radius of a node’s circle
    x_spacing = 20  # Horizontal distance between neighboring subtrees
    y_spacing = 20  # Vertical distance between parent and child subtrees

    def __init__(self, value, children: Optional[List[NaryNode]] = None):
        self.value = value
        self.children = children if children else []

    def add_child(self, child_node: NaryNode):
        self.children.append(child_node)

    def find_node(self, value) -> Optional[NaryNode]:
        if value == self.value:
            return self
        for child in self.children:
            if node := child.find_node(value):
                return node
        return None

    def traverse_preorder(self):
        yield self
        for child in self.children:
            yield from child.traverse_preorder()

    def traverse_postorder(self):
        for child in self.children:
            yield from child.traverse_postorder()
        yield self

    def traverse_breadth_first(self):
        queue = [self]
        while queue:
            node = queue.pop(0)
            yield node
            queue += node.children

    def __str__(self, level=0) -> str:
        s = f"{NaryNode.indent * level}{self.value}:"
        for child in self.children:
            s += f"\n{child.__str__(level + 1)}"
        return s

    def arrange_subtree(
        self, xmin: float, ymin: float
    ) -> Tuple[float, float, float, float]:
        r = NaryNode.radius
        cy = r + ymin

        if len(self.children) == 0:
            cx = r + xmin
            self.center = (cx, cy)
            self.subtree_bounds = (cx - r, cy - r, cx + r, cy + r)
        else:
            child_height = 0
            child_ymin = NaryNode.y_spacing + cy + r
            width = 0
            for i, child in enumerate(self.children):
                if i > 0:
                    width += NaryNode.x_spacing
                _, y0, x1, y1 = child.arrange_subtree(xmin + width, child_ymin)
                child_height = max(child_height, y1 - y0)
                width = x1 - xmin
            self.center = (xmin + width / 2, cy)
            self.subtree_bounds = (xmin, ymin, xmin + width, child_ymin + child_height)

        return self.subtree_bounds

    def draw_subtree_links(self, canvas: tk.Canvas) -> None:
        if len(self.children) == 1:
            canvas.create_line(*self.center, *self.children[0].center)
            self.children[0].draw_subtree_links(canvas)
        elif len(self.children) > 1:
            cx, cy = self.center
            x0, y0 = self.children[0].center
            x1, _ = self.children[-1].center
            yh = (cy + y0) / 2
            # Horizonal line
            canvas.create_line(x0, yh, x1, yh)
            # Center -> Horizontal line
            canvas.create_line(cx, cy, cx, yh)
            for child in self.children:
                cx, cy = child.center
                # Horizontal line -> Child
                canvas.create_line(cx, yh, cx, cy)
                child.draw_subtree_links(canvas)

    def draw_subtree_nodes(self, canvas: tk.Canvas) -> None:
        cx, cy = self.center
        r = NaryNode.radius
        canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill="white")
        canvas.create_text(cx, cy, text=str(self.value))
        for child in self.children:
            child.draw_subtree_nodes(canvas)
        # Outline the subtree for debugging.
        canvas.create_rectangle(self.subtree_bounds, outline="red")

    def arrange_and_draw_subtree(
        self, canvas: tk.Canvas, xmin: float, ymin: float
    ) -> None:
        self.arrange_subtree(xmin, ymin)
        self.draw_subtree_links(canvas)
        self.draw_subtree_nodes(canvas)


def find_value(root: NaryNode, value) -> None:
    if root.find_node(value):
        print(f"Found {value}")
    else:
        print(f"Value {value} not found")


a = NaryNode("A")
b = NaryNode("B")
c = NaryNode("C")
d = NaryNode("D")
e = NaryNode("E")
f = NaryNode("F")
g = NaryNode("G")
h = NaryNode("H")
i = NaryNode("I")
j = NaryNode("J")
k = NaryNode("K")

a.add_child(b)
a.add_child(c)
a.add_child(d)
b.add_child(e)
b.add_child(f)
d.add_child(g)
e.add_child(h)
g.add_child(i)
g.add_child(j)
g.add_child(k)

print(a)


def kill_callback():
    """A callback to destroy the tkinter window."""
    window.destroy()


# Make the tkinter window.
window = tk.Tk()
window.title("nary_node5")
window.protocol("WM_DELETE_WINDOW", kill_callback)
window.geometry("260x180")

canvas = tk.Canvas(window, bg="white", borderwidth=2, relief=tk.SUNKEN)
canvas.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Draw the tree.
a.arrange_and_draw_subtree(canvas, 10, 10)

window.focus_force()
window.mainloop()
