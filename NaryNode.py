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

    def __str__(self) -> str:
        return nary_tree_as_str(self, 0)


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
                        ]),
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


if __name__ == "__main__":
    main()
