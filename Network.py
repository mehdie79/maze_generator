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

    

    def start(self):
        udp_thread = threading.Thread(target=self.receive_data)
        udp_thread.start()
    
    def get_info_client(self):
        return self.width, self.height, self.algorithm
    
    def send_maze_map(self, data):
        array_json = json.dumps(data)
        self.udp_socket.sendto(array_json.encode(), self.client_address)

        
    def send_message(self, message):
        self.udp_socket.sendto(message.encode(), self.client_address)
    
    def close_socket(self):
        self.udp_socket.close()

                



        

        

        
    