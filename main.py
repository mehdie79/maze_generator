
import time
import MazeGenerator
import Network
import PathFinder





network = Network.UDPServer("127.0.0.1", 12345)

path_finder = PathFinder.PathFinder(network)

   
    
algorithm_choices = {'depth-first-search': path_finder.find_path_depth_first_search, 'breath-first-search': path_finder.find_path_breadth_first_search , 
                     'dijkstra-algorithm': path_finder.find_dijkstra_search, 'a-star-algorithm': path_finder.a_star_search_algorithm}    

def customize_mode(ALGORITHM, maze, maze_generator):
    while network.running:
        if network.client_send_generate_path():
            algorithm_choices[ALGORITHM](maze)
            network.client_set_generate_path_initial_state()
            network.send_message("generate_path_complete")
        elif network.client_send_restart_maze():
            maze = maze_generator.restart_maze()
            network.send_message("maze_message")
            network.send_maze_map(maze)
            network.send_message("restart_maze_complete")
            network.client_set_restart_maze_initial_state()
        else:
            row, column, addPunishment = network.get_and_remove_first_coordinate()
            if row != None and column != None:
                maze = maze_generator.set_wall_punishment(row, column, addPunishment) 
                

network.receive_data()
WIDTH, HEIGHT, ALGORITHM, checked_box = network.get_info_client()


maze_generator = MazeGenerator.MazeGenerator(WIDTH, HEIGHT)

maze = None
if checked_box == False:
    maze = maze_generator.generate_maze()
else:
    maze = maze_generator.generate_customize_maze()

network.send_message("maze_message")
network.send_maze_map(maze)

if checked_box:
    network.start_recieve_coordiante()
    customize_mode(ALGORITHM, maze, maze_generator)
else:
    time.sleep(1)
    algorithm_choices[ALGORITHM](maze)

network.close_socket()


