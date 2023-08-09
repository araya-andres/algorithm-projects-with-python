"""
Draw binary tree.
"""
from __future__ import annotations

from tkinter import Canvas
from typing import Tuple

RADIUS = 10  # Radius of a node’s circle.
X_SPACING = 20  # Horizontal distance between neighboring subtrees.
Y_SPACING = 20  # Vertical distance between parent and child subtrees.


def arrange_subtree(
    node, x_min: float, y_min: float
) -> Tuple[float, float, float, float]:
    """
    Calculate the position of the nodes of the subtree.
    """
    c_y = RADIUS + y_min

    if node.is_leaf():
        c_x = RADIUS + x_min
        node.center = (c_x, c_y)
        node.subtree_bounds = (x_min, y_min, c_x + RADIUS, c_y + RADIUS)
        return node.subtree_bounds

    child_x, child_y = x_min, Y_SPACING + c_y + RADIUS
    y_max = 0

    if node.left:
        _, _, x_max, y_max = arrange_subtree(node.left, child_x, child_y)
        child_x = x_max + X_SPACING
    if node.right:
        _, _, x_max, y_right = arrange_subtree(node.right, child_x, child_y)
        y_max = max(y_max, y_right)

    node.center = ((x_max + x_min) / 2, c_y)
    node.subtree_bounds = (x_min, y_min, x_max, y_max)
    return node.subtree_bounds


def draw_subtree_links(node, canvas: Canvas) -> None:
    """
    Draw subtree links.
    """
    if node.left:
        canvas.create_line(*node.center, *node.left.center)
        draw_subtree_links(node.left, canvas)
    if node.right:
        canvas.create_line(*node.center, *node.right.center)
        draw_subtree_links(node.right, canvas)


def draw_subtree_nodes(node, canvas: Canvas) -> None:
    """
    Draw subtree nodes.
    """
    if node is None:
        return
    c_x, c_y = node.center
    canvas.create_oval(
        c_x - RADIUS, c_y - RADIUS, c_x + RADIUS, c_y + RADIUS, fill="white"
    )
    canvas.create_text(c_x, c_y, text=str(node.value))
    draw_subtree_nodes(node.left, canvas)
    draw_subtree_nodes(node.right, canvas)
    # Outline the subtree for debugging.
    # canvas.create_rectangle(p.subtree_bounds, fill="", outline="red")


def arrange_and_draw_subtree(root, canvas: Canvas, x_min: float, y_min: float) -> None:
    """
    Draw subtree.
    """
    arrange_subtree(root, x_min, y_min)
    draw_subtree_links(root, canvas)
    draw_subtree_nodes(root, canvas)
