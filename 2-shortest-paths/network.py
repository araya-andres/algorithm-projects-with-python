from __future__ import annotations

import math
from tkinter import Canvas
from typing import List, Optional


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

    def is_visible(self):
        return (
            (self.from_node.index < self.to_node.index)
            or self.is_in_path
            or self.is_in_tree
        )

    def draw(self, canvas: Canvas):
        if not self.is_visible():
            return
        witdh = 1
        color = "black"
        if self.is_in_tree:
            witdh = 5
            color = "green"
        if self.is_in_path:
            witdh = 5
            color = "red"
        _x0, _y0 = self.from_node.pos_x, self.from_node.pos_y
        _x1, _y1 = self.to_node.pos_x, self.to_node.pos_y
        canvas.create_line(_x0, _y0, _x1, _y1, width=witdh, fill=color)

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
    BIG: int = 100
    LABEL_CORRECTING: int = 0
    LABEL_SETTING: int = 1

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

    def add_link(self, from_node: Node, to_node: Node, cost: int) -> Link:
        link = Link(from_node, to_node, cost)
        self.links.append(link)
        return link

    def select_start_node(self, node: Node) -> Node:
        node.is_start_node = True
        if self.start_node:
            self.start_node.is_start_node = False
        self.start_node = node
        for link in self.links:
            link.is_in_path = False
            link.is_in_tree = False

    def select_end_node(self, node: Node) -> Node:
        node.is_end_node = True
        if self.end_node:
            self.end_node.is_end_node = False
        self.end_node = node
        for link in self.links:
            link.is_in_path = False
            link.is_in_tree = False

    def check_for_path(self, algorithm_idx: int):
        if self.start_node is None:
            return
        links_in_tree = [
            self.find_path_tree_label_correcting,
            self.find_path_tree_label_setting,
        ][algorithm_idx]()
        if self.end_node:
            self.find_path(links_in_tree)

    def find_path_tree_label_setting(self) -> List[Optional[Link]]:
        processed: List[Node] = []
        links: List[Optional[Link]] = [None] * len(self.nodes)
        costs: List[float] = [float("inf")] * len(self.nodes)

        node = self.start_node
        costs[node.index] = 0
        while node is not None:
            cost = costs[node.index]
            for link in node.links:
                new_cost = cost + link.cost
                i = link.to_node.index
                if new_cost < costs[i]:
                    link.is_in_tree = True
                    if prev_link := links[i]:
                        prev_link.is_in_tree = False
                    links[i] = link
                    costs[i] = new_cost
            processed.append(node)
            node = self.find_lowest_cost_node(costs, processed)

        return links

    def find_path_tree_label_correcting(self):
        pass

    def find_lowest_cost_node(
        self, costs: List[float], processed: List[Node]
    ) -> Optional[Node]:
        lowest_cost = float("inf")
        lowest_cost_node = None
        for i, cost in enumerate(costs):
            node = self.nodes[i]
            if cost < lowest_cost and node not in processed:
                lowest_cost = cost
                lowest_cost_node = node
        return lowest_cost_node

    def find_path(self, links_in_tree: List[Optional[Link]]):
        cost = 0
        link = links_in_tree[self.end_node.index]
        while link is not None:
            cost += link.cost
            link.is_in_path = True
            link = links_in_tree[link.from_node.index]
        print(f"cost={cost}")

    def draw(self, canvas: Canvas):
        draw_labels = len(self.nodes) < Network.BIG
        for link in self.links:
            link.draw(canvas)
        if draw_labels:
            for link in self.links:
                link.draw_label(canvas)
        for node in self.nodes:
            node.draw(canvas, draw_labels)
