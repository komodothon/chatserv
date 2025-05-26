"""/client.py"""

import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                print("Connection closed by server.")
                break
            print(message)
        except:
            print("Error receiving message.")
            break

def client_program():
    host = 'localhost'  # Change to server's IP if connecting remotely
    port = 5555

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # Start thread to receive messages from server
    threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

    print("Connected to chat server. You can start sending messages.")
    while True:
        msg = input()
        if msg.lower() == 'exit':
            break
        client_socket.send(msg.encode('utf-8'))

    client_socket.close()

if __name__ == '__main__':
    client_program()
