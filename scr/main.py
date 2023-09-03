from config  import *
from custom_task_thread import CustomTaskThread
from shared_data import SharedData
from socket_client import SocketClient
from tasks import *

import threading
import random


class Main:
    def __init__(self, addr, operation_mode, send_cycle, toggle_cycle):
        self.value_to_send = SharedData(random.randint(0, 2**32 - 1))   # Initial 32-bit binary data  
        self.stop_event = threading.Event()                             # Global flag to control the execution of tasks
        self.socket_client = SocketClient(addr)
        self.op = operation_mode
        self.send_cycle = send_cycle
        self.toggle_cycle = toggle_cycle

    # Operation Mode selection, OP == 1 toggle_bit_thread does not run 
    def start_thread(self, client, operation_mode):
        task_args = (self.value_to_send, self.stop_event, client)

        if self.op == 0:
            # Create and start the threads  
            toggle_bit_thread = CustomTaskThread(task_args, toggle_bit_task, self.toggle_cycle)
            send_thread = CustomTaskThread(task_args, send_task, self.send_cycle)
            toggle_bit_thread.start()  
            send_thread.start()
            return [toggle_bit_thread, send_thread]
        elif self.op == 1:
            send_thread = CustomTaskThread(task_args, send_task, self.send_cycle)
            send_thread.start()
            return send_thread
        


    def start(self):
        with self.socket_client as client:

            threads = self.start_thread(client, self.op)
           
            try:  
                while True:  
                    # Main thread will sleep and wait for KeyboardInterrupt
                    time.sleep(1)  
                    
            except KeyboardInterrupt:  
                print("\nStopping threads...")  
                self.stop_event.set() 
                if isinstance(threads, list):
                    for thread in threads:
                        thread.join()
                else:
                    threads.join()
                client.close() 
                print("Threads stopped.") 


if __name__ == "__main__":
    main = Main(ADDR, 0, 0.1, 0.5)
    main.start()