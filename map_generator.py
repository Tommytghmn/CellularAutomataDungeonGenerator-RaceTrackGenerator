import random
import heapq

# Density is the percentage of floors expected in the grid and iterations is how many times we do cellular automata
# This will create a randomly generated dungeon and track avoiding the walls in the dungeon.
def create_dungeon(map_width, map_height, density, iterations):
    # This creates the noise grid to add randomness to the cellular automata
    def make_noise_grid():
        # Returns map_data object
        return [[1 if random.randint(1, 100) < density else 0 for j in range(map_width)] for i in range(map_height)] # WALLS
        # return [[0 for j in range(map_width)] for i in range(map_height)] # NO WALLS
    
    # This counts the number of neighbors to a cell where the cell is the middle of a square
    # The boxlength has to be odd to work
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
    for _ in range(iterations):
        dungeon_map = cell_auto(dungeon_map)

    # History made to keep track of the random points we want the track to flow through
    history = [[None for _ in range(2)] for _ in range(5)]

    # I want to make 5 random points on the map that can be connected with track portions
    countRandPts = 0
    # Keep track of how many points that are created to try to create the track. Some may fail due to proximity or landing on a floor
    count = 0
    # Loop until 5 accepted random points are found or if we are unable to find enough points.
    while countRandPts < 5 and count < 1000:
        # Increment count
        count += 1
        # Generate a random int for the x axis
        randX = random.randint(0, map_width - 1)
        # Generate a random int for the y axis
        randY = random.randint(0, map_height - 1)
        # Check if the current square is a floor
        if dungeon_map[randY][randX] == 0:
            # This means we are on the floor
            # If their is no random points or their are no points close to the current point then add it to the dungeon_map
            if countRandPts == 0 or check_for_points(dungeon_map, map_width, map_height, randX, randY):
                # Add the first race track point since their are none at this point
                dungeon_map[randY][randX] = 2
                # Update the history
                history[countRandPts][0] = randX
                history[countRandPts][1] = randY
                # Increment the count
                countRandPts += 1
                print(f"Point {countRandPts} placed at ({randX}, {randY})")
            else: 
                # This means that their are multiple points on the grid and this one would be added to close to one of them.
                print(f"Point rejected at ({randX}, {randY}) due to proximity.")
        else:
            # This means we are on the wall
            print(f"Point rejected at ({randX}, {randY}) because it is not on a floor.")
    # Send an error if their aren't 5 random points generated successfully
    if countRandPts < 5:
        raise ValueError("Failed to generate 5 valid points on the map")
    
    # Take the points from the history and converts them from a list[list] to list[tuple] so the coordinates are locked in and immutable
    points = [(history[i][0], history[i][1]) for i in range(5) if history[i][0] is not None]
    # If their are less than 5 points throw an error because we want 5 points to create the track
    if len(points) < 5:
        raise ValueError("Not enough points were generated to connect.")
    # Connect points returns the dungeon_map with the floors, track, and walls.
    # Also return the track segments so we can color them that way its easier to identify them
    dungeon_map, track_segments = connect_points(dungeon_map, points)
    # Once the dungeon map and track segments have been created return them
    return dungeon_map, track_segments

# This will check that points dont overlap one another and are spread out
def check_for_points(map_data, map_width, map_height, x, y):
    for ny in range(y - 2, y + 3): # This is two to the left through two to the right
            for nx in range(x - 2, x + 3): # This is two above through two below
                # Check the points that are in the range and the map
                if 0 <= nx < map_width and 0 <= ny < map_height:
                    # If any of the points in the range are a track square then we don't want to add another one this close so return false
                    if map_data[ny][nx] == 2:
                        return False
    # None of the track squares were too close so return true
    return True

# Algorithm for finding paths to connect the track squares
def a_star(map_data, start, end, crossTracks=False):
    # Store the current height and width based on the map
    map_height = len(map_data)
    map_width = len(map_data[0])

    # Initialize a priority queue that is a list of potential moves
    priority_queue = []
    # This adds the first point to the priority queue with a cost of 0 and starting at the start
    # (priority queue min heap, (cost to reach current node from the start + manhattan distance estimate, coordinates of start point))
    # ( [], f_cost = g_cost + h_cost, (x, y) )
    heapq.heappush(priority_queue, (0, start))

    # Initialize a dictionary to hold the g_cost which is the cost to reach current node from the start for the current square
    # { (x, y): cost}
    g_cost = {start: 0}
    # Create an empty dictionary to contain the paths
    # This is used to backtrack through the points to create the path once we reach the goal square
    paths = {}

    # This function checks the squares up, down, left, and right of the current square to see if they are valid moves
    def check_moves(x, y):
        # Initialize an list to store the moves
        moves = []
        # Loop through potential moves to see if they are valid moves
        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]: # Directions: Up, Down, Left, Right
            # Calculate the actual squares next to the current point
            ny, nx = y + dy, x + dx
            # Check that the move we are checking is in the map and isn't a wall
            if 0 <= nx < map_width and 0 <= ny < map_height and map_data[ny][nx] != 1:
                # This move is valid so add it to the list of moves
                moves.append((nx, ny))
        # Return the list of valid moves for the current square
        return moves
    
    # While their is content in our priority_queue keep looping
    while priority_queue:
        # This removes the top node from the heap which has the lowest f_cost from the priority_queue
        # this f_cost is unused here but we need it in order to get current
        # current is the square being processed currently
        _, current = heapq.heappop(priority_queue)

        # If the current square is equal to the end square then we can stop trying to create a track
        if current == end:
            # Initialize path as a empty list to construct the path back
            path = []
            # Loop back from the end node to the start node since the current node is at the end
            while current in paths:
                # Add the current node to the path being created
                path.append(current)
                # Go back to the square the current path came from in order to backtrack through the map
                current = paths[current]
            # Return the path flipped since we backtracked through the map and now we want to go forward.
            return path[::-1]
        
        # Loop over the potential moves based on the current square in order to find the most optimal move
        for move in check_moves(*current):
            # Get the g_cost = cost to get to the current square + get the cost of the move that is being processed currently
            temp_g_cost = g_cost[current] + get_cost(map_data[move[1]][move[0]], crossTracks)
            # If the move isn't in g_cost yet or the temp_g_cost is less than the g_cost then replace it with temp_g_cost since its more optimal
            if move not in g_cost or temp_g_cost < g_cost[move]:
                # Add this move to g_cost since it hasn't been added yet or if this move has a lower cost than the current move that is stored
                g_cost[move] = temp_g_cost
                # f_cost = g_cost + h_cost
                # calculate the f_cost by adding the cost to get to the square and the estimated distance to the desired endpoint
                f_cost = temp_g_cost + manhattan_distance(move, end)
                # Add this move to the priority queue/heap and enter the f_cost for its priority and the moves coordinates
                heapq.heappush(priority_queue, (f_cost, move))
                # Add the move square to the paths dictionary since it can be reached from the current node
                paths[move] = current
    return None # No path found

