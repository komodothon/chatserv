"""/chat_server_ws.py"""

import asyncio
import websockets

connected_clients = set()

HOST = "0.0.0.0"
PORT = 8000

async def handler(websocket):
    # Extract remote client info
    peername = websocket.remote_address  # Tuple (IP, port)
    client_ip = peername[0]
    client_port = peername[1]

    print(f"New client connected: {client_ip}:{client_port}")

    connected_clients.add(websocket)

    try:
        async for message in websocket:
            print(f"Message from {client_ip}:{client_port} -> {message}")
            for client in connected_clients:
                if client != websocket:
                    await client.send(f"{client_ip}:{client_port} says: {message}")
    except websockets.exceptions.ConnectionClosed as e:
        print(f"Connection closed for {client_ip}:{client_port}: {e}")
    finally:
        connected_clients.remove(websocket)


async def main():
    async with websockets.serve(
        handler,
        HOST,
        PORT,
        ping_interval=600,
        ping_timeout=100
    ):
        print(f"WebSocket server started on ws://{HOST}:{PORT}")
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
