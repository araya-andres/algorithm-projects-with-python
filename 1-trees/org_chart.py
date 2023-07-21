from __future__ import annotations

import tkinter as tk
from typing import List, Optional, Tuple


class NaryNode:
    indent = "  "
    box_half_width = 40
    box_half_height = 20
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

    def is_leaf(self) -> bool:
        return len(self.children) == 0

    def is_twig(self) -> bool:
        return all(c.is_leaf() for c in self.children)

    def __str__(self, level=0) -> str:
        s = f"{NaryNode.indent * level}{self.value}:"
        for child in self.children:
            s += f"\n{child.__str__(level + 1)}"
        return s

    def arrange_subtree(
        self, xmin: float, ymin: float
    ) -> Tuple[float, float, float, float]:
        cx = NaryNode.box_half_width + xmin
        cy = NaryNode.box_half_height + ymin
        child_y = cy + NaryNode.box_half_height + NaryNode.y_spacing

        if self.is_leaf():
            self.center = (cx, cy)
            self.subtree_bounds = (
                cx - NaryNode.box_half_width,
                cy - NaryNode.box_half_height,
                cx + NaryNode.box_half_width,
                cy + NaryNode.box_half_height,
            )
        elif self.is_twig():
            child_x = xmin + 2 * NaryNode.x_spacing
            for i, child in enumerate(self.children):
                if i > 0:
                    child_y += NaryNode.y_spacing
                _, _, x1, y1 = child.arrange_subtree(child_x, child_y)
                child_y += 2 * NaryNode.box_half_height
            self.center = (cx, cy)
            self.subtree_bounds = (xmin, ymin, x1, y1)
        else:
            subtree_height = 0
            width = 0
            for i, child in enumerate(self.children):
                if i > 0:
                    width += NaryNode.x_spacing
                _, y0, x1, y1 = child.arrange_subtree(xmin + width, child_y)
                subtree_height = max(subtree_height, y1 - y0)
                width = x1 - xmin
            self.center = (xmin + width / 2, cy)
            self.subtree_bounds = (xmin, ymin, xmin + width, child_y + subtree_height)

        return self.subtree_bounds

    def draw_subtree_links(self, canvas: tk.Canvas) -> None:
        if self.is_twig():
            xv, y0, _, y1 = self.subtree_bounds
            xv += NaryNode.x_spacing
            canvas.create_line(xv, y0, xv, y1 - NaryNode.box_half_height)
            for child in self.children:
                cx, cy = child.center
                canvas.create_line(xv, cy, cx, cy)
        else:
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
        canvas.create_rectangle(
            cx - NaryNode.box_half_width,
            cy - NaryNode.box_half_height,
            cx + NaryNode.box_half_width,
            cy + NaryNode.box_half_height,
            fill="white" if self.is_leaf() else "salmon",
        )
        canvas.create_text(
            cx, cy, text=str(self.value), justify="center", font=("arial", 8)
        )
        for child in self.children:
            child.draw_subtree_nodes(canvas)
        # Outline the subtree for debugging.
        # canvas.create_rectangle(self.subtree_bounds, outline="red")

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


a = NaryNode(
    "Generi Gloop",
    [
        NaryNode(
            "R&D",
            [
                NaryNode("Applied"),
                NaryNode("Basic"),
                NaryNode("Advanced"),
                NaryNode("Sci Fi"),
            ],
        ),
        NaryNode(
            "Sales",
            [
                NaryNode("Inside\nSales"),
                NaryNode("Outside\nSales"),
                NaryNode("B2B"),
                NaryNode("Consumer"),
                NaryNode("Account\nManagement"),
            ],
        ),
        NaryNode(
            "Professional\nServices",
            [
                NaryNode(
                    "HR",
                    [
                        NaryNode("Training"),
                        NaryNode("Hiring"),
                        NaryNode("Equity"),
                        NaryNode("Discipline"),
                    ],
                ),
                NaryNode(
                    "Accounting",
                    [
                        NaryNode("Payroll"),
                        NaryNode("Billing"),
                        NaryNode("Reporting"),
                        NaryNode("Opacity"),
                    ],
                ),
                NaryNode(
                    "Legal",
                    [
                        NaryNode("Compliance"),
                        NaryNode("Progress\nPrevention"),
                        NaryNode("Bail\nServices"),
                    ],
                ),
            ],
        ),
    ],
)

print(a)


def kill_callback():
    """A callback to destroy the tkinter window."""
    window.destroy()


# Make the tkinter window.
window = tk.Tk()
window.title("org_chart")
window.protocol("WM_DELETE_WINDOW", kill_callback)
window.geometry("720x440")

canvas = tk.Canvas(window, bg="white", borderwidth=2, relief=tk.SUNKEN)
canvas.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Draw the tree.
a.arrange_and_draw_subtree(canvas, 10, 10)

window.focus_force()
window.mainloop()
