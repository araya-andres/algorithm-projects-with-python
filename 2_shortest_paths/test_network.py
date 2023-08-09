import pytest
from network import Network

from common.point import Point


@pytest.fixture
def network() -> Network:
    test_network = Network()
    node_a = test_network.add_node(Point(0, 0), "A")
    test_network.add_link(node_a, test_network.add_node(Point(0, 1), "B"), 1)
    test_network.add_link(node_a, test_network.add_node(Point(1, 1), "C"), 1)
    assert not any(node.is_start_node for node in test_network.nodes)
    assert not any(node.is_end_node for node in test_network.nodes)
    return test_network


def test_nodes():
    node = Network().add_node(Point(0, 1), "A")
    assert len(node.links) == 0
    assert str(node) == "[A]"


def test_links():
    test_network = Network()
    node_a = test_network.add_node(Point(0, 0), "A")
    node_b = test_network.add_node(Point(0, 1), "B")
    link_a_b = test_network.add_link(node_a, node_b, 10)
    assert len(node_a.links) == 1
    assert len(node_b.links) == 0
    assert str(link_a_b) == "[A] --> [B] (10)"


def test_start_point(network):
    node_a = network.nodes[0]
    network.select_start_node(node_a)
    assert node_a.is_start_node


def test_end_point(network):
    node_a = network.nodes[0]
    network.select_end_node(node_a)
    assert node_a.is_end_node
