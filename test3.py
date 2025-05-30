"""/test3.py"""

# Asyncio example
import asyncio

async def task(name):
    print(f"{name} starting")
    await asyncio.sleep(2)
    print(f"{name} done")

async def main():
    await asyncio.gather(task("Task 3"), task("Task 4"))

asyncio.run(main())

# Threading eg.
import threading
import time

def task(name):
    print(f"{name} starting")
    time.sleep(2)
    print(f"{name} done")

thread1 = threading.Thread(target=task, args=("Thread 1",))
thread2 = threading.Thread(target=task, args=("Thread 2",))

thread1.start()
thread2.start()

thread1.join()
thread2.join()

