import random

# Density is the percentage of floors expected in the grid
def create_dungeon(map_width, map_height, density, iterations):
    # This creates the noise grid to add randomness to the cellular automata
    def make_noise_grid():
        return [[1 if random.randint(1, 100) < density else 0 for j in range(map_width)] for i in range(map_height)]
    
    # This counts the number of neighbors to a cell where the cell is the middle of a 3 by 3 square
    def num_neighbors(map_data, x, y):
        # Initialize the number of neighbors
        num = 0
        for nx in range(x - 1, x + 2): # This is one to the left through one to the right
            for ny in range(y - 1, y + 2): # This is one above through one below
                if nx == x and ny == y:
                     # This is the current cell so do nothing
                    continue
                if 0 <= nx < map_width and 0 <= ny < map_height:
                    # This is in the map and now we are counting if the neighboring cells are walls
                    num += map_data[ny][nx]
                else:
                    # This counts cells outside the map width/length that are still neighbors as walls
                    num += 1
        # Return the number of neighbors that are walls for a particular cell
        return num
    
    # This uses cellular automation to change the look of the cells based on the number of neighboring floors
    def cell_auto(map_data):
        # Create the new grid row by row from the cells in map_data
        new_map_data = [row[:] for row in map_data]
        # Loop through the y axis
        for y in range(map_height):
            # Loop through the x axis
            for x in range(map_width):
                # Get the count of neighbors for the current cell
                neighbors = num_neighbors(map_data, x, y)
                # Check if the number of neighbors is greater than 4
                if neighbors > 4:
                    # If the number of walls is greater than 4 then add a wall at the current cell
                    new_map_data[y][x] = 1
                else:
                    # If the number of walls is 4 or less than add a floor at the current cell
                    new_map_data[y][x] = 0
        # Return the new adjusted map
        return new_map_data
    
    # Create the noise grid for randomness
    dungeon_map = make_noise_grid()
    # Do the cellular automata multiple times to keep adjusting the map
    for k in range(iterations):
        dungeon_map = cell_auto(dungeon_map)

    # Once the dungeon map has been created return it
    return dungeon_map