import threading  
import time  
  
def toggle_bit_0(binary_data):  
    return binary_data ^ 0b00000000000000000000000000000001  
  
def toggle_bit_task(stop_event):  
    global binary_data  
    while not stop_event.is_set():  
        binary_data = toggle_bit_0(binary_data)  
        time.sleep(0.5)  
  
def task_every_100ms(stop_event):  
    global binary_data  
    while not stop_event.is_set():  
        least_significant_bit = binary_data & 1  # Get the value of Bit-0  
        print(f"Value of the toggle bit (Bit-0): {least_significant_bit}")  
        time.sleep(0.1)  
  
# Initial 32-bit binary data (all zeros)  
binary_data = 0b00000000000000000000000000000000  
  
# Event object to signal threads to stop  
stop_event = threading.Event()  
  
# Create and start the threads  
toggle_bit_thread = threading.Thread(target=toggle_bit_task, args=(stop_event,))  
task_100ms_thread = threading.Thread(target=task_every_100ms, args=(stop_event,))  
  
toggle_bit_thread.start()  
task_100ms_thread.start()  
  
try:  
    while True:  
        time.sleep(1)  # Main thread will sleep and wait for KeyboardInterrupt  
  
except KeyboardInterrupt:  
    print("\nStopping threads...")  
    stop_event.set()  
    toggle_bit_thread.join()  
    task_100ms_thread.join()  
    print("Threads stopped.")  
