"""/test1.py"""

import threading

def print_numbers():
    for i in range(5):
        print(i)

# Create a thread
t = threading.Thread(target=print_numbers)

# Start the thread
t.start()

# Continue main thread
print("Main thread running.")
