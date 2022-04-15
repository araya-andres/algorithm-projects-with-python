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


def find_value(root: BinaryNode, value) -> None:
    if root.find_node(value):
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

    print('Preorder:  ', end='')
    for node in root.traverse_preorder():
        print(f'{node.value} ', end='')
    print()

    print('Inorder:  ', end='')
    for node in root.traverse_inorder():
        print(f'{node.value} ', end='')
    print()

    print('Postorder:  ', end='')
    for node in root.traverse_postorder():
        print(f'{node.value} ', end='')
    print()

    print('Breadth-First:  ', end='')
    for node in root.traverse_breadth_first():
        print(f'{node.value} ', end='')
    print()

if __name__ == "__main__":
    main()
