from __future__ import annotations

import math
from tkinter import Canvas
from typing import List


class Node:
    LARGE_RADIUS: int = 10
    SMALL_RADIUS: int = 5

    def __init__(
        self, index: int, pos_x: int, pos_y: int, text: str, radius=LARGE_RADIUS
    ):
        self.index = index
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.text = text
        self.links: List[Link] = []
        self.is_start_node = False
        self.is_end_node = False
        self.radius = radius

    def __str__(self) -> str:
        return f"[{self.text}]"

    def add_link(self, link: Link):
        self.links.append(link)

    def links_in_path(self, in_path: bool):
        for link in self.links:
            link.is_in_path = in_path

    def links_in_tree(self, in_tree: bool):
        for link in self.links:
            link.is_in_tree = in_tree

    def draw(self, canvas: Canvas, draw_label: bool):
        color = "white"
        if self.is_start_node:
            color = "pink"
        elif self.is_end_node:
            color = "lightblue1"
        _x, _y = self.pos_x, self.pos_y
        _r = self.radius
        canvas.create_oval(_x - _r, _y - _r, _x + _r, _y + _r, fill=color)
        if draw_label:
            canvas.create_text(_x, _y, text=self.text)


class Link:
    def __init__(self, from_node: Node, to_node: Node, cost: int):
        self.from_node = from_node
        self.to_node = to_node
        self.cost = cost
        self.is_in_path = False
        self.is_in_tree = False
        from_node.add_link(self)

    def __str__(self) -> str:
        return f"{self.from_node} --> {self.to_node} ({self.cost})"

    def draw(self, canvas: Canvas):
        witdh = 1
        color = "black"
        if self.is_in_path:
            witdh = 5
            color = "red"
        elif self.is_in_tree:
            witdh = 5
            color = "green"
        canvas.create_line(
            self.from_node.pos_x,
            self.from_node.pos_y,
            self.to_node.pos_x,
            self.to_node.pos_y,
            width=witdh,
            fill=color,
        )

    def draw_label(self, canvas: Canvas):
        _dx = self.to_node.pos_x - self.from_node.pos_x
        _dy = self.to_node.pos_y - self.from_node.pos_y
        angle = 180 * math.atan2(_dx, _dy) / math.pi - 90
        _x = 0.667 * self.from_node.pos_x + 0.333 * self.to_node.pos_x
        _y = 0.667 * self.from_node.pos_y + 0.333 * self.to_node.pos_y
        _r = Node.LARGE_RADIUS
        canvas.create_oval(_x - _r, _y - _r, _x + _r, _y + _r, fill="white", width=0)
        canvas.create_text(_x, _y, text=str(self.cost), angle=angle)


class Network:
    BIG = 100

    def __init__(self):
        self.nodes: List[Node] = []
        self.links: List[Link] = []
        self.start_node = None
        self.end_node = None

    def add_node(
        self, pos_x: int, pos_y: int, text: str, radius: int = Node.LARGE_RADIUS
    ) -> Node:
        index = len(self.nodes)
        node = Node(index, pos_x, pos_y, text, radius)
        self.nodes.append(node)
        return node

    def add_link(self, from_node: Node, to_node: Node, cost: int):
        link = Link(from_node, to_node, cost)
        self.links.append(link)
        return link

    def select_start_node(self, start_node):
        if self.start_node:
            self.start_node.is_start_node = False
            self.start_node.links_in_tree(False)
        self.start_node = start_node
        start_node.is_start_node = True
        start_node.links_in_tree(True)

    def select_end_node(self, end_node):
        if self.end_node:
            self.end_node.is_end_node = False
            self.end_node.links_in_path(False)
        self.end_node = end_node
        end_node.is_end_node = True
        end_node.links_in_path(True)

    def draw(self, canvas: Canvas):
        draw_labels = len(self.nodes) < Network.BIG
        for link in self.links:
            link.draw(canvas)
        if draw_labels:
            for link in self.links:
                link.draw_label(canvas)
        for node in self.nodes:
            node.draw(canvas, draw_labels)
