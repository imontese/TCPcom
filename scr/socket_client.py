from config  import *

import socket

class SocketClient:
    def __init__(self, server, port):
        self.addr = (server, port)

    def __enter__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(ADDR)
        return self.client

    def __exit__(self, exc_type, exc_value, traceback):
        self.client.close()