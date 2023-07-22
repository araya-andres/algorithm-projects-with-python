from __future__ import annotations

from typing import List


class Node:
    def __init__(self, index: int, pos_x: int, pos_y: int, text: str):
        self.index = index
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.text = text

    def __str__(self) -> str:
        return f"[{self.text}]"


class Link:
    def __init__(self, from_node: Node, to_node: Node, cost: int):
        self.from_node = from_node
        self.to_node = to_node
        self.cost = cost

    def __str__(self) -> str:
        return f"{self.from_node} --> {self.to_node} ({self.cost})"


class Network:
    def __init__(self):
        self.nodes: List[Node] = []
        self.links: List[Link] = []

    def add_node(self, pos_x: float, pos_y: float, text: str) -> Node:
        index = len(self.nodes)
        node = Node(index, pos_x, pos_y, text)
        self.nodes.append(node)
        return node

    def add_link(self, from_node: Node, to_node: Node, cost: int):
        link = Link(from_node, to_node, cost)
        self.links.append(link)
        return link
