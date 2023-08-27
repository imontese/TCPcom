import threading

# CustomTaskThread class is a subclass of the threading.Thread class  
# It accepts a shared_data object, a stop_event, a task_function, a tuple of task_args, and an optional extra_arg  
# This class allows you to run the specified task_function in a separate thread with the given arguments    
class CustomTaskThread(threading.Thread):
    def __init__(self, task_args, task_function):
        super().__init__()
        # self.shared_data = shared_data
        # self.stop_event = stop_event
        self.task_args = task_args
        self.task_function = task_function

    def run(self):
        self.task_function(*self.task_args)