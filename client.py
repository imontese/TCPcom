import socket
import threading
import struct
import time  
import random 


LENGTH = 32
PORT = 5050
FORMAT = 'utf-8'
SERVER = "192.168.17.100"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


class SharedData:
    def __init__(self, initial_value):
        self.value_to_send = initial_value
        self.lock = threading.Lock()

    # Toggle Bit-0
    def toggle_bit_0(self):
        with self.lock:
            self.value_to_send ^= 0x1

    def get_value_to_send(self):
        with self.lock:
            return self.value_to_send

    # Update the value keeping the bit-0
    def update_value_to_send(self):
        new_value = random.randint(0, 2**32 - 1)
        with self.lock:
            bit_0 = self.value_to_send & 0x1
            self.value_to_send = (new_value & ~0x1) | bit_0 


# The measure_time calculates the time taken to execute a task  
def measure_time(task, *args, **kwargs):  
    start_time = time.perf_counter()  
    task(*args, **kwargs)  
    end_time = time.perf_counter()  
      
    time_taken = end_time - start_time  
    return time_taken 


def toggle_bit_task(share_data, stop_event):   
    while not stop_event.is_set():  
        share_data.toggle_bit_0()   
        #print(value_to_send)  
        time.sleep(0.5) 

# Send and receive the data packets
def send(share_data):
    value_to_send = share_data.get_value_to_send()
    msg_length = value_to_send.bit_length()
    if msg_length > 32:
        print("Exceed 32 bits")
        return
    else:
        try:
            #Send data to the server
            packed_data = struct.pack('>I', value_to_send)
            client.sendall(packed_data)
            received_data = client.recv(2048)
            received_value = struct.unpack('>I', received_data)[0]
            binary_representation = format(received_value, 'b')  
            print(binary_representation)
            #print(received_value)

            # Compare the sent and received data  
            if packed_data != received_data:  
                print("Sent and received data do not match!") 

        except socket.error as e:  
            print(f"Socket error occurred: {e}")  
            print("Attempting to reconnect...")  
  
            # Attempt to reconnect to the server  
            try:  
                client.close()          
                client.connect(ADDR)  
            except socket.error as e:  
                print(f"Failed to reconnect: {e}")  


def task_100ms(share_data, stop_event):
    while not stop_event.is_set():  
        share_data.update_value_to_send()
        time_taken = measure_time(send, share_data)  
        #print(f"Time taken: {time_taken} seconds")   
            
        # Sleep for the remaining time to achieve a total of 100ms per cycle  
        sleep_time = max(0.1 - time_taken, 0)  
        time.sleep(sleep_time)
    

# Initial 32-bit binary data
value_to_send = SharedData(random.randint(0, 2**32 - 1))

# Global flag to control the execution of tasks  
stop_event = threading.Event() 


# Create and start the threads  
toggle_bit_thread = threading.Thread(target=toggle_bit_task, args=(value_to_send, stop_event,))  
task_100ms_thread = threading.Thread(target=task_100ms, args=(value_to_send, stop_event,))

toggle_bit_thread.start()  
task_100ms_thread.start()  

try:  
    while True:  
        # Main thread will sleep and wait for KeyboardInterrupt
        time.sleep(1)  
        
except KeyboardInterrupt:  
    print("\nStopping threads...")  
    stop_event.set() 
    toggle_bit_thread.join()  
    task_100ms_thread.join() 
    client.close() 
    print("Threads stopped.")  
