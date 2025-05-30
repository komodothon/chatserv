"""/chat_stress_tester.py"""

import socket
import threading
import time
import random

HOST = "68.233.111.200"
PORT = 8000
NUM_CLIENTS = 700

clients = []

def client_thread(index):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        clients.append(s)
        if index % 100 == 0:
            print(f"[CONNECTED] Client {index}")

        while True:
            message = f"Hello from Client {index}"
            s.send(message.encode('utf-8'))
            time.sleep(random.uniform(1, 3))
    
    except Exception as e:
        if index % 100 == 0:
            print(f"[ERRO] Client {index}: {e}")

# start test

def main():
    for i in range(NUM_CLIENTS):
        threading.Thread(target=client_thread, args=(i,), daemon=True).start()
        
        # Stagger connections
        time.sleep(0.01)
    
    print(f"Started {NUM_CLIENTS} clients")
    input("Press ENTER to exit... ]n")


if __name__ == "__main__":
    main()
