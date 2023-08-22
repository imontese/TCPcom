import socket
import threading
import struct
import time  
import random 


LENGTH = 32
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.17.110"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def toggle_bit_0(value_to_send):  
    return value_to_send ^ 0x1 

def toggle_bit_task(stop_event):  
    global value_to_send  
    while not stop_event.is_set():  
        value_to_send = toggle_bit_0(value_to_send)  
        binary_str = format(value_to_send, '032b')  
        #print(binary_str)  
        time.sleep(0.5) 

def send(stop_event):
    global value_to_send
    msg_length = value_to_send.bit_length()
    send_length = str(msg_length).encode(FORMAT)
    if msg_length > 32:
        print("Exceed 32 bits")
        return
    else:
        try:
            while not stop_event.is_set():
                #Send data to the server
                start_time = time.perf_counter() 
                packed_data = struct.pack('>I', value_to_send)
                client.sendall(packed_data)
                received_data = client.recv(2048)
                received_value = struct.unpack('>I', received_data)[0]
                print(received_value)

                # Compare the sent and received data  
                if packed_data != received_data:  
                    print("Sent and received data do not match!") 

                end_time = time.perf_counter()  
                time_difference = end_time - start_time  
                #print(f"Time difference (excluding sleep): {time_difference} seconds")

                # Sleep for the remaining time to achieve a total of 100ms per cycle  
                sleep_time = max(0.1 - time_difference, 0)  
                time.sleep(sleep_time)  
                
                end_time = time.perf_counter()
                time_difference = end_time - start_time 
                print(f"Time difference: {time_difference} seconds")

        finally:
            # Close the socket connection
            client.close()


# Initial 32-bit binary data
value_to_send = random.randint(0, 2**32 - 1)  

# Global flag to control the execution of tasks  
stop_event = threading.Event() 


# Create and start the threads  
toggle_bit_thread = threading.Thread(target=toggle_bit_task, args=(stop_event,))  
task_100ms_thread = threading.Thread(target=send, args=(stop_event,))

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
    print("Threads stopped.")  
