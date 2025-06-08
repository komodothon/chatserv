"""/client_ws.py"""

import asyncio
import websockets
import ssl
import json

# You can hardcode or prompt for these:
USERNAME = "Python terminal client"
ROOM = "general"


async def chat():
    uri = "wss://oceanotech.in/chat"
    
    # uri = "ws://localhost:8000"
    # uri = "ws://192.168.1.6:8000"

    # Set up SSL context to verify certificate
    ssl_context = ssl.create_default_context()

    try:
        async with websockets.connect(uri, ssl=ssl_context) as websocket:
        # async with websockets.connect(uri) as websocket:
            print(f"Connected to {uri} as {USERNAME} in room '{ROOM}'")

            async def send_messages():
                while True:
                    
                    text = await asyncio.to_thread(input)

                    msg = {
                        "type": "chat",
                        "sender": USERNAME,
                        "room": ROOM,
                        "message": text
                    }

                    await websocket.send(json.dumps(msg))

            async def receive_messages():
                while True:
                    try:
                        raw = await websocket.recv()
                        msg = json.loads(raw)

                        # Nicely print received message
                        sender = msg.get("sender", "Unknown")
                        message = msg.get("message", "")
                        print(f"\n[{sender}] {message}")
                    except json.JSONDecodeError:
                        print("\n[!] Received invalid JSON")

            await asyncio.gather(send_messages(), receive_messages())

    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(chat())
