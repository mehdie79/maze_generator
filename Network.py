import socket
import threading
import json

class UDPServer:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.data = None
        self.width = None
        self.height = None
        self.algorithm = None
        self.client_address = None
        self.udp_socket = None
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.udp_socket.bind((self.ip, self.port))  
        self.row = []
        self.column = []
        self.addPunishment = []
        self.mutex = threading.Lock()

        self.restart_maze = False
        self.generate_path = False

        self.running = True      

    def receive_data(self):

        data, client_address = self.udp_socket.recvfrom(1024)
        received_data = data.decode()
        self.client_address = client_address

        # Parse the received JSON data
        parsed_data = json.loads(received_data)

        # Extract the values from the parsed data
        self.width = int(parsed_data.get('width'))
        self.height = int(parsed_data.get('height'))
        self.algorithm = parsed_data.get('algorithm')
        self.checked_box = parsed_data.get('box_checked')

    
    def receive_coordinates(self):

        while self.running:
            data, client_address = self.udp_socket.recvfrom(1024)

            received_data = data.decode('utf-8')
            print(received_data)

            if received_data == "close":
                self.running = False
                break
            elif received_data == "generate_path":
                self.generate_path= True
                continue
            elif received_data == "reset_maze":
                self.restart_maze = True
                continue
            self.client_address = client_address

            # Parse the received JSON data
            parsed_data = json.loads(received_data)

            

            
            self.mutex.acquire()
            # Extract the values from the parsed data
            self.row.append(int(parsed_data.get('row')))
            self.column.append( int(parsed_data.get('column')))
            self.addPunishment.append(parsed_data.get('addPunishment'))
            self.mutex.release()
        
    def get_and_remove_first_coordinate(self):
        # Acquire the mutex to ensure exclusive access
        self.mutex.acquire()
        try:
            if self.row and self.column:
                first_row = self.row.pop(0)
                first_column = self.column.pop(0)
                addPunishment = self.addPunishment.pop(0)
                return first_row, first_column, addPunishment
            else:
                return None, None, None
        finally:
            # Always release the mutex, even if an exception occurs
            self.mutex.release()

    def client_send_generate_path(self):
        return self.generate_path
     
    def client_send_restart_maze(self):
        return self.restart_maze
    
    def client_set_generate_path_initial_state(self):
        self.generate_path = False
     
    def client_set_restart_maze_initial_state(self):
        self.restart_maze = False
     
    def start_recieve_coordiante(self):
        udp_thread = threading.Thread(target=self.receive_coordinates)
        udp_thread.start()
    
    def start(self):
        udp_thread = threading.Thread(target=self.receive_data)
        udp_thread.start()
    
    def get_info_client(self):
        return self.width, self.height, self.algorithm, self.checked_box
    
    def send_maze_map(self, data):
        array_json = json.dumps(data)
        self.udp_socket.sendto(array_json.encode(), self.client_address)

        
    def send_message(self, message):
        self.udp_socket.sendto(message.encode(), self.client_address)
    
    def close_socket(self):
        self.udp_socket.close()

                



        

        

        
    