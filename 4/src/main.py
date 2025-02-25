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
SEED = 42
ALPHA = 1
BETA = 1
TIME_STEP = 1/60

def main():
    nodes = generate_nodes_randomly(NODES_COUNT, WIDTH, HEIGHT, MAX_PROXIMITY)
    ants = [Ant(i, nodes, ALPHA, BETA) for i in range(ANTS_COUNT)]
    
    pygame.init()
    screen = pygame.display.set_mode((720, 480))
    pygame.display.set_caption("Ants")
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        
        for node in nodes:
            pygame.draw.circle(screen, (255, 255, 255), (node.x, node.y), 5)
        
        completed_ants = 0
        for ant in ants:
            pygame.draw.circle(screen, (255, 0, 0), (ant.x, ant.y), 5)
            if not ant.completed:
                print(f"Ant {ant.id} moving to {ant.node_destination}")
                ant.move(TIME_STEP)
            else:
                print(f"Ant {ant.id} completed the path")
                completed_ants += 1

        if completed_ants == len(ants):      
            for ant in ants:
                ant.restart()

        # Flip -> obrazowanie na ekranie :)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()