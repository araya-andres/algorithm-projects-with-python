"""
Traverse tree
"""


def preorder(node):
    """
    Pre-order traversal.
    """
    yield node
    if node.left:
        yield from preorder(node.left)
    if node.right:
        yield from preorder(node.right)


def inorder(node):
    """
    In-order traversal.
    """
    if node.left:
        yield from inorder(node.left)
    yield node
    if node.right:
        yield from inorder(node.right)


def postorder(node):
    """
    Post-order traversal.
    """
    if node.left:
        yield from postorder(node.left)
    if node.right:
        yield from postorder(node.right)
    yield node


def breadth_first(node):
    """
    Breadth-First traversal.
    """
    queue = [node]
    while queue:
        node = queue.pop(0)
        yield node
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
