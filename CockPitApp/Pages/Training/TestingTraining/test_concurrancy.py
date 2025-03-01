import threading
import csv
from queue import Queue

class A:
    def __init__(self, filename, queue, condition):
        self.filename = filename
        self.queue = queue
        self.condition = condition

    def write_data(self, data):
        with open(self.filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)
        print("A wrote:", data)
        with self.condition:
            self.queue.put(data)  # Add data to the queue for B to read
            self.condition.notify()  # Notify the waiting B thread

class B:
    def __init__(self, queue, condition):
        self.queue = queue
        self.condition = condition

    def read_data(self):
        with self.condition:
            while self.queue.empty():
                self.condition.wait()  # Wait for data in the queue
            data = self.queue.get()  # Get data from the queue
            fruit = data[0]  # Extract fruit from data
            price = float(data[1])  # Extract price from data
            last_row = [fruit, price]
            if last_row:
                print("B read most recent:", last_row)  # Print the most recent data read by B
            self.queue.task_done()  # Mark the task as done for the queue

class C:
    def __init__(self, filename):
        self.filename = filename
        self.queue = Queue()
        self.condition = threading.Condition()
        self.a = A(self.filename, self.queue, self.condition)
        self.b = B(self.queue, self.condition)

    def process_data(self, data):
        t1 = threading.Thread(target=self.a.write_data, args=(data,))
        t2 = threading.Thread(target=self.b.read_data)
        t1.start()
        t2.start()
        t1.join()
        t2.join()


import os 

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

data_path = os.path.join(parent_dir, 'Training', 'TestingTraining')

# Example usage
filename = os.path.join(data_path , "data.csv")

# Create an instance of class C
c = C(filename)

# Call process_data method of class C multiple times with different data

c.process_data(["Apple", 20.0])
c.process_data(["Orange", 40.0])
c.process_data(["Banana", 30.0])

for i in range(20):
    c.process_data([i, i])
