from __future__ import annotations
from typing import List


def nary_tree_as_str(node: NaryNode, level: int) -> str:
    indent = "  " * level
    if node is None:
        return f"{indent}{node}"
    elif len(node.children) > 0:
        children = "\n".join(
            nary_tree_as_str(child, level + 1) for child in node.children
        )
        return f"{indent}{node.value}:\n{children}"
    else:
        return f"{indent}{node.value}:"


class NaryNode:
    def __init__(self, value, children: List[NaryNode] = []):
        self.value = value
        self.children = children

    def add_child(self, child_node: NaryNode):
        self.children.append(child_node)

    def find_node(self, value) -> Optional[NaryNode]:
        if value == self.value:
            return self
        for child in self.children:
            node = child.find_node(value)
            if node:
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


    def __str__(self) -> str:
        return nary_tree_as_str(self, 0)


def find_value(root: NaryNode, value) -> None:
    if root.find_node(value):
        print(f"Found {value}")
    else:
        print(f"Value {value} not found")


def main():
    root = NaryNode(
        "Root",
        [
            NaryNode(
                "A",
                [
                    NaryNode(
                        "D",
                        [
                            NaryNode("G"),
                        ],
                    ),
                    NaryNode("E"),
                ],
            ),
            NaryNode("B"),
            NaryNode(
                "C",
                [
                    NaryNode(
                        "F",
                        [
                            NaryNode("H"),
                            NaryNode("I"),
                        ],
                    )
                ],
            ),
        ],
    )
    print(root)
    print(root.children[0])
    print()
    # Find some values.
    find_value(root, "Root")
    find_value(root, "E")
    find_value(root, "F")
    find_value(root, "Q")

    print('Preorder:  ', end='')
    for node in root.traverse_preorder():
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
