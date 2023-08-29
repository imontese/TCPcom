import time
import random
from threading import Event, Thread

class ValueGenerator:
    def __init__(self, min_time, max_time):
        self.min_time = min_time
        self.max_time = max_time
        self.stop_event = Event()
        self.start_flag = False
        self.thread = Thread(target=self.generate_value)
        self.thread.start()

    def generate_value(self):
        while not self.stop_event.is_set():
            if self.start_flag:
                # Generate a random value
                new_value = random.randint(0, 2**32 -1)

                # Print the generated value
                print(f'Generated Value {new_value}')

                # Sleep for random amount of time between min_time and max_time
                sleep_time = random.uniform(self.min_time, self.max_time)
                time.sleep(sleep_time)
            else:
                time.sleep(0.1)

            
    def start(self):
        self.start_flag = True

    def stop(self):
        self.start_flag = False

    def terminate(self):
        self.stop_event.set()
        self.thread.join()

if __name__ == "__main__" :
    value_generator =ValueGenerator(0.1, 0.1)   # Generates values with variable cycle times

    try:  
        while True:  
            # Main thread will sleep and wait for KeyboardInterrupt
            time.sleep(1) 
