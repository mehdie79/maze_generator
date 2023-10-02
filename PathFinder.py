import queue
import time
import Map
import math

class PathFinder:
    def __init__(self, network) -> None:
        self.network = network

    def find_start(self, maze, start):
        for i, row in enumerate(maze):
            for j, value in enumerate(row):
                
                if value == start:
                    return i, j
        
        return None

    def find_path_depth_first_search(self, maze): 
        start = "O"
        end = "X"
        start_position = self.find_start(maze, start)
        stack = []
        stack.append((start_position, [start_position]))
        visited = set()
        my_path = None
        while not len(stack) == 0:
            current_position , path = stack.pop()
            row, col = current_position
            
            self.network.send_message("path_message")
            self.network.send_maze_map(path)
            time.sleep(0.2)

            if maze[row][col]== end:
                my_path = path
                break
            neighbors = self.find_neighbors(maze, row, col)
            for neighbor in neighbors:
                if neighbor in visited:
                    continue
                
                r, c = neighbor
                if maze[r][c] == "#": # WALL
                    continue
                new_path = path + [neighbor]
                stack.append((neighbor, new_path))
                visited.add(neighbor)

        for i in range(len(my_path)):
            self.network.send_message("actual_path_message")
            self.network.send_maze_map(my_path[i])
            time.sleep(0.3)

        return my_path

    def find_path_breadth_first_search(self,maze):
        start = "O"
        end = "X"
        start_position = self.find_start(maze, start)
        q= queue.Queue()
        q.put((start_position, [start_position]))
        visited = set()
        my_path = None
        while not q.empty():
            current_position , path = q.get()
            row, col = current_position
            
            self.network.send_message("path_message")
            self.network.send_maze_map(path)
            time.sleep(0.2)
            if maze[row][col]== end:
                my_path = path
                break
            neighbors = self.find_neighbors(maze, row, col)
            for neighbor in neighbors:
                if neighbor in visited:
                    continue
                
                r, c = neighbor
                if maze[r][c] == "#": # WALL
                    continue
                new_path = path + [neighbor]
                q.put((neighbor, new_path))
                visited.add(neighbor)

        for i in range(len(my_path)):
            self.network.send_message("actual_path_message")
            self.network.send_maze_map(my_path[i])
            time.sleep(0.3)

        return my_path

        
    def find_dijkstra_search(self, maze):
        map_pbj = Map.Map(maze)
        start_position = map_pbj.start_position
        map_variable = map_pbj.my_map
        priority_queue = queue.PriorityQueue()
        row_index, column_index = start_position
        end_row_index, end_column_index = map_pbj.end_position
        map_variable[row_index][column_index].distanceTo = 0
        priority_queue.put((map_variable[row_index][column_index].distanceTo, map_variable[row_index][column_index], [start_position]))

        while priority_queue.not_empty:
            priority, node, current_path = priority_queue.get()
            node.isVisited = True
            self.network.send_message("path_message")
            self.network.send_maze_map(current_path)
            
            if node == map_variable[end_row_index][end_column_index]:
                break
            for i in range(len(node.neighbors)):
                path = current_path
                if node.neighbors[i].isVisited == True:
                    continue
                first_node = node.neighbors[i].distanceTo
                second_node = (node.distanceTo+ node.weight[i])
                if first_node > second_node:
                    path.append((node.neighbors[i].row, node.neighbors[i].column))
                    node.neighbors[i].parent = node
                    node.neighbors[i].distanceTo=node.distanceTo+ node.weight[i] 
                priority_queue.put((node.neighbors[i].distanceTo, node.neighbors[i], path))

                

        path = []

        current_path = map_variable[end_row_index][end_column_index]

        while current_path != map_variable[row_index][column_index]:
            path.insert(0, (current_path.row, current_path.column))
            current_path = current_path.parent
        
        path.insert(0, (row_index,column_index))

        for i in range(len(path)):
            self.network.send_message("actual_path_message")
            self.network.send_maze_map(path[i])
            time.sleep(0.3)

        return path

    def distance(self, row_index1, column_index1, row_index2, column_index2):
        return math.sqrt((row_index1 - row_index2) * (row_index1 - row_index2) + (column_index1 - column_index2) * (column_index1 - column_index2))

    def heuristic(self, node_one, node_two):
        return self.distance(node_one.row, node_one.column, node_two.row, node_two.column)
        
    def a_star_search_algorithm(self, maze):
        map_pbj = Map.Map(maze)
        start_position = map_pbj.start_position
        map_variable = map_pbj.my_map
        priority_queue = queue.PriorityQueue()
        row_index, column_index = start_position
        end_row_index, end_column_index = map_pbj.end_position
        map_variable[row_index][column_index].distanceTo = 0
        map_variable[row_index][column_index].global_goal = self.heuristic(map_variable[row_index][column_index], map_variable[end_row_index][end_column_index])
        priority_queue.put((map_variable[row_index][column_index].global_goal, map_variable[row_index][column_index], [start_position]))
        
        while priority_queue.qsize() != 0:
            while priority_queue.qsize() != 0:
                priority, node, current_path = priority_queue.get()
                if map_variable[node.row][node.column].isVisited == True:
                    continue
                else:
                    priority_queue.put((priority, node, current_path))
                    break
            
            if priority_queue.qsize == 0:
                break

            priority, node, current_path = priority_queue.get()
            map_variable[node.row][node.column].isVisited = True
            self.network.send_message("path_message")
            self.network.send_maze_map(current_path)
            
            for i in range(len(node.neighbors)):
                path = current_path   
                if map_variable[node.neighbors[i].row][node.neighbors[i].column].isVisited == True:
                    continue
                first_node = node.neighbors[i].distanceTo # Neighbour Local goal
                second_node = (node.distanceTo+ self.distance(node.row, node.column,node.neighbors[i].row, node.neighbors[i].column))
                if first_node > second_node:
                    path.append((node.neighbors[i].row, node.neighbors[i].column))
                    node.neighbors[i].parent = node
                    node.neighbors[i].distanceTo= (node.distanceTo+ self.distance(node.row, node.column,node.neighbors[i].row, node.neighbors[i].column))
                    node.neighbors[i].global_goal = node.neighbors[i].distanceTo + self.heuristic(node.neighbors[i],  map_variable[end_row_index][end_column_index])
                
                priority_queue.put((node.neighbors[i].global_goal, node.neighbors[i], path))

            
        path = []
        current_path = map_variable[end_row_index][end_column_index]

        while current_path != map_variable[row_index][column_index]:
            path.insert(0, (current_path.row, current_path.column))
            current_path = current_path.parent
        
        path.insert(0, (row_index,column_index))

        for i in range(len(path)):
            self.network.send_message("actual_path_message")
            self.network.send_maze_map(path[i])
            time.sleep(0.3)

        return path

    def find_neighbors(self, maze, row, column):
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