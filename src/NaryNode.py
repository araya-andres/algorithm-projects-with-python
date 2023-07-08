from __future__ import annotations
from typing import List
import tkinter as tk


def nary_tree_as_str(node: NaryNode, level: int) -> str:
    indent = "  " * level
    if node is None:
        return f"{indent}{node}"
    elif len(node.children) > 0:
        children = "\n".join(
            nary_tree_as_str(child, level + 1) for child in node.children
        )
        return f"{indent}{node.value}:\n{children}"
    else:
        return f"{indent}{node.value}:"


class NaryNode:
    node_radius = 8  # FIXME

    def __init__(self, value, children: List[NaryNode] = []):
        self.value = value
        self.children = children

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

    def __str__(self) -> str:
        return nary_tree_as_str(self, 0)

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
        ymax = ymin + 2 * NaryNode.node_radius

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
