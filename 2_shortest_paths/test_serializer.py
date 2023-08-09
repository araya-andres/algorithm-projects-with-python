import pytest
import serializer
from network import Network
from pytest import approx
from serializer import DeserializationException

from common.point import Point

TEST_FILES_PATH = "2_shortest_paths/test_files/"


@pytest.fixture
def network() -> Network:
    network = Network()
    node_a = network.add_node(Point(0, 0), "A")
    node_b = network.add_node(Point(1, 1), "B")
    network.add_link(node_a, node_b, 1)
    return network


def test_node_to_string(network):
    assert serializer._node_to_string(network.nodes[0]) == "0,0,A"


def test_link_to_string(network):
    assert serializer._link_to_string(network.links[0]) == "0,1,1"


def test_network_to_string(network):
    assert serializer._network_to_string(network) == "\n".join(
        [
            "2 # Num nodes.",
            "1 # Num links.",
            "# Nodes.",
            "0,0,A",
            "1,1,B",
            "# Links.",
            "0,1,1",
        ]
    )


def test_node_from_string(network):
    node = serializer._add_node(network, "0,1,C")
    assert node.index == 2
    assert node.pos.x == approx(0)
    assert node.pos.y == approx(1)
    assert node.text == "C"


def test_parse_a_node_string_with_no_text_raises_an_exception(network):
    with pytest.raises(DeserializationException) as ex:
        serializer._add_node(network, "1,0")
    assert str(ex.value) == "Invalid node string: '1,0'"


def test_parse_a_node_string_with_a_non_numerical_value_for_x_raises_an_exception(
    network,
):
    with pytest.raises(DeserializationException) as ex:
        serializer._add_node(network, "foo,0,bar")
    assert str(ex.value) == "Invalid node string: 'foo,0,bar'"


def test_parse_a_node_string_with_a_non_numerical_value_for_y_raises_an_exception(
    network,
):
    with pytest.raises(DeserializationException) as ex:
        serializer._add_node(network, "0,foo,bar")
    assert str(ex.value) == "Invalid node string: '0,foo,bar'"


def test_get_a_link_from_string(network):
    link_str = "1,0,1"
    link_b_a = serializer._add_link(network, link_str)
    assert str(link_b_a) == "[B] --> [A] (1)"


def test_parse_a_link_string_with_no_cost_raises_an_exception(network):
    with pytest.raises(DeserializationException) as ex:
        serializer._add_link(network, "0,1")
    assert str(ex.value) == "Invalid link string: '0,1'"


def test_parse_a_link_string_with_a_non_numeric_value_raises_an_exception(network):
    with pytest.raises(DeserializationException) as ex:
        serializer._add_link(network, "1,foo,1")
    assert str(ex.value) == "Invalid link string: '1,foo,1'"


def test_parse_a_link_string_with_index_out_of_bounds_raises_an_exception(network):
    with pytest.raises(DeserializationException) as ex:
        serializer._add_link(network, "1,2,3")
    assert str(ex.value) == "Node index out of bounds: '1,2,3'"


def test_save_and_load_from_file(network):
    filename = TEST_FILES_PATH + "test.net"
    serializer.save_into_file(network, filename)
    new_network = serializer.load_from_file(filename)
    assert len(new_network.nodes) == 2
    assert len(new_network.links) == 1
    assert str(new_network.links[0]) == "[A] --> [B] (1)"


def test_load_an_empty_file_raises_an_exception():
    with pytest.raises(DeserializationException) as ex:
        serializer.load_from_file(TEST_FILES_PATH + "empty.txt")
    assert str(ex.value) == "Could not find the number of nodes"


def test_load_a_file_with_only_commented_lines_raises_an_exception():
    with pytest.raises(DeserializationException) as ex:
        serializer.load_from_file(TEST_FILES_PATH + "only-commented-lines.txt")
    assert str(ex.value) == "Could not find the number of nodes"


def test_load_a_file_with_only_the_number_of_nodes_raises_an_exception():
    with pytest.raises(DeserializationException) as ex:
        serializer.load_from_file(TEST_FILES_PATH + "only-node-num.txt")
    assert str(ex.value) == "Could not find the number of links"


def test_load_a_file_with_zero_nodes():
    network = serializer.load_from_file(TEST_FILES_PATH + "zero.txt")
    assert len(network.nodes) == 0
    assert len(network.links) == 0


def test_load_a_file_with_less_nodes_than_expected_raises_an_exception():
    with pytest.raises(DeserializationException) as ex:
        serializer.load_from_file(TEST_FILES_PATH + "missing-nodes.txt")
    assert str(ex.value) == "Could not find the number of nodes expected (1/2)"


def test_load_a_file_with_less_links_than_expected_raises_an_exception():
    with pytest.raises(DeserializationException) as ex:
        serializer.load_from_file(TEST_FILES_PATH + "missing-links.txt")
    assert str(ex.value) == "Could not find the number of links expected (0/1)"
