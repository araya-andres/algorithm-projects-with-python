class NaryNode:
    def __init__(self, value, children=[]):
        self.value = value
        self.children = children

    def add_child(self, child_node):
        self.children.append(child_node)

    def __str__(self):
        children = ' '.join(child.value for child in self.children)
        return f'{self.value}: {children}'


def main():
    root = NaryNode('Root', [
        NaryNode('A', [
            NaryNode('D'),
            NaryNode('E'),
        ]),
        NaryNode('B'),
        NaryNode('C', [
            NaryNode('F', [
                NaryNode('H'),
                NaryNode('I'),
            ])
        ]),
    ])
    print(root)
    print(root.children[0])
    print(root.children[1])


if __name__ == '__main__':
    main()