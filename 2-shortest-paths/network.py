from __future__ import annotations

from typing import List

COMMENT = "#"


class Node:
    def __init__(self, index: int, pos_x: float, pos_y: float, text: str):
        self.index = index
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.text = text

    def to_string(self) -> str:
        return f"{self.pos_x},{self.pos_y},{self.text}"

    def __str__(self) -> str:
        return f"[{self.text}]"


class Link:
    def __init__(self, from_node: Node, to_node: Node, cost: int):
        self.from_node = from_node
        self.to_node = to_node
        self.cost = cost

    def to_string(self) -> str:
        return f"{self.from_node.index},{self.to_node.index},{self.cost}"

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

    def add_node_from_string(self, node_str: str):
        pos_x, pos_y, text = node_str.split(",")
        return self.add_node(float(pos_x), float(pos_y), text)

    def add_link(self, from_node: Node, to_node: Node, cost: int):
        link = Link(from_node, to_node, cost)
        self.links.append(link)
        return link

    def add_link_from_string(self, link_str: str):
        from_index, to_index, cost = (int(value) for value in link_str.split(","))
        return self.add_link(self.nodes[from_index], self.nodes[to_index], cost)

    def to_string(self) -> str:
        return "\n".join(
            [
                f"{len(self.nodes)} {COMMENT} Num nodes.",
                f"{len(self.links)} {COMMENT} Num links.",
                f"{COMMENT} Nodes.",
            ]
            + [node.to_string() for node in self.nodes]
            + [f"{COMMENT} Links."]
            + [link.to_string() for link in self.links]
        )

    def save_into_file(self, filename: str):
        with open(filename, "w", encoding="utf-8") as writer:
            writer.writelines(self.to_string())

    @staticmethod
    def load_from_file(filename: str) -> Network:
        network = Network()
        with open(filename, "r", encoding="utf-8") as reader:
            num_nodes = int(Network._parse(reader.readline()))
            num_links = int(Network._parse(reader.readline()))
            for line in range(num_nodes):
                if line := Network._parse(reader.readline()):
                    network.add_node_from_string(line)
            for line in range(num_links):
                if line := Network._parse(reader.readline()):
                    network.add_link_from_string(line)
        return network

    @staticmethod
    def _parse(line: str) -> str:
        if pos := line.find(COMMENT):
            line = line[:pos]
        return line.strip()
