import pygame
from map_generator import create_dungeon

CELL_LENGTH = 10
MAP_WIDTH = 100
MAP_HEIGHT = 100
SCREEN_WIDTH = MAP_WIDTH * CELL_LENGTH
SCREEN_HEIGHT = MAP_HEIGHT * CELL_LENGTH
DENSITY = 57
ITERATIONS = 5

COLOR_FLOOR = (220, 220, 220)
COLOR_WALL = (30, 30, 30)

def make_grid(screen, dungeon_map):
    for y, row in enumerate(dungeon_map):
        for x, cell in enumerate(row):
            grid = pygame.Rect(x * CELL_LENGTH, y * CELL_LENGTH, CELL_LENGTH, CELL_LENGTH)
            color = COLOR_WALL if cell == 1 else COLOR_FLOOR
            pygame.draw.rect(screen, color, grid)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Dungeon Generator/Track Generator")
    clock = pygame.time.Clock()

    dungeon_map = create_dungeon(MAP_WIDTH, MAP_HEIGHT, DENSITY, ITERATIONS)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        make_grid(screen, dungeon_map)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()