# This estimates the distance between 2 squares on the map not taking into account obstacles
def manhattan_distance(a, b): # Accepts the start point and end point as a list
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
                
# Apply costs to floor, walls, and tracks so we can use an algorithm to connect the points
def get_cost(square, crossTracks=False): # Accepts a point as an list
    if square == 2: # Track square
        return float('inf') if not crossTracks else 1
    elif square == 0: # Floor square
        return 2
    else: # Wall
        return float('inf') # Walls should not be passable so make the cost high
    
# This connects the random points on the track to create the track
def connect_points(map_data, points):
        # Check that points are provided that way we have something to work with.
        if not points:
            raise ValueError("No points provided to connect.")
        
        # Keeps track of how many connections each random point has in a dictionary environment
        connections = {point: 0 for point in points}
        # Initialize a list of unconnected points to keep track of which ones need to be connected
        unconnected_points = points[:]
        # Initialize a list of connected points
        connected_points = []
        # Initialize a dictionary of track segments
        track_segments = {}

        # Get rid of the first unconnected point and put it in the current points
        current_point = unconnected_points.pop(0)
        # Add the first connected point to the list of connected points
        connected_points.append(current_point)
        # red, white, orange, yellow, pink
        colors = [(255, 0, 0), (255, 255, 255), (255, 165, 0), (255, 255, 0), (255, 0, 255)]
        # Initialize the color index so we can iterate through the colors
        color_index = 0

        # Keep looping through the unconnected_points list until their are no more points
        while unconnected_points:
            # Initialize the closest point to none since its the first point
            closest_point = None
            # Set the closest distance to infinity that way the first point found will already be better in terms of distance
            closest_distance = float('inf')
            # Loop through all of the unconnected points
            for point in unconnected_points:
                # Calculate the distance using manhattan distance to get the lowest distance
                distance = manhattan_distance(current_point, point)
                # Prioritize the distance that is the lowest
                if distance < closest_distance:
                    # Update the new closest distance
                    closest_distance = distance
                    # Update the closest point
                    closest_point = point

            # Create a debatably optimal path between two of the random points
            path = a_star(map_data, current_point, closest_point, crossTracks=False)
            # If the path exists between the points then proceed if not fail
            if path:
                # For each square on the path if the map is a floor make it into a track
                for x, y in path:
                    # if the map is a floor make it into a track
                    if map_data[y][x] == 0:
                        # Make the map a 2 which represents a track square
                        map_data[y][x] = 2
                        # Set the colors different for each segment of the track
                        # This is done by storing the squares color in a list based on the coordinates
                        track_segments[(x, y)] = colors[color_index]
                # Increment the dictionary's totals tracking the amount of connections for the current point and closest point
                connections[current_point] += 1
                connections[closest_point] += 1
            else:
                # Throw an error since their was no possible path from the current point to the closest point
                raise ValueError(f"No path found between points {current_point} and {closest_point}.")

            # Make the current point become the closest point since thats how the next connection is decided
            current_point = closest_point
            # Add the new current point to the list of connected points since its being used now
            connected_points.append(current_point)
            # Remove the new connected point from the list of unconnected points since its connected now
            unconnected_points.remove(current_point)

            # Increment the color index each time the track segment changes
            color_index += 1

        # The last point of connected points is considered the start
        start = connected_points[-1]
        # The first point of connected points is considered the end
        end = connected_points[0]
        # If the start and the end are different points when proceed if not then fail because their wouldn't be a path between them.
        if start != end:
             # Create a debatably optimal path between two of the random points
            path = a_star(map_data, start, end, crossTracks=False)
            if path:
                # For each square on the path if the map is a floor make it into a track
                for x, y in path:
                    # if the map is a floor make it into a track
                    if map_data[y][x] == 0:
                        # Make the map a 2 which represents a track square
                        map_data[y][x] = 2
                        # Set the colors different for each segment of the track
                        # This is done by storing the squares color in a list based on the coordinates
                        track_segments[(x, y)] = colors[color_index]
            else:
                # If the start and the end are 
                raise ValueError(f"No path found between points {start} and {end}.")  
        
        print(f"Connecting points: {connected_points}")
        print(f"Closing loop between {start} and {end}")  
        # Return the map data as numbers to be interpreted when coloring the grid and color the track using the track segments
        return map_data, track_segments
    
