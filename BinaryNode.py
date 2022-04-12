class BinaryNode:
    def __init__(self, value, left_child = None, right_child = None):
        self.value = value
        self.left_child = left_child
        self.right_child = right_child

    def add_left(self, left):
        self.left_child = left

    def add_right(self, right):
        self.right_child = right

    def __str__(self):
        left_value = self.left_child.value if self.left_child else None
        right_value = self.right_child.value if self.right_child else None
        return f'{self.value}: {left_value} {right_value}'


def main():
    root = BinaryNode('Root',
        BinaryNode('A', BinaryNode('C'), BinaryNode('D')),
        BinaryNode('B', None, BinaryNode('E', BinaryNode('F')))
    )
    print(root)
    print(root.left_child)
    print(root.right_child)


if __name__ == '__main__':
    main()