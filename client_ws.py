"""/client_ws.py"""

import asyncio
import ssl
import json

import websockets
import jwt
import os

from datetime import datetime, timedelta, timezone
import time

from dotenv import load_dotenv
load_dotenv()


# You can hardcode or prompt for these:
USERNAME = "Python terminal client"
ROOM = "general"

def generate_token(user_id):
    now = datetime.now(timezone.utc)

    payload = {
        "user_id": str(user_id),
        "iat": now,
        "exp": now + timedelta(hours=1)
    }
    

    jwt_secret_key = os.getenv("JWT_SECRET_KEY", "super_secret_jwt_key")
    jwt_algorithm = os.getenv("JWT_ALGORITHM", "HS256")

    jwt_token = jwt.encode(payload, jwt_secret_key, jwt_algorithm)
    return jwt_token

async def chat():    
    user_id = 4
    # token = "abc123"
    token = ""

    jwt_token = generate_token(user_id)
    print(f"[client_ws.py] jwt_token: {jwt_token}")

    # uri = "wss://oceanotech.in/chat"
    
    uri = f"ws://localhost:8000/chat?token={jwt_token}"
    # uri = "ws://localhost:8000/?token=test123"
    # uri = "ws://192.168.1.6:8000"

    # Set up SSL context to verify certificate
    ssl_context = ssl.create_default_context()


    try:
        # async with websockets.connect(uri, ssl=ssl_context) as websocket:
        async with websockets.connect(uri) as websocket:
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


# Minimal test client


# async def go():
#     token = "abc123"
#     uri = f"ws://localhost:8000/test?token={token}"

#     async with websockets.connect(uri) as ws:
#         print(await ws.recv())

# asyncio.run(go())