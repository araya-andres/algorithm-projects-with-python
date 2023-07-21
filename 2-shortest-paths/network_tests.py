from network import Link, Network, Node


def test_represent_node_as_string():
    node = Network().add_node(0, 1, "A")
    assert str(node) == "[A]"
    assert node.to_string() == "0,1,A"


def test_make_node_from_string():
    node = Network().add_node_from_string("1,0,B")
    assert node.index == 0
    assert node.pos_x == 1
    assert node.pos_y == 0
    assert node.text == "B"


def test_represent_link_as_string():
    network = Network()
    node_a = network.add_node(0, 0, "A")
    node_b = network.add_node(1, 1, "B")
    link_a_b = network.add_link(node_a, node_b, 10)
    assert str(link_a_b) == "[A] --> [B] (10)"
    assert link_a_b.to_string() == "0,1,10"


def test_make_link_from_string():
    network = Network()
    network.add_node(0, 0, "A")
    network.add_node(1, 1, "B")
    link_str = "0,1,10"
    link_a_b = network.add_link_from_string(link_str)
    assert str(link_a_b) == "[A] --> [B] (10)"
    assert link_a_b.to_string() == link_str


def test_represent_network_as_string():
    network = Network()
    node_a = network.add_node(0, 0, "A")
    node_b = network.add_node(1, 1, "B")
    network.add_link(node_a, node_b, 10)
    assert network.to_string() == "\n".join(
        [
            "2 # Num nodes.",
            "1 # Num links.",
            "# Nodes.",
            "0,0,A",
            "1,1,B",
            "# Links.",
            "0,1,10",
        ]
    )
