"""
Sorted binary tree.
"""
from __future__ import annotations

import tkinter as tk
from tkinter import messagebox
from typing import Optional, Tuple

from draw_binary_tree import arrange_and_draw_subtree


class Node:
    """
    Binary tree node.
    """

    INDENT = "  "

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.h_left = 0
        self.h_right = 0

    def is_leaf(self) -> bool:
        """
        Return true if the node is a leaf. False otherwise.
        """
        return self.left is None and self.right is None

    def __len__(self):
        return size(self)

    def __str__(self, level=0) -> str:
        node_str = f"{Node.INDENT * level}{self.value}"
        if not is_leaf(self):
            node_str += ":"
            if self.left:
                node_str += f"\n{self.left.__str__(level + 1)}"
            if self.right:
                node_str += f"\n{self.right.__str__(level + 1)}"
        return node_str


def size(node: Node):
    """
    Return the number of nodes in the subtree.
    """
    if node is None:
        return 0
    return 1 + size(node.left) + size(node.right)


def put(root: Optional[Node], value) -> Node:
    """
    Add a node with the giving value.
    """
    new_root, _ = _put_helper(root, value)
    return new_root


def find(node: Optional[Node], value) -> Optional[Node]:
    """
    Return a node with the giving value if it exits. None otherwise.
    """
    if node is None:
        return None
    if node.value > value:
        return find(node.left, value)
    if node.value < value:
        return find(node.right, value)
    return node


def pop(node: Node, value) -> Node:
    """
    Remove and return a node with the giving value.
    """
    if node is None:
        return None
    if value < node.value:
        node.left = pop(node.left, value)
    elif value > node.value:
        node.right = pop(node.right, value)
    else:
        if node.right is None:
            return node.left
        if node.left is None:
            return node.right
        target = node
        node = node_min(target.right)
        node.right = delete_min(target.right)
        node.left = target.left
        target.right = target.left = None
    return node


def node_min(node: Node):
    """
    Return the node with the minimum value in the subtree.
    """
    return node if node.left is None else node_min(node.left)


def delete_min(node: Node) -> Node:
    """
    Remove the node with the minimum value from the subtree and return the node.
    """
    if node.left is None:
        return node.right
    node.left = delete_min(node.left)
    return node


def is_bst(node: Node) -> bool:
    """
    Return True if node is the root of a binary search tree.
    """
    if node is None:
        return True
    if node.left is not None and node.value < node.left.value:
        return False
    if node.right is not None and node.value > node.right.value:
        return False
    return is_bst(node.left) and is_bst(node.right)


def _put_helper(root: Optional[Node], value) -> Tuple(Node, int):
    if root is None:
        return (Node(value), 0)
    if value < root.value:
        root.left, h_left = _put_helper(root.left, value)
        root.h_left = max(h_left + 1, root.h_left)
    if value > root.value:
        root.right, h_right = _put_helper(root.right, value)
        root.h_right = max(h_right + 1, root.h_right)
    if -2 < _balance_factor(root) < 2:
        return (root, _height(root))
    return _rebalance(root)


def _rebalance(node: Node):
    bf_ = _balance_factor(node)
    bf_right = _balance_factor(node.right)
    bf_left = _balance_factor(node.left)
    if bf_ == -2 and bf_right == -1:
        node = _single_left_rotation(node)
    elif bf_ == 2 and bf_left == 1:
        node = _single_right_rotation(node)
    elif bf_ == 2 and bf_left == -1:
        node = _left_right_rotation(node)
    elif bf_ == -2 and bf_right == 1:
        node = _right_left_rotation(node)
    return (node, _height(node))


def _balance_factor(node: Node):
    return node.h_left - node.h_right if node else 0


def _height(node: Node):
    if node is None:
        return -1
    node.h_left = _height(node.left) + 1
    node.h_right = _height(node.right) + 1
    return max(node.h_left, node.h_right)


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
def _single_left_rotation(node_p: Node) -> Node:
    node_q = node_p.right
    node_p.right = node_q.left
    node_q.left = node_p
    return node_q


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
def _single_right_rotation(node_p: Node) -> Node:
    node_q = node_p.left
    node_p.left = node_q.right
    node_q.right = node_p
    return node_q


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
def _left_right_rotation(node_p: Node) -> Node:
    node_p.left = _single_left_rotation(node_p.left)
    return _single_right_rotation(node_p)


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
def _right_left_rotation(node_p: Node) -> Node:
    node_p.right = _single_right_rotation(node_p.right)
    return _single_left_rotation(node_p)


# GUI


class App:
    """
    tk app.
    """

    def __init__(self):
        # Make a sentinel root.
        self.root = None
        self._run_tests()

        # Make the tkinter window.
        self.window = tk.Tk()
        self.window.title("SortedBinaryNode")
        self.window.protocol("WM_DELETE_WINDOW", self._kill_callback)
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
        self.window.bind_all("<Control-a>", self._ctrl_a_pressed)
        self.window.bind_all("<Control-p>", self._ctrl_p_pressed)
        self.window.bind_all("<Control-f>", self._ctrl_f_pressed)

        # Draw the initial tree.
        self._draw_tree()

        self.window.focus_force()
        self.window.mainloop()

    def _kill_callback(self):
        """
        A callback to destroy the tkinter window.
        """
        self.window.destroy()

    def _draw_tree(self):
        # Remove any previous widgets.
        self.canvas.delete("all")
        if self.root is not None:
            arrange_and_draw_subtree(self.root, self.canvas, 10, 10)

    def _ctrl_a_pressed(self, _event):
        self.add_value()

    def add_value(self):
        """
        Add a value to the tree.
        """
        if new_string := self.value_entry.get():
            self.value_entry.delete(0, "end")
            self.value_entry.focus_set()
            try:
                new_value = int(new_string)
                self.root = put(self.root, new_value)
                self._draw_tree()
            except ValueError as ex:
                messagebox.showinfo(
                    "Find Error", f"Value {new_string} must be an integer.\n{ex}"
                )

    def _ctrl_p_pressed(self, _event):
        self.pop_value()

    def pop_value(self):
        """
        Remove a value from the tree.
        """
        if target_string := self.value_entry.get():
            self.value_entry.delete(0, "end")
            self.value_entry.focus_set()

            try:
                target = int(target_string)
                self.root = pop(self.root, target)
                _height(self.root)
                self._draw_tree()
            except ValueError as ex:
                messagebox.showinfo(
                    "Pop Error", f"Value {target_string} must be an integer.\n{ex}"
                )

    def _ctrl_f_pressed(self, _event):
        self.find_value()

    def find_value(self):
        """
        Find the value's node.
        """
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
                self._draw_tree()
            except ValueError as ex:
                messagebox.showinfo(
                    "Find Error", f"Value {target_string} must be an integer.\n{ex}"
                )

    def _run_tests(self):
        for value in [60, 35, 76, 21, 42, 71, 89, 17, 24, 74, 11, 23, 72, 75]:
            self.root = put(self.root, value)


if __name__ == "__main__":
    App()
