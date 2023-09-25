import random

class MazeGenerator():

    def __init__(self, width, height):
        self.width = width
        self.height = height
        # Init Maze
        self.maze = [["u" for _ in range(width)] for _ in range(height)]
        self.walls = []

    
    
    def surroundingCells(self, rand_wall):
        s_cells = 0
        if (self.maze[rand_wall[0]-1][rand_wall[1]] == " "):
            s_cells += 1
        if (self.maze[rand_wall[0]+1][rand_wall[1]] == " "):
            s_cells += 1
        if (self.maze[rand_wall[0]][rand_wall[1]-1] == " "):
            s_cells +=1
        if (self.maze[rand_wall[0]][rand_wall[1]+1] == " "):
            s_cells += 1
        return s_cells
    
    def delete_wall(self,rand_wall):
        for wall in self.walls:
            if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                self.walls.remove(wall) 

    def make_walls(self):
        for i in range(0, self.height):
            for j in range(0, self.width):
                if (self.maze[i][j] == 'u'):
                    self.maze[i][j] = "#"
        

    def create_entrance_exit(self):
        for i in range(0, self.width):
            if (self.maze[1][i] == " "):
                self.maze[0][i] = "O"
                break
        for i in range(self.width-1, 0, -1):
            if (self.maze[self.height-2][i] == " "):
                self.maze[self.height-1][i] = "X"
                break

    def generate_maze(self):

        
        
        starting_height = int(random.random()*self.height)
        starting_width = int(random.random()*self.width)

        if starting_height == 0:
            starting_height += 1
        if starting_height == self.height-1:
            starting_height -= 1
        if starting_width == 0:
            starting_width += 1
        if starting_width == self.width-1:
            starting_width -= 1
        
        self.maze[starting_height][starting_width] = " "
        
        self.walls.append([starting_height-1, starting_width])
        self.walls.append([starting_height, starting_width-1])
        self.walls.append([starting_height, starting_width+1])
        self.walls.append([starting_height+1, starting_width])

        self.maze[starting_height-1][starting_width] = "#"
        self.maze[starting_height][starting_width-1] = "#"
        self.maze[starting_height][starting_width+1] = "#"
        self.maze[starting_height+1][starting_width] = "#"
        while (self.walls):
            # Pick a random wall
            rand_wall = self.walls[int(random.random()*len(self.walls))-1]

            # Check if it is a left wall
            if (rand_wall[1] != 0):
                if (self.maze[rand_wall[0]][rand_wall[1]-1] == 'u' and self.maze[rand_wall[0]][rand_wall[1]+1] == " "):
                    # Find the number of surrounding cells
                    s_cells = self.surroundingCells(rand_wall)

                    if (s_cells < 2):
                        # Denote the new path
                        self.maze[rand_wall[0]][rand_wall[1]] = " "

                        # Mark the new walls
                        # Upper cell
                        if (rand_wall[0] != 0):
                            if (self.maze[rand_wall[0]-1][rand_wall[1]] != " "):
                                self.maze[rand_wall[0]-1][rand_wall[1]] = "#"
                            if ([rand_wall[0]-1, rand_wall[1]] not in self.walls):
                                self.walls.append([rand_wall[0]-1, rand_wall[1]])


                        # Bottom cell
                        if (rand_wall[0] != self.height-1):
                            if (self.maze[rand_wall[0]+1][rand_wall[1]] != " "):
                                self.maze[rand_wall[0]+1][rand_wall[1]] = "#"
                            if ([rand_wall[0]+1, rand_wall[1]] not in self.walls):
                                self.walls.append([rand_wall[0]+1, rand_wall[1]])

                        # Leftmost cell
                        if (rand_wall[1] != 0):	
                            if (self.maze[rand_wall[0]][rand_wall[1]-1] != " "):
                                self.maze[rand_wall[0]][rand_wall[1]-1] = "#"
                            if ([rand_wall[0], rand_wall[1]-1] not in self.walls):
                                self.walls.append([rand_wall[0], rand_wall[1]-1])
                    

                    
                    self.delete_wall(rand_wall)

                    continue

            # Check if it is an upper wall
            if (rand_wall[0] != 0):
                if (self.maze[rand_wall[0]-1][rand_wall[1]] == 'u' and self.maze[rand_wall[0]+1][rand_wall[1]] == " "):

                    s_cells = self.surroundingCells(rand_wall)
                    if (s_cells < 2):
                        # Denote the new path
                        self.maze[rand_wall[0]][rand_wall[1]] = " "

                        # Mark the new walls
                        # Upper cell
                        if (rand_wall[0] != 0):
                            if (self.maze[rand_wall[0]-1][rand_wall[1]] != " "):
                                self.maze[rand_wall[0]-1][rand_wall[1]] = "#"
                            if ([rand_wall[0]-1, rand_wall[1]] not in self.walls):
                                self.walls.append([rand_wall[0]-1, rand_wall[1]])

                        # Leftmost cell
                        if (rand_wall[1] != 0):
                            if (self.maze[rand_wall[0]][rand_wall[1]-1] != " "):
                                self.maze[rand_wall[0]][rand_wall[1]-1] = "#"
                            if ([rand_wall[0], rand_wall[1]-1] not in self.walls):
                                self.walls.append([rand_wall[0], rand_wall[1]-1])

                        # Rightmost cell
                        if (rand_wall[1] != self.width-1):
                            if (self.maze[rand_wall[0]][rand_wall[1]+1] != " "):
                                self.maze[rand_wall[0]][rand_wall[1]+1] = "#"
                            if ([rand_wall[0], rand_wall[1]+1] not in self.walls):
                                self.walls.append([rand_wall[0], rand_wall[1]+1])

                    self.delete_wall(rand_wall)

                    continue

            # Check the bottom wall
            if (rand_wall[0] != self.height-1):
                if (self.maze[rand_wall[0]+1][rand_wall[1]] == 'u' and self.maze[rand_wall[0]-1][rand_wall[1]] == " "):

                    s_cells = self.surroundingCells(rand_wall)
                    if (s_cells < 2):
                        # Denote the new path
                        self.maze[rand_wall[0]][rand_wall[1]] = " "

                        # Mark the new walls
                        if (rand_wall[0] != self.height-1):
                            if (self.maze[rand_wall[0]+1][rand_wall[1]] != " "):
                                self.maze[rand_wall[0]+1][rand_wall[1]] = "#"
                            if ([rand_wall[0]+1, rand_wall[1]] not in self.walls):
                                self.walls.append([rand_wall[0]+1, rand_wall[1]])
                        if (rand_wall[1] != 0):
                            if (self.maze[rand_wall[0]][rand_wall[1]-1] != " "):
                                self.maze[rand_wall[0]][rand_wall[1]-1] = "#"
                            if ([rand_wall[0], rand_wall[1]-1] not in self.walls):
                                self.walls.append([rand_wall[0], rand_wall[1]-1])
                        if (rand_wall[1] != self.width-1):
                            if (self.maze[rand_wall[0]][rand_wall[1]+1] != " "):
                                self.maze[rand_wall[0]][rand_wall[1]+1] = "#"
                            if ([rand_wall[0], rand_wall[1]+1] not in self.walls):
                                self.walls.append([rand_wall[0], rand_wall[1]+1])

                    self.delete_wall(rand_wall)


                    continue

            # Check the right wall
            if (rand_wall[1] != self.width-1):
                if (self.maze[rand_wall[0]][rand_wall[1]+1] == 'u' and self.maze[rand_wall[0]][rand_wall[1]-1] == " "):

                    s_cells = self.surroundingCells(rand_wall)
                    if (s_cells < 2):
                        # Denote the new path
                        self.maze[rand_wall[0]][rand_wall[1]] = " "

                        # Mark the new walls
                        if (rand_wall[1] != self.width-1):
                            if (self.maze[rand_wall[0]][rand_wall[1]+1] != " "):
                                self.maze[rand_wall[0]][rand_wall[1]+1] = "#"
                            if ([rand_wall[0], rand_wall[1]+1] not in self.walls):
                                self.walls.append([rand_wall[0], rand_wall[1]+1])
                        if (rand_wall[0] != self.height-1):
                            if (self.maze[rand_wall[0]+1][rand_wall[1]] != " "):
                                self.maze[rand_wall[0]+1][rand_wall[1]] = "#"
                            if ([rand_wall[0]+1, rand_wall[1]] not in self.walls):
                                self.walls.append([rand_wall[0]+1, rand_wall[1]])
                        if (rand_wall[0] != 0):	
                            if (self.maze[rand_wall[0]-1][rand_wall[1]] != " "):
                                self.maze[rand_wall[0]-1][rand_wall[1]] = "#"
                            if ([rand_wall[0]-1, rand_wall[1]] not in self.walls):
                                self.walls.append([rand_wall[0]-1, rand_wall[1]])

                    self.delete_wall(rand_wall)

                    continue

            self.delete_wall(rand_wall)
        


        self.make_walls()
        self.create_entrance_exit()

        return self.maze
        

    def print_maze_console(self):
        for row in self.maze:
            print(" ".join(row))