from config  import *
from custom_task_thread import CustomTaskThread
from shared_data import SharedData
from socket_client import SocketClient
from tasks import *

import threading
import random


class Main:
    def __init__(self, server, port):
        self.value_to_send = SharedData(random.randint(0, 2**32 - 1))   # Initial 32-bit binary data  
        self.stop_event = threading.Event()                             # Global flag to control the execution of tasks
        self.socket_client = SocketClient(server, port)

    def start(self):
        with self.socket_client as client:

            task_args = (self.value_to_send, self.stop_event, client)

            # Create and start the threads  
            toggle_bit_thread = CustomTaskThread(task_args, toggle_bit_task)
            task_100ms_thread = CustomTaskThread(task_args, task_100ms)

            toggle_bit_thread.start()  
            task_100ms_thread.start()  

            try:  
                while True:  
                    # Main thread will sleep and wait for KeyboardInterrupt
                    time.sleep(1)  
                    
            except KeyboardInterrupt:  
                print("\nStopping threads...")  
                self.stop_event.set() 
                toggle_bit_thread.join()  
                task_100ms_thread.join() 
                client.close() 
                print("Threads stopped.") 


if __name__ == "__main__":
    main = Main(SERVER, PORT)
    main.start()