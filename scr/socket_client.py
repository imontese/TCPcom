from config  import *

import socket

class SocketClient:
    def __init__(self, addr):
        self.addr = (addr)

    def __enter__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.addr)
        return self.client

    def __exit__(self, exc_type, exc_value, traceback):
        self.client.close()