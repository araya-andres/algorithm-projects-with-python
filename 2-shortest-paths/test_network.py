import pytest
from network import Network


@pytest.fixture
def network() -> Network:
    network = Network()
    node_a = network.add_node(0, 0, "A")
    network.add_link(node_a, network.add_node(0, 1, "B"), 1)
    network.add_link(node_a, network.add_node(1, 1, "C"), 1)
    assert not any(node.is_start_node for node in network.nodes)
    assert not any(node.is_end_node for node in network.nodes)
    assert not any(link.is_in_path for link in network.links)
    assert not any(link.is_in_tree for link in network.links)
    return network


def test_nodes():
    node = Network().add_node(0, 1, "A")
    assert len(node.links) == 0
    assert str(node) == "[A]"


def test_links():
    network = Network()
    node_a = network.add_node(0, 0, "A")
    node_b = network.add_node(0, 1, "B")
    link_a_b = network.add_link(node_a, node_b, 10)
    assert len(node_a.links) == 1
    assert len(node_b.links) == 0
    assert str(link_a_b) == "[A] --> [B] (10)"


def test_start_point(network):
    node_a = network.nodes[0]
    network.select_start_node(node_a)
    assert node_a.is_start_node
    assert all(link.is_in_tree for link in node_a.links)


def test_end_point(network):
    node_a = network.nodes[0]
    network.select_end_node(node_a)
    assert node_a.is_end_node
    assert all(link.is_in_path for link in node_a.links)
