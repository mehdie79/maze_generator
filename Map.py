
class Node:
    def __init__(self, weight, parent, neighbors, isFloor, isStartTile, isFinishTile, is_punishment, row_index, column_index):
        self.weight = weight
        self.parent = parent
        self.neighbors = neighbors
        self.isFloor = isFloor
        self.isStartTile = isStartTile
        self.isFinishTile = isFinishTile
        self.isVisited = False
        self.distanceTo = float('inf')
        self.row = row_index
        self.column = column_index
        # Only used for A* algorithm
        self.global_goal = None
        self.is_punishment = is_punishment

    def __eq__(self, other):
        if self.row == other.row and self.column == other.column:
            return True
        else:
            return False
    def __ne__(self, other):
        if self.row != other.row or self.column != other.column:
            return True
        else:
            return False
    def __lt__(self, other):
        # Compare nodes based on their global goal (for A* algorithm) or local goal(for Dijkstra Algorithm)
        if self.global_goal != None and other.global_goal != None:
            return self.global_goal < other.global_goal
    
        return self.distanceTo < other.distanceTo


class Map:

    def __init__(self, maze):

        self.my_map = []

        self.start_position= None

        self.end_position = None

        self.PUNISHMENT_WEIGHT = 3

        self.make_map(maze)
        
    def make_map(self, maze):

        for i in range(len(maze)):
            rows = []
            for j in range(len(maze[0])):
                is_endTile = False
                is_startTile = False
                is_floor = True 
                is_punishment = False
                if maze[i][j] == " " or maze[i][j] == "X" or maze[i][j] == "O" or maze[i][j] == "P":
                    is_floor = True 
                else:
                    is_floor = False

                if maze[i][j] == "P":
                    is_punishment = True

                if maze[i][j] == "X":
                    is_endTile = True
                    self.end_position = i, j
                elif maze[i][j] == "O":
                    is_startTile = True
                    self.start_position = i, j
                
                rows.append(Node(None, None, None, is_floor, is_startTile, is_endTile, is_punishment ,i, j))
            
            self.my_map.append(rows)
        
        for i in range(len(self.my_map)):
            for j in range(len(self.my_map[0])):
                neighbors, weight= self.find_neighbors(self.my_map, i, j)
                self.my_map[i][j].neighbors = neighbors
                self.my_map[i][j].weight = weight
        
        self.set_punishment_weights()


    def set_punishment_weights(self):

        for i in range(len(self.my_map)):
            for j in range(len(self.my_map[0])):
                if self.my_map[i][j].is_punishment:
                    if i > 0 and self.my_map[i-1][j].isFloor == True :  # Up
                        #self.my_map[i-1][j].weight[2] = self.PUNISHMENT_WEIGHT # Down
                        index =None
                        for k in range(len(self.my_map[i][j].neighbors)):
                            if self.my_map[i][j].neighbors[k] == self.my_map[i-1][j]:
                                index = k
                                break
                        self.my_map[i][j].weight[index] = self.PUNISHMENT_WEIGHT
                        index1 = None
                        for k in range(len(self.my_map[i-1][j].neighbors)):
                            if self.my_map[i-1][j].neighbors[k] == self.my_map[i][j]:
                                index1 = k
                                break
                                
                        self.my_map[i-1][j].weight[index1] = self.PUNISHMENT_WEIGHT
                        #self.my_map[i][j].weight[0] = self.PUNISHMENT_WEIGHT
                        
                       
                    
                    if j > 0 and self.my_map[i][j-1].isFloor == True : # Left
                        #self.my_map[i][j-1].weight[3] = self.PUNISHMENT_WEIGHT
                        index =None
                        for k in range(len(self.my_map[i][j].neighbors)):
                            if self.my_map[i][j].neighbors[k] == self.my_map[i][j-1]:
                                index = k
                                break
                        self.my_map[i][j].weight[index] = self.PUNISHMENT_WEIGHT
                        index1 = None
                        for k in range(len(self.my_map[i][j-1].neighbors)):
                            if self.my_map[i][j-1].neighbors[k] == self.my_map[i][j]:
                                index1 = k
                                break

                        self.my_map[i][j-1].weight[index1] = self.PUNISHMENT_WEIGHT
                        #self.my_map[i][j].weight[1] = self.PUNISHMENT_WEIGHT
                        
                    
                    if (i < len(self.my_map)-1) and self.my_map[i+1][j].isFloor == True: # Down
                        #self.my_map[i+1][j].weight[0] = self.PUNISHMENT_WEIGHT
                        index =None
                        for k in range(len(self.my_map[i][j].neighbors)):
                            if self.my_map[i][j].neighbors[k] == self.my_map[i+1][j]:
                                index = k
                                break
                        self.my_map[i][j].weight[index] = self.PUNISHMENT_WEIGHT
                        index1 = None
                        for k in range(len(self.my_map[i+1][j].neighbors)):
                            if self.my_map[i+1][j].neighbors[k] == self.my_map[i][j]:
                                index1 = k
                                break
                                
                        self.my_map[i+1][j].weight[index1] = self.PUNISHMENT_WEIGHT
                        #self.my_map[i][j].weight[2] = self.PUNISHMENT_WEIGHT

                    if j < (len(self.my_map[0])-1) and self.my_map[i][j+1].isFloor == True: # Right
                        #self.my_map[i][j+1].weight[1] = self.PUNISHMENT_WEIGHT
                        index =None
                        for k in range(len(self.my_map[i][j].neighbors)):
                            if self.my_map[i][j].neighbors[k] == self.my_map[i][j+1]:
                                index = k
                                break
                        self.my_map[i][j].weight[index] = self.PUNISHMENT_WEIGHT
                        index1 = None
                        for k in range(len(self.my_map[i][j+1].neighbors)):
                            if self.my_map[i][j+1].neighbors[k] == self.my_map[i][j]:
                                index1 = k
                                break
                                
                        self.my_map[i][j+1].weight[index1] = self.PUNISHMENT_WEIGHT
                        #self.my_map[i][j].weight[3] = self.PUNISHMENT_WEIGHT
                    

    def find_neighbors(self, my_map, i, j):
        neighbors = []
        weight = []

        if i > 0 and my_map[i-1][j].isFloor == True :  # Up
            neighbors.append(my_map[i-1][j])
            weight.append(0)
        
        if j > 0 and my_map[i][j-1].isFloor == True : # Left
            neighbors.append(my_map[i][j-1])
            weight.append(0)
        
        if (i < len(my_map)-1) and my_map[i+1][j].isFloor == True: # Down
            neighbors.append(my_map[i+1][j])
            weight.append(0)

        if (j < len(my_map[0])-1) and my_map[i][j+1].isFloor == True: # Right
            neighbors.append(my_map[i][j+1])
            weight.append(0)

        return neighbors, weight
