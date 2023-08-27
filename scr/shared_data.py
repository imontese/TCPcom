import threading
import random

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