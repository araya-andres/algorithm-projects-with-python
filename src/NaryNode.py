from __future__ import annotations
from typing import List
import tkinter as tk


class NaryNode:
    indent = "  "
    radius = 10  # Radius of a node’s circle
    x_spacing = 20  # Horizontal distance between neighboring subtrees
    y_spacing = 20  # Vertical distance between parent and child subtrees

    def __init__(self, value, children: List[NaryNode] = []):
        self.value = value
        self.children = children

        # Initialize drawing parameters.
        self.center = (0, 0)
        self.subtree_bounds = (
            -NaryNode.radius,
            -NaryNode.radius,
            NaryNode.radius,
            NaryNode.radius,
        )

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
        return "\n".join(
            [f"{NaryNode.indent * level}{self.value}"]
            + [child.__str__(level + 1) for child in self.children]
        )

    def arrange_subtree(self, xmin, ymin):
        """Position the node's subtree."""
        # Calculate cy, the Y coordinate for this node.
        # This doesn't depend on the children.
        # ...

        # If the node has no children, just place it here and return.
        if len(self.children) == 0:
            # ...
            return

        # Set child_xmin and child_ymin to the
        # start position for child subtrees.
        # ...

        # Set ymax equal to the largest Y position used.
        ymax = ymin + 2 * NaryNode.radius

        # Position the child subtrees.
        for child in self.children:
            # ...
            # Position this child subtree.
            ...

            # Update child_xmin to allow room for the subtree
            # and space between the subtrees.
            ...

            # Update the subtree bottom ymax.
            # ...

        # Set xmax equal to child_xmin minus the horizontal
        # spacing we added after the last subtree.
        # ...

        # Use xmin, ymin, xmax, and ymax to set our subtree bounds.
        # ...

        # Center this node over the subtree bounds.
        # ...

    def draw_subtree_links(self, canvas):
        """Draw the subtree's links."""
        # If we have exactly one child, just draw to it.
        if len(self.children) == 1:
            # ...
            pass

        # Else if we have more than one child,
        # draw vertical and horizontal branches.
        elif len(self.children) > 0:
            # ...
            pass

        # Recursively draw child subtree links.
        # ...

        # Outline the subtree for debugging.
        # canvas.create_rectangle(self.subtree_bounds, fill='', outline='red')

    def draw_subtree_nodes(self, canvas):
        """Draw the subtree's nodes."""
        # Draw the node.
        # ...

        # Draw the descendants' nodes.
        # ...

    def arrange_and_draw_subtree(self, canvas, xmin, ymin):
        # Position the tree.
        self.arrange_subtree(xmin, ymin)

        # Draw the links.
        self.draw_subtree_links(canvas)

        # Draw the nodes.
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
