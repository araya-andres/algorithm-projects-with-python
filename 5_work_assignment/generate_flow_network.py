"""
Generate grid-shaped networks.
"""
import argparse
import random

from common.network import Network, Node
from common.point import Point
from common.serializer import save_into_file


def _capacity() -> int:
    return random.randint(1, 5)


def build_grid_network(width: int, height: int, num_rows: int, num_cols) -> Network:
    """
    Build a grid-shaped network with num_rows rows and num_cols columns.
    The nodes should be arranged in an area width pixels wide and height pixels tall.
    The capacity of a link is a value set at random between 1 and 5.
    """
    network = Network()

    # Add nodes
    num_nodes = num_rows * num_cols
    radius = Node.LARGE_RADIUS if num_nodes < Network.BIG else Node.SMALL_RADIUS
    dist_x = (width - 4 * radius) / (num_cols - 1) if num_cols > 1 else 0
    dist_y = (height - 4 * radius) / (num_rows - 1) if num_rows > 1 else 0
    pos_x, pos_y = 2 * radius, 2 * radius
    i = 0
    for _ in range(num_rows):
        for _ in range(num_cols):
            network.add_node(Point(pos_x, pos_y), str(i))
            pos_x += dist_x
            i += 1
        pos_x = 2 * radius
        pos_y += dist_y

    # Link nodes
    col, row = 0, 0
    nodes = network.nodes
    for i in range(num_nodes):
        if col < num_cols - 1:
            network.add_link(nodes[i], nodes[i + 1], _capacity())
        if row < num_rows - 1:
            network.add_link(nodes[i], nodes[i + num_cols], _capacity())
        col += 1
        if col >= num_cols:
            col = 0
            row += 1

    return network


def _main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument("width", type=int)
    parser.add_argument("height", type=int)
    parser.add_argument("rows", type=int)
    parser.add_argument("cols", type=int)
    args = parser.parse_args()
    network = build_grid_network(args.width, args.height, args.rows, args.cols)
    save_into_file(network, args.filename)


if __name__ == "__main__":
    _main()
