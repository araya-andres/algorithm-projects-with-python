"""
Generate grid-shaped networks.
"""
import argparse
import random

from network import Network, Node
from serializer import save_into_file


def _cost(lenght: int) -> int:
    return int(lenght * (1 + random.randint(0, 200) / 1000))


def build_grid_network(width: int, height: int, num_rows: int, num_cols) -> Network:
    """
    Build a grid-shaped network with num_rows rows and num_cols columns.
     The nodes should be arranged in an area width pixels wide and height pixels tall.
    The cost of a link equal to its length times a random value between 1.0 and 1.2.
    """
    network = Network()

    # Add nodes
    num_nodes = num_rows * num_cols
    _r = Node.LARGE_RADIUS if num_nodes < Network.BIG else Node.SMALL_RADIUS
    _dx = (width - 4 * _r) / (num_cols - 1) if num_cols > 1 else 0
    _dy = (height - 4 * _r) / (num_rows - 1) if num_rows > 1 else 0
    pos_x = 2 * _r
    pos_y = 2 * _r
    index = 0
    for _ in range(num_rows):
        for _ in range(num_cols):
            network.add_node(int(pos_x), int(pos_y), str(index))
            pos_x += _dx
            index += 1
        pos_x = 2 * _r
        pos_y += _dy

    # Link nodes
    col = 0
    row = 0
    nodes = network.nodes
    for i in range(num_nodes):
        if col > 0:
            network.add_link(nodes[i], nodes[i - 1], _cost(_dx))
        if col < num_cols - 1:
            network.add_link(nodes[i], nodes[i + 1], _cost(_dx))
        if row > 0:
            network.add_link(nodes[i], nodes[i - num_cols], _cost(_dy))
        if row < num_rows - 1:
            network.add_link(nodes[i], nodes[i + num_cols], _cost(_dy))
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
