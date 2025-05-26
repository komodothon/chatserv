"""/test2.py"""

import threading
import time
import random

def handle_client(client_id):
    for i in range(3):
        print(f"[Client {client_id}] Message {i}")
        time.sleep(random.uniform(0.5, 1.5))

def simulate_chat_server():
    threads = []

    print("[Server] Chat server started. Accepting clients ...\n")

    for client_id in range(1,6):
        t = threading.Thread(target=handle_client, args=(client_id,))
        t.start()
        threads.append(t)
        time.sleep(0.3)

    print("\n[Server] All clients connectd. Waiting for messages... \n")

    for t in threads:
        t.join()
    
    print("\n[Server] All clients disconnected. Server shutting down")

if __name__ == "__main__":
    simulate_chat_server()