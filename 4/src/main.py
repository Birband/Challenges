# let's go!
import pygame
import sys

from src.entities.ant import Ant
from src.entities.node import Node, generate_nodes_randomly

ANTS_COUNT = 10
NODES_COUNT = 10
WIDTH = 720
HEIGHT = 480
MAX_PROXIMITY = 20
SEED = 44
ALPHA = 1
BETA = 7
TIME_STEP = 1/60
TRAIL_FADE_SPEED = 5
TRAIL_LENGTH = 128
TRAIL_PERSISTENCE = 0.7
TRAIL_PERIOD = 1
EVAPORATION = 0.75

def calculate_pheromones_and_best_path(ants, pheromones, evaporation):
    updated_pheromones = {edge: pheromone * evaporation for edge, pheromone in pheromones.items()}
    best_ant = None
    best_path_length = float('inf')

    for ant in ants:
        path_length = ant.path_length()
        if path_length < best_path_length:
            best_path_length = path_length
            best_ant = ant
        
    if best_ant:
        for i in range(len(best_ant.visited_nodes) - 1):
            edge = (best_ant.visited_nodes[i].id, best_ant.visited_nodes[i+1].id)
            updated_pheromones[edge] = updated_pheromones.get(edge, 0) + 1 / best_path_length

    return updated_pheromones, best_path_length, best_ant.visited_nodes if best_ant else []

def main():
    trail = [[] for _ in range(TRAIL_LENGTH)]
    nodes = generate_nodes_randomly(NODES_COUNT, WIDTH, HEIGHT, MAX_PROXIMITY)
    ants = [Ant(i, nodes, ALPHA, BETA) for i in range(ANTS_COUNT)]
    pheromones = {(min(node1.id, node2.id), max(node1.id, node2.id)): 1 for node1 in nodes for node2 in nodes if node1 != node2}
    best_path = float('inf')
    best_path_nodes = []
    
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Ants")
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((50, 50, 50))
        
        if pygame.time.get_ticks() % TRAIL_PERIOD == 0:
            for i, trail_segment in enumerate(trail):
                for j, point in enumerate(trail_segment):
                    opacity = int(255 * (j + 1) / TRAIL_LENGTH)
                    trail_surface = pygame.Surface((4, 4), pygame.SRCALPHA)
                    pygame.draw.circle(trail_surface, (255, 255, 255, opacity), (2, 2), 2)
                    screen.blit(trail_surface, point)

        for node in nodes:
            pygame.draw.circle(screen, (0, 255, 255), (node.x, node.y), 8)
        
        completed_ants = 0
        for i, ant in enumerate(ants):
            pygame.draw.circle(screen, (255, 123, 123), (ant.x, ant.y), 6)
            completed, _ = ant.move(TIME_STEP)
            if not completed:
                if len(trail[i]) < TRAIL_LENGTH:
                    trail[i].append((ant.x, ant.y))
                else:
                    trail[i].pop(0)
                    trail[i].append((ant.x, ant.y))
            else:
                completed_ants += 1

        if completed_ants == len(ants):      
            pheromones, path, path_nodes = calculate_pheromones_and_best_path(ants, pheromones, EVAPORATION)
            if path < best_path:
                best_path = path
                best_path_nodes = path_nodes
            for ant in ants:
                ant.restart(pheromones)
        
        if best_path_nodes:
            best_path_nodes.append(best_path_nodes[0])
            for i in range(len(best_path_nodes) - 1):
                pygame.draw.line(screen, (0, 255, 0), (best_path_nodes[i].x, best_path_nodes[i].y), (best_path_nodes[i+1].x, best_path_nodes[i+1].y), 2)
        
        font = pygame.font.Font(None, 18)
        text = font.render(f"Best path: {best_path:.2f}", True, (255, 255, 255))
        screen.blit(text, (0, 0))

        pygame.display.flip()
        clock.tick(600)

    pygame.quit()

if __name__ == "__main__":
    main()