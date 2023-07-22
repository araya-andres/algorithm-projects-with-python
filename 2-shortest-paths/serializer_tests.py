import serializer
from network import Network


def test_node_to_string():
    node = Network().add_node(0, 1, "A")
    assert serializer._node_to_string(node) == "0,1,A"


def test_link_to_string():
    network = Network()
    node_a = network.add_node(0, 0, "A")
    node_b = network.add_node(1, 1, "B")
    link_a_b = network.add_link(node_a, node_b, 10)
    assert serializer._link_to_string(link_a_b) == "0,1,10"


def test_network_to_string():
    network = Network()
    node_a = network.add_node(0, 0, "A")
    node_b = network.add_node(1, 1, "B")
    network.add_link(node_a, node_b, 10)
    assert serializer._network_to_string(network) == "\n".join(
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


def test_node_from_string():
    network = Network()
    node = serializer._add_node(network, "1,0,B")
    assert node.index == 0
    assert node.pos_x == 1
    assert node.pos_y == 0
    assert node.text == "B"


def test_link_from_string():
    network = Network()
    network.add_node(0, 0, "A")
    network.add_node(1, 1, "B")
    link_str = "0,1,10"
    link_a_b = serializer._add_link(network, link_str)
    assert str(link_a_b) == "[A] --> [B] (10)"


def test_save_and_load_from_file():
    network = Network()
    node_a = network.add_node(0, 0, "A")
    node_b = network.add_node(1, 1, "B")
    network.add_link(node_a, node_b, 10)
    filename = "test.net"
    serializer.save_into_file(network, filename)
    new_network = serializer.load_from_file(filename)
    assert serializer._network_to_string(network) == serializer._network_to_string(
        new_network
    )
