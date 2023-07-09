from __future__ import annotations
from typing import Optional
import tkinter as tk


class BinaryNode:
    indent = "  "
    radius = 10  # Radius of a node’s circle
    x_spacing = 20  # Horizontal distance between neighboring subtrees
    y_spacing = 20  # Vertical distance between parent and child subtrees

    def __init__(
        self, value, left_child: BinaryNode = None, right_child: BinaryNode = None
    ):
        self.value = value
        self.left_child = left_child
        self.right_child = right_child

        # Initialize drawing parameters.
        self.center = (0, 0)
        self.subtree_bounds = (
            -BinaryNode.radius,
            -BinaryNode.radius,
            BinaryNode.radius,
            BinaryNode.radius,
        )

    def add_left(self, left: BinaryNode):
        self.left_child = left

    def add_right(self, right: BinaryNode):
        self.right_child = right

    def has_children(self) -> bool:
        return self.left_child or self.right_child

    def find_node(self, value) -> Optional[BinaryNode]:
        if self.value == value:
            return self
        if self.left_child:
            if node := self.left_child.find_node(value):
                return node
        if self.right_child:
            if node := self.right_child.find_node(value):
                return node
        return None

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
        s = f"{BinaryNode.indent * level}{self.value}:"
        if self.left_child:
            s += f"\n{self.left_child.__str__(level + 1)}"
        if self.right_child:
            s += f"\n{self.right_child.__str__(level + 1)}"
        return s

    def arrange_subtree(self, xmin, ymin):
        r = BinaryNode.radius
        cy = r + ymin

        if not self.has_children():
            cx = r + xmin
            self.center = (cx, cy)
            self.subtree_bounds = (cx - r, cy - r, cx + r, cy + r)
            return

        child_ymin = BinaryNode.y_spacing + cy + r
        child_xmin = xmin

        if self.left_child and self.right_child:
            x_spacing = BinaryNode.x_spacing
            self.left_child.arrange_subtree(child_xmin, child_ymin)
            self.right_child.arrange_subtree(child_xmin, child_ymin)
            xl0, yl0, xl1, yl1 = self.left_child.subtree_bounds
            xr0, yr0, xr1, yr1 = self.right_child.subtree_bounds
            wl, wr = xl1 - xl0, xr1 - xr0
            w = wl + wr + x_spacing
            self.center = (xmin + w // 2, cy)
            self.subtree_bounds = (
                xmin,
                ymin,
                xmin + w,
                child_ymin + max(yl1 - yl0, yr1 - yr0),
            )
            self.left_child.arrange_subtree(xmin, child_ymin)
            self.right_child.arrange_subtree(xmin + wl + x_spacing, child_ymin)
        elif self.left_child:
            self.left_child.arrange_subtree(child_xmin, child_ymin)
            x0, y0, x1, y1 = self.left_child.subtree_bounds
            self.center = ((x0 + x1) // 2, cy)
            self.subtree_bounds = (x0, ymin, x1, child_ymin + y1 - y0)
        else:
            self.right_child.arrange_subtree(child_xmin, child_ymin)
            x0, y0, x1, y1 = self.right_child.subtree_bounds
            self.center = ((x0 + x1) // 2, cy)
            self.subtree_bounds = (x0, ymin, x1, child_ymin + y1 - y0)

    def draw_subtree_links(self, canvas: tk.Canvas):
        if self.left_child:
            canvas.create_line(
                self.center[0],
                self.center[1],
                self.left_child.center[0],
                self.left_child.center[1],
            )
            self.left_child.draw_subtree_links(canvas)
        if self.right_child:
            canvas.create_line(
                self.center[0],
                self.center[1],
                self.right_child.center[0],
                self.right_child.center[1],
            )
            self.right_child.draw_subtree_links(canvas)

        # Outline the subtree for debugging.
        # canvas.create_rectangle(self.subtree_bounds, fill='', outline='red')

    def draw_subtree_nodes(self, canvas: tk.Canvas):
        cx, cy = self.center
        r = BinaryNode.radius
        canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill="white")
        canvas.create_text(cx, cy, text=str(self.value))
        if self.left_child:
            self.left_child.draw_subtree_nodes(canvas)
        if self.right_child:
            self.right_child.draw_subtree_nodes(canvas)

    def arrange_and_draw_subtree(self, canvas, xmin, ymin):
        # Position the tree.
        self.arrange_subtree(xmin, ymin)

        # Draw the links.
        self.draw_subtree_links(canvas)

        # Draw the nodes.
        self.draw_subtree_nodes(canvas)


def find_value(root: BinaryNode, value) -> None:
    if root.find_node(value):
        print(f"Found {value}")
    else:
        print(f"Value {value} not found")


a = BinaryNode("A")
b = BinaryNode("B")
c = BinaryNode("C")
d = BinaryNode("D")
e = BinaryNode("E")
f = BinaryNode("F")
g = BinaryNode("G")
h = BinaryNode("H")
i = BinaryNode("I")
j = BinaryNode("J")
k = BinaryNode("K")
l = BinaryNode("L")

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
a.arrange_and_draw_subtree(canvas, 10, 10)

window.focus_force()
window.mainloop()
