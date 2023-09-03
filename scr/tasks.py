from config  import *

import time
import struct
import socket

def toggle_bit_task(share_data, stop_event, client, task_cycle):   
    while not stop_event.is_set():  
        share_data.toggle_bit_0()   
        #print(value_to_send)  
        time.sleep(task_cycle) 

def send_task(share_data, stop_event, client, task_cycle):
    while not stop_event.is_set():  
        share_data.update_value_to_send()
        time_taken = measure_time(send, share_data, client)  
        #print(f"Time taken: {time_taken} seconds")   
            
        # Sleep for the remaining time to achieve the tas_cycle time  
        sleep_time = max(task_cycle - time_taken, 0)  
        time.sleep(sleep_time)

# The measure_time calculates the time taken to execute a task  
def measure_time(task, *args, **kwargs):  
    start_time = time.perf_counter()  
    task(*args, **kwargs)  
    end_time = time.perf_counter()  
      
    time_taken = end_time - start_time  
    return time_taken 

# Send and receive the data packets
def send(share_data, client):
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
            #print(f'Sent data ---- :{value_to_send}')      # print send data
            received_data = client.recv(2048)
            received_value = struct.unpack('>I', received_data)[0]
            binary_representation = format(received_value, 'b')  
            print(received_value)

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

    