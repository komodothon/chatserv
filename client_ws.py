"""/client_ws.py"""

import asyncio
import websockets
import ssl

async def chat():
    uri = "wss://oceanotech.in/chat"
    # uri = "ws://localhost:8000"

    # Set up SSL context to verify certificate
    ssl_context = ssl.create_default_context()

    try:
        async with websockets.connect(uri, ssl=ssl_context) as websocket:
        # async with websockets.connect(uri) as websocket:
            print(f"Connected to {uri}")

            async def send_messages():
                while True:
                    
                    msg = await asyncio.to_thread(input)

                    await websocket.send(msg)

            async def receive_messages():
                while True:
                    msg = await websocket.recv()
                    print(f"\nReceived: {msg}")

            await asyncio.gather(send_messages(), receive_messages())

    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(chat())
