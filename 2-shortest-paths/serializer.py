"""
Serielizer for the Network class
"""
from network import Link, Network, Node

COMMENT = "#"


class DeserializationException(Exception):
    """
    Exception for deserialization errors
    """


def _node_to_string(node: Node) -> str:
    return f"{node.pos_x},{node.pos_y},{node.text}"


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


def _add_node(network: Network, node_str: str) -> Node:
    try:
        pos_x, pos_y, text = node_str.split(",")
        return network.add_node(int(pos_x), int(pos_y), text)
    except ValueError as ex:
        raise DeserializationException(f"Invalid node string: '{node_str}'") from ex


def _add_link(network: Network, link_str: str) -> Link:
    if len(network.nodes) == 0:
        raise DeserializationException("Can not have a link in an empty network")
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


def _parse(line: str) -> str:
    pos = line.find(COMMENT)
    if pos > -1:
        line = line[:pos]
    return line.strip()


def load_from_file(filename: str) -> Network:
    """
    Load a network from a file
    """
    network = Network()
    with open(filename, "r", encoding="utf-8") as reader:
        num_nodes = 0
        while True:
            if line := reader.readline():
                if parsed_line := _parse(line):
                    num_nodes = int(parsed_line)
                    break
            else:
                raise DeserializationException("Could not find the number of nodes")
        if num_nodes == 0:
            return network
        num_links = 0
        while True:
            if line := reader.readline():
                if parsed_line := _parse(line):
                    num_links = int(parsed_line)
                    break
            else:
                raise DeserializationException("Could not find the number of links")
        i = 0
        while i < num_nodes:
            if line := reader.readline():
                if node_str := _parse(line):
                    _add_node(network, node_str)
                    i += 1
            else:
                msg = f"Could not find the number of nodes expected ({i}/{num_nodes})"
                raise DeserializationException(msg)
        i = 0
        while i < num_links:
            if line := reader.readline():
                if link_str := _parse(line):
                    _add_link(network, link_str)
                    i += 1
            else:
                msg = f"Could not find the number of links expected ({i}/{num_links})"
                raise DeserializationException(msg)
    return network
