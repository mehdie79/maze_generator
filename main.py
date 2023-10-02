
import time
import MazeGenerator
import Network
import PathFinder

network = Network.UDPServer("127.0.0.1", 12345)

path_finder = PathFinder.PathFinder(network)
    
    
algorithm_choices = {'depth-first-search': path_finder.find_path_depth_first_search, 'breath-first-search': path_finder.find_path_breadth_first_search , 
                     'dijkstra-algorithm': path_finder.find_dijkstra_search, 'a-star-algorithm': path_finder.a_star_search_algorithm}    


network.receive_data()
WIDTH, HEIGHT, ALGORITHM = network.get_info_client()

maze_generator = MazeGenerator.MazeGenerator(WIDTH, HEIGHT)

maze = maze_generator.generate_maze()
network.send_message("maze_message")
network.send_maze_map(maze)

time.sleep(1)

algorithm_choices[ALGORITHM](maze)

network.close_socket()


