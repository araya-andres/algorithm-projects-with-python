from builder import build_grid_network
from pytest import approx


def test_build_one_by_one_grid():
    network = build_grid_network(40, 40, 1, 1)
    assert len(network.nodes) == 1
    assert len(network.links) == 0
    node = network.nodes[0]
    assert node.pos.x == approx(20)
    assert node.pos.y == approx(20)
    assert node.text == "0"


def test_build_two_by_one_grid():
    network = build_grid_network(140, 40, 1, 2)
    assert len(network.nodes) == 2
    assert len(network.links) == 2
    node_a, node_b = network.nodes
    assert node_a.pos.x == approx(20)
    assert node_a.pos.y == approx(20)
    assert node_a.text == "0"
    assert node_b.pos.x == approx(120)
    assert node_b.pos.y == approx(20)
    assert node_b.text == "1"
    link_a_b, link_b_a = network.links
    assert link_a_b.from_node == node_a
    assert link_a_b.to_node == node_b
    assert 100 <= link_a_b.cost <= 120
    assert link_b_a.from_node == node_b
    assert link_b_a.to_node == node_a
    assert 100 <= link_b_a.cost <= 120


def test_build_two_by_two_grid():
    network = build_grid_network(140, 140, 2, 2)
    assert len(network.nodes) == 4
    assert len(network.links) == 8
    assert network.nodes[0].pos.x == approx(20)
    assert network.nodes[0].pos.y == approx(20)
    assert network.nodes[1].pos.x == approx(120)
    assert network.nodes[1].pos.y == approx(20)
    assert network.nodes[2].pos.x == approx(20)
    assert network.nodes[2].pos.y == approx(120)
    assert network.nodes[3].pos.x == approx(120)
    assert network.nodes[3].pos.y == approx(120)


def test_build_three_by_three_grid():
    network = build_grid_network(240, 240, 3, 3)
    assert len(network.nodes) == 9
    assert len(network.links) == 24
    assert network.nodes[-1].pos.x == approx(220)
    assert network.nodes[-1].pos.y == approx(220)


def test_build_a_big_grid():
    network = build_grid_network(220, 220, 10, 10)
    assert len(network.nodes) == 100
    assert len(network.links) == 360
    assert network.nodes[0].pos.x == approx(10)
    assert network.nodes[0].pos.y == approx(10)
    assert network.nodes[-1].pos.x == approx(210)
    assert network.nodes[-1].pos.y == approx(210)
