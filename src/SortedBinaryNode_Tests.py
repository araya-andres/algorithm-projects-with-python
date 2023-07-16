import pytest
import SortedBinaryNode


def test_the_size_of_an_empty_tree_is_zero():
    root = None
    assert SortedBinaryNode.size(root) == 0


def test_add_a_value():
    value = 42
    root = SortedBinaryNode.put(None, value)
    assert SortedBinaryNode.size(root) == 1
    assert root.value == value
    assert root.left == None
    assert root.right == None


def test_find_a_value():
    values = [1, 2, 3]
    root = None
    for x in values:
        root = SortedBinaryNode.put(root, x)
    for x in values:
        assert SortedBinaryNode.find(x, root) is not None


def test_find_returns_none_if_the_value_is_not_present():
    root = None
    for x in [2, 1, 3]:
        root = SortedBinaryNode.put(root, x)
    assert SortedBinaryNode.find(666, root) is None


def test_traverse_in_order_when_the_values_are_inserted_in_order():
    n = 100
    root = None
    for x in range(n):
        root = SortedBinaryNode.put(root, x)
    assert len(root) == n
    prev = None
    for node in SortedBinaryNode.traverse_inorder(root):
        if prev:
            prev.value < node.value
        prev = node


def test_traverse_in_order_when_the_values_are_inserted_reversed_in_order():
    n = 100
    root = None
    for x in reversed(range(n)):
        root = SortedBinaryNode.put(root, x)
    assert len(root) == n
    prev = None
    for node in SortedBinaryNode.traverse_inorder(root):
        if prev:
            prev.value < node.value
        prev = node
