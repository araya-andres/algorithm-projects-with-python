from __future__ import annotations
from typing import Optional
import tkinter as tk


def binary_tree_as_str(node: BinaryNode, level: int) -> str:
    indent = "  " * level
    if node is None:
        return f"{indent}{node}"
    elif node.has_children():
        left_child = binary_tree_as_str(node.left_child, level + 1)
        right_child = binary_tree_as_str(node.right_child, level + 1)
        return f"{indent}{node.value}:\n{left_child}\n{right_child}"
    else:
        return f"{indent}{node.value}:"


class BinaryNode:
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

    def __str__(self) -> str:
        return binary_tree_as_str(self, 0)

    def arrange_subtree(self, xmin, ymin):
        """Position the node's subtree."""
        # Calculate cy, the Y coordinate for this node.
        # This doesn't depend on the children.
        # ...

        # If the node has no children, just place it here and return.
        # ...

        # Set child_xmin and child_ymin to the
        # start position for child subtrees.
        # ...

        # Position the child subtrees.
        # ...

        if self.right_child != None:
            # Arrange the right child subtree.
            # ...
            pass

        # Arrange this node depending on the number of children.
        if (self.left_child != None) and (self.right_child != None):
            # Two children. Center this node over the child nodes.
            # Use the child subtree bounds to set our subtree bounds.
            # ...
            pass
        elif self.left_child != None:
            # We have only a left child.
            # ...
            pass
        else:
            # We have only a right child.
            # ...
            pass

    def draw_subtree_links(self, canvas):
        """Draw the subtree's links."""
        # ...

        # Outline the subtree for debugging.
        # canvas.create_rectangle(self.subtree_bounds, fill='', outline='red')

    def draw_subtree_nodes(self, canvas):
        """Draw the subtree's nodes."""
        # Draw the node.
        # ...

        # Draw the descendants' nodes.
        # ...
        pass

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
