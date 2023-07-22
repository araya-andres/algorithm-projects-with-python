from network import Link, Network, Node

COMMENT = "#"


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
    with open(filename, "w", encoding="utf-8") as writer:
        writer.writelines(_network_to_string(network))


def _add_node(network: Network, node_str: str) -> Node:
    pos_x, pos_y, text = node_str.split(",")
    return network.add_node(int(pos_x), int(pos_y), text)


def _add_link(network: Network, link_str: str) -> Link:
    from_index, to_index, cost = (int(value) for value in link_str.split(","))
    return network.add_link(network.nodes[from_index], network.nodes[to_index], cost)


def _parse(line: str) -> str:
    pos = line.find(COMMENT)
    if pos > -1:
        line = line[:pos]
    return line.strip()


def load_from_file(filename: str) -> Network:
    network = Network()
    with open(filename, "r", encoding="utf-8") as reader:
        num_nodes = int(_parse(reader.readline()))
        num_links = int(_parse(reader.readline()))
        i = 0
        while i < num_nodes:
            if line := _parse(reader.readline()):
                _add_node(network, line)
                i += 1
        i = 0
        while i < num_links:
            if line := _parse(reader.readline()):
                _add_link(network, line)
                i += 1
    return network
