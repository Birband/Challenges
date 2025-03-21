import random
from src.entities.node import Node


class Ant:
    def __init__(self, id: int, nodes: list, alpha: float, beta: float):
        self.id = id
        self.nodes = nodes
        self.alpha = alpha
        self.beta = beta
        self.pheromones = {
            (min(node1.id, node2.id), max(node1.id, node2.id)): 1
            for node1 in nodes
            for node2 in nodes
            if node1 != node2
        }
        self.node = nodes[0]
        self.visited_nodes = [self.node]
        self.node_destination = self.select_next_node()
        self.x = self.node.x
        self.y = self.node.y
        self.completed = False

    def path_length(self):
        self.visited_nodes.append(self.node)
        length = sum(
            self.distance_between_nodes(
                self.visited_nodes[i], self.visited_nodes[i + 1]
            )
            for i in range(len(self.visited_nodes) - 1)
        )
        self.visited_nodes.pop()
        return length

    def distance_between_nodes(self, node_start: Node, node_end: Node):
        return (
            (node_start.x - node_end.x) ** 2 + (node_start.y - node_end.y) ** 2
        ) ** 0.5

    def distance_to_destination(self, node: Node):
        return ((self.x - node.x) ** 2 + (self.y - node.y) ** 2) ** 0.5

    def restart(self, pheromones: dict | None = None):
        self.node = self.nodes[0]
        self.x = self.node.x
        self.y = self.node.y
        self.pheromones = (
            pheromones
            if pheromones
            else {
                (min(node1, node2), max(node1, node2)): 1
                for node1 in self.nodes
                for node2 in self.nodes
                if node1 != node2
            }
        )
        self.visited_nodes = [self.node]
        self.node_destination = self.select_next_node()
        self.completed = False

    def select_next_node(self):
        available_nodes = [
            node for node in self.nodes if node not in self.visited_nodes
        ]
        probabilities = [
            self.pheromones[(min(self.node.id, node.id), max(self.node.id, node.id))]
            ** self.alpha
            * (1 / (self.distance_between_nodes(self.node, node) + 1e-10)) ** self.beta
            for node in available_nodes
        ]
        total = sum(probabilities)
        probabilities = [p / total for p in probabilities]
        return random.choices(available_nodes, probabilities)[0]

    def move(self, time_step: float):
        distance_to_destination = self.distance_to_destination(self.node_destination)
        total_distance = self.distance_between_nodes(self.node, self.node_destination)
        speed = total_distance * time_step if time_step > 0 else total_distance

        if distance_to_destination <= speed:
            self.node = self.node_destination
            self.x = self.node.x
            self.y = self.node.y
            if self.node not in self.visited_nodes:
                self.visited_nodes.append(self.node)
            if len(self.visited_nodes) == len(self.nodes):
                self.completed = True
                return True, self.path_length()
            self.node_destination = self.select_next_node()
        else:
            direction_x = (self.node_destination.x - self.x) / distance_to_destination
            direction_y = (self.node_destination.y - self.y) / distance_to_destination
            self.x += direction_x * speed
            self.y += direction_y * speed

        return False, 0

    def __str__(self):
        return f"Ant {self.id} at ({self.x}, {self.y})"
