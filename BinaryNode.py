def binary_tree_as_str(node, level):
    indent = '  ' * level
    if node is None:
        return f'{indent}{node}'
    elif node.has_children():
        left_child = binary_tree_as_str(node.left_child, level + 1)
        right_child = binary_tree_as_str(node.right_child, level + 1) 
        return f'{indent}{node.value}:\n{left_child}\n{right_child}'
    else:
        return f'{indent}{node.value}:'


class BinaryNode:
    def __init__(self, value, left_child = None, right_child = None):
        self.value = value
        self.left_child = left_child
        self.right_child = right_child

    def add_left(self, left):
        self.left_child = left

    def add_right(self, right):
        self.right_child = right

    def has_children(self):
        return self.left_child or self.right_child

    def __str__(self):
        return binary_tree_as_str(self, 0)


def main():
    root = BinaryNode('Root',
        BinaryNode('A', BinaryNode('C'), BinaryNode('D')),
        BinaryNode('B', None, BinaryNode('E', BinaryNode('F')))
    )
    print(root)


if __name__ == '__main__':
    main()