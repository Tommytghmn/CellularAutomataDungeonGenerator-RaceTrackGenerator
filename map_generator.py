import random

# Density is the percentage of floors expected in the grid
def create_dungeon(map_width, map_height, density, iterations):
    def make_noise_grid():
        return [[1 if random.randint(1, 100) < density else 0 for j in range(map_width)] for i in range(map_height)]
    
    def num_neighbors(map_data, x, y):
        num = 0
        for nx in range(x - 1, x + 2): # This is one to the left through one to the right
            for ny in range(y - 1, y + 2): # This is one above through one below
                if nx == x and ny == y:
                    continue
                if 0 <= nx < map_width and 0 <= ny < map_height:
                    num += map_data[ny][nx]
                else:
                    num += 1
        return num
    
    def cell_auto(map_data):
        new_map_data = [row[:] for row in map_data]
        for y in range(map_height):
            for x in range(map_width):
                neighbors = num_neighbors(map_data, x, y)
                if neighbors > 4:
                    new_map_data[y][x] = 1
                else:
                    new_map_data[y][x] = 0
        return new_map_data
    
    dungeon_map = make_noise_grid()
    for k in range(iterations):
        dungeon_map = cell_auto(dungeon_map)

    return dungeon_map