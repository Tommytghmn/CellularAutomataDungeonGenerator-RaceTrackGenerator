import pygame
from map_generator import create_dungeon
from map_generator import thickenTrack

# Parameters for the look of the dungeon look
# You can alter these to change the look of the track
CELL_LENGTH = 3 # 2
MAP_WIDTH = 200 # 250 or 500 if you have a monitor is better
MAP_HEIGHT = 200 # 250 or 500 if you have a monitor is better
SCREEN_WIDTH = MAP_WIDTH * CELL_LENGTH
SCREEN_HEIGHT = MAP_HEIGHT * CELL_LENGTH
DENSITY = 57
ITERATIONS = 6

# Colors
COLOR_FLOOR = (50, 180, 0) # Green
COLOR_WALL = (0, 50, 180) # Blue
COLOR_RANDOM_SQUARES = (0, 0, 0) # Black

# This will construct the dungeon inside the screen given using the given colors.
def make_grid(screen, dungeon_map, track_segments):
    # This loops through the rows 
    # y: the row index and 
    # row: the list of cells in the row
    for y, row in enumerate(dungeon_map):
        # This loops through the cells on each row
        # x: the column index 
        # cell: the value stored in the current cell (x, y)
        for x, cell in enumerate(row):
            # This creates the grid based on the parameters given for cell length
            grid = pygame.Rect(x * CELL_LENGTH, y * CELL_LENGTH, CELL_LENGTH, CELL_LENGTH)
            # This adjusts the color of the cells to black for walls and white for floors.
            if cell == 1:
                color = COLOR_WALL
            elif cell == 0:
                color = COLOR_FLOOR
            elif (x, y) in track_segments:
                color = track_segments[(x, y)]
            else:
                color = COLOR_RANDOM_SQUARES
            # This takes the screen, colors, and grid and puts them together to make the dungeon map
            pygame.draw.rect(screen, color, grid)



# DISCLAIMER sometimes it takes multiple runs to get a track that works. This is due to randomness and wanting the track to not overlap.
# The pink path connects back to the red path which is usually the most chaotic path since its trying to finish the loop. While the rest of the 
# paths are trying to get to the closest node to add to the track.
# Path starts at the node between pink and red and goes to red white all the way around the loop
def main():
    # Start using pygame to display the cellular automata/track generation
    pygame.init()
    # Initialize the screens dimensions
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # Set the caption of the screen
    pygame.display.set_caption("Dungeon Generator/Track Generator")

    # Create the dungeon map based on the parameters given
    # Color the segments so its easier to tell what is happening.
    dungeon_map, track_segments = create_dungeon(MAP_WIDTH, MAP_HEIGHT, DENSITY, ITERATIONS)

    # This makes it so that the grid is displayed until we dont want it anymore.
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Makes track wider
        dungeon_map = thickenTrack(dungeon_map, MAP_WIDTH, MAP_HEIGHT, track_segments)
        
        # This makes the dungeon map and puts it on the screen.
        make_grid(screen, dungeon_map, track_segments)
        # This displays the dungeon map
        pygame.display.flip()

    # Quit out of pygame because we are no longer using it
    pygame.quit()

if __name__ == "__main__":
    main()