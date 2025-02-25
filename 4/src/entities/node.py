import random
class Node:
    def __init__(self, id: int, x: int, y: int):
        self.x = x
        self.y = y
        self.id = id

    def __str__(self):
        return f"Node {self.id} at ({self.x}, {self.y})"

def generate_nodes_randomly(node_count: int, width: int, height: int, max_proximity: int = 20, seed: int = None):
    nodes = []

    if seed:
        random.seed(seed)

    while len(nodes) < node_count:
        i = len(nodes)
        x = random.randint(0, width)
        y = random.randint(0, height)

        if not any([((node.x - x) ** 2 + (node.y - y) ** 2) ** 0.5 < max_proximity for node in nodes]):
            nodes.append(Node(i, x, y))

    return nodes
    