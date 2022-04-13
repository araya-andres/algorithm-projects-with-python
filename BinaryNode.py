from __future__ import annotations
from typing import Optional


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
    def __init__(
        self, value, left_child: BinaryNode = None, right_child: BinaryNode = None
    ):
        self.value = value
        self.left_child = left_child
        self.right_child = right_child

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
            node = self.left_child.find_node(value)
            if node:
                return node
        if self.right_child:
            node = self.right_child.find_node(value)
            if node:
                return node
        return None

    def __str__(self) -> str:
        return binary_tree_as_str(self, 0)


def find_value(tree: BinaryNode, value) -> None:
    if tree.find_node(value):
        print(f"Found {value}")
    else:
        print(f"Value {value} not found")


def main() -> None:
    root = BinaryNode(
        "Root",
        BinaryNode("A", BinaryNode("C"), BinaryNode("D")),
        BinaryNode("B", None, BinaryNode("E", BinaryNode("F"))),
    )

    print(root)
    print(root.left_child)

    print()

    find_value(root, "Root")
    find_value(root, "E")
    find_value(root, "F")
    find_value(root, "Q")
    find_value(root.right_child, "F")


if __name__ == "__main__":
    main()
