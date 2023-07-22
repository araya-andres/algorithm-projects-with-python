from network import Network


def test_node_str():
    node = Network().add_node(0, 1, "A")
    assert str(node) == "[A]"


def test_link_str():
    network = Network()
    node_a = network.add_node(0, 0, "A")
    node_b = network.add_node(1, 1, "B")
    link_a_b = network.add_link(node_a, node_b, 10)
    assert str(link_a_b) == "[A] --> [B] (10)"
