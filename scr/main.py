from config  import *
from custom_task_thread import CustomTaskThread
from shared_data import SharedData
from socket_client import SocketClient
from tasks import *

import threading
import random


class Main:
    def __init__(self, server, port, send_cycle, toggle_cycle):
        self.value_to_send = SharedData(random.randint(0, 2**32 - 1))   # Initial 32-bit binary data  
        self.stop_event = threading.Event()                             # Global flag to control the execution of tasks
        self.socket_client = SocketClient(server, port)
        self.send_cycle = send_cycle
        self.toggle_cycle = toggle_cycle

    def start(self):
        with self.socket_client as client:

            task_args = (self.value_to_send, self.stop_event, client)

            # Create and start the threads  
            toggle_bit_thread = CustomTaskThread(task_args, toggle_bit_task, self.toggle_cycle)
            send_thread = CustomTaskThread(task_args, send_task, self.send_cycle)

            toggle_bit_thread.start()  
            send_thread.start()  

            try:  
                while True:  
                    # Main thread will sleep and wait for KeyboardInterrupt
                    time.sleep(1)  
                    
            except KeyboardInterrupt:  
                print("\nStopping threads...")  
                self.stop_event.set() 
                toggle_bit_thread.join()  
                send_thread.join() 
                client.close() 
                print("Threads stopped.") 


if __name__ == "__main__":
    main = Main(SERVER, PORT, 0.2, 1)
    main.start()