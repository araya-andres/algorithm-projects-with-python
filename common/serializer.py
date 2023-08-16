"""
Serielizer for the Network class
"""
from common.network import Link, Network, Node
from common.point import Point

COMMENT = "#"


class DeserializationException(Exception):
    """
    Exception for deserialization errors
    """


def _node_to_string(node: Node) -> str:
    return f"{int(node.pos.x)},{int(node.pos.y)},{node.text}"


def _link_to_string(link: Link) -> str:
    return f"{link.from_node.index},{link.to_node.index},{link.cost}"


def _network_to_string(network) -> str:
    return "\n".join(
        [
            f"{len(network.nodes)} {COMMENT} Num nodes.",
            f"{len(network.links)} {COMMENT} Num links.",
            f"{COMMENT} Nodes.",
        ]
        + [_node_to_string(node) for node in network.nodes]
        + [f"{COMMENT} Links."]
        + [_link_to_string(link) for link in network.links]
    )


def save_into_file(network, filename: str):
    """
    Save the network to a file
    """
    with open(filename, "w", encoding="utf-8") as writer:
        writer.writelines(_network_to_string(network))


def _add_node(network: Network, node_str: str, radius: int = Node.LARGE_RADIUS) -> Node:
    try:
        pos_x, pos_y, text = node_str.split(",")
        return network.add_node(Point(float(pos_x), float(pos_y)), text, radius=radius)
    except ValueError as ex:
        raise DeserializationException(f"Invalid node string: '{node_str}'") from ex


def _add_link(network: Network, link_str: str) -> Link:
    try:
        from_index, to_index, cost = (int(value) for value in link_str.split(","))
        n_nodes = len(network.nodes)
        if not (0 <= from_index < n_nodes and 0 <= to_index < n_nodes):
            raise DeserializationException(f"Node index out of bounds: '{link_str}'")
        from_node = network.nodes[from_index]
        to_node = network.nodes[to_index]
        return network.add_link(from_node, to_node, cost)
    except ValueError as ex:
        raise DeserializationException(f"Invalid link string: '{link_str}'") from ex


def _remove_comments(line: str) -> str:
    pos = line.find(COMMENT)
    if pos > -1:
        line = line[:pos]
    return line.strip()


def _get_value(reader, exception_msg) -> int:
    while True:
        if line := reader.readline():
            if clean_line := _remove_comments(line):
                return int(clean_line)
        else:
            raise DeserializationException(exception_msg)


def _parse_lines(reader, num_lines, parser, exception_msg):
    i = 0
    while i < num_lines:
        if line := reader.readline():
            if clean_line := _remove_comments(line):
                parser(clean_line)
                i += 1
        else:
            raise DeserializationException(f"{exception_msg} ({i}/{num_lines})")


def load_from_file(filename: str) -> Network:
    """
    Load a network from a file
    """
    network = Network()
    with open(filename, "r", encoding="utf-8") as reader:
        num_nodes = _get_value(
            reader, exception_msg="Could not find the number of nodes"
        )
        if num_nodes == 0:
            return network
        radius = Node.LARGE_RADIUS
        if num_nodes > Network.BIG:
            radius = Node.SMALL_RADIUS
        num_links = _get_value(
            reader, exception_msg="Could not find the number of links"
        )
        _parse_lines(
            reader,
            num_lines=num_nodes,
            parser=lambda line: _add_node(network, node_str=line, radius=radius),
            exception_msg="Could not find the number of nodes expected",
        )
        _parse_lines(
            reader,
            num_lines=num_links,
            parser=lambda line: _add_link(network, link_str=line),
            exception_msg="Could not find the number of links expected",
        )
    return network
