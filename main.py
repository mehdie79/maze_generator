import queue
import time
import MazeGenerator
import Network


network = Network.UDPServer("127.0.0.1", 12345)

def find_start(maze, start):
    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            
            if value == start:
                return i, j
    
    return None

def find_path_depth_first_search(maze): 
    start = "O"
    end = "X"
    start_position = find_start(maze, start)
    stack = []
    stack.append((start_position, [start_position]))
    visited = set()
    while not len(stack) == 0:
        current_position , path = stack.pop()
        row, col = current_position
        
        network.send_message("path_message")
        network.send_maze_map(path)
        time.sleep(0.2)

        if maze[row][col]== end:
            return path
        neighbors = find_neighbors(maze, row, col)
        for neighbor in neighbors:
            if neighbor in visited:
                continue
            
            r, c = neighbor
            if maze[r][c] == "#": # WALL
                continue
            new_path = path + [neighbor]
            stack.append((neighbor, new_path))
            visited.add(neighbor)

def find_path_breadth_first_search(maze):
    start = "O"
    end = "X"
    start_position = find_start(maze, start)
    q= queue.Queue()
    q.put((start_position, [start_position]))
    visited = set()
    while not q.empty():
        current_position , path = q.get()
        row, col = current_position
        
        network.send_message("path_message")
        network.send_maze_map(path)
        time.sleep(0.2)
        if maze[row][col]== end:
            return path
        neighbors = find_neighbors(maze, row, col)
        for neighbor in neighbors:
            if neighbor in visited:
                continue
            
            r, c = neighbor
            if maze[r][c] == "#": # WALL
                continue
            new_path = path + [neighbor]
            q.put((neighbor, new_path))
            visited.add(neighbor)

        

def find_neighbors(maze, row, column):
    neighbors = []

    if row > 0: # UP
        neighbors.append((row-1, column))
    if row+ 1 < len(maze): # Down
        neighbors.append((row+1, column))
    if column > 0: # LEFT
        neighbors.append((row, column - 1))
    if column+ 1 < len(maze[0]): # RIGHT
        neighbors.append((row, column + 1))
    
    return neighbors
    
    
algorithm_choices = {'depth-first-search': find_path_depth_first_search, 'breath-first-search': find_path_breadth_first_search}    


network.receive_data()
WIDTH, HEIGHT, ALGORITHM = network.get_info_client()

maze_generator = MazeGenerator.MazeGenerator(WIDTH, HEIGHT)

maze = maze_generator.generate_maze()
network.send_message("maze_message")
network.send_maze_map(maze)

time.sleep(1)

algorithm_choices[ALGORITHM](maze)

network.close_socket()


