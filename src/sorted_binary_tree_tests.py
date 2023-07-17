"""
Unit tests for sort_binary_node.
"""
import sorted_binary_tree


def test_the_size_of_an_empty_tree_is_zero():
    root = None
    assert sorted_binary_tree.size(root) == 0


def test_add_a_value():
    value = 42
    root = sorted_binary_tree.put(None, value)
    assert sorted_binary_tree.size(root) == 1
    assert root.value == value
    assert root.left is None
    assert root.right is None


def test_find_a_value():
    values = [1, 2, 3]
    root = None
    for value in values:
        root = sorted_binary_tree.put(root, value)
    for value in values:
        assert sorted_binary_tree.find(root, value) is not None


def test_find_returns_none_if_the_value_is_not_present():
    root = None
    for value in [2, 1, 3]:
        root = sorted_binary_tree.put(root, value)
    assert sorted_binary_tree.find(root, 666) is None


def test_traverse_in_order_when_the_values_are_inserted_in_order():
    size = 100
    root = None
    for value in range(size):
        root = sorted_binary_tree.put(root, value)
    assert len(root) == size
    prev = None
    for node in sorted_binary_tree.traverse_inorder(root):
        if prev:
            assert prev.value < node.value
        prev = node


def test_traverse_in_order_when_the_values_are_inserted_reversed_in_order():
    size = 100
    root = None
    for value in reversed(range(size)):
        root = sorted_binary_tree.put(root, value)
    assert len(root) == size
    prev = None
    for node in sorted_binary_tree.traverse_inorder(root):
        if prev:
            assert prev.value < node.value
        prev = node
