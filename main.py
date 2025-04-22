import pygame
from map_generator import create_dungeon

# Parameters for the look of the dungeon look
CELL_LENGTH = 6
MAP_WIDTH = 100
MAP_HEIGHT = 100
SCREEN_WIDTH = MAP_WIDTH * CELL_LENGTH
SCREEN_HEIGHT = MAP_HEIGHT * CELL_LENGTH
DENSITY = 57
ITERATIONS = 5

# Colors
COLOR_FLOOR = (50, 180, 0) # Green
COLOR_WALL = (0, 50, 180) # Blue
COLOR_DOT = (200, 0, 0) # Red
COLOR_TRACK = (180, 100, 0) # Orange?

# This will construct the dungeon inside the screen given using the given colors.
def make_grid(screen, dungeon_map):
    # This loops through the rows
    for y, row in enumerate(dungeon_map):
        # This loops through the cells on each row
        for x, cell in enumerate(row):
            # This creates the grid based on the parameters given for cell length
            grid = pygame.Rect(x * CELL_LENGTH, y * CELL_LENGTH, CELL_LENGTH, CELL_LENGTH)
            # This adjusts the color of the cells to black for walls and white for floors.
            color = COLOR_WALL if cell == 1 else COLOR_FLOOR
            # This takes the screen, colors, and grid and puts them together to make the dungeon map
            pygame.draw.rect(screen, color, grid)

def main():
    # Start using pygame to display the cellular automata/track generation
    pygame.init()
    # Initialize the screens dimensions
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # Set the caption of the screen
    pygame.display.set_caption("Dungeon Generator/Track Generator")

    # Create the dungeon map based on the parameters given
    dungeon_map = create_dungeon(MAP_WIDTH, MAP_HEIGHT, DENSITY, ITERATIONS)

    # This makes it so that the grid is displayed until we dont want it anymore.
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # This makes the dungeon map and puts it on the screen.
        make_grid(screen, dungeon_map)
        # This displays the dungeon map
        pygame.display.flip()

    # Quit out of pygame because we are no longer using it
    pygame.quit()

if __name__ == "__main__":
    main()