"""/chat_server_ws.py"""

import asyncio
import json
import jwt
import os
import websockets
import requests

from datetime import datetime, timezone

from dotenv import load_dotenv

load_dotenv()


from urllib.parse import urlparse, parse_qs
from pprint import pprint

from clientsession import ClientSession


# {websocket: user_values}
connected_clients = {}

HOST = "0.0.0.0"
PORT = 8000

# for development
CHATFRONT_API_URL = "http://localhost:5000/api/messages/save_message"

# for production
# CHATFRONT_API_URL = "https://oceanotech.in/api/messages/save_message"


jwt_secret_key = os.getenv("JWT_SECRET_KEY")
jwt_algorithm = os.getenv("JWT_ALGORITHM")

def post_message_to_chatfront(payload):
    try:
        res = requests.post(CHATFRONT_API_URL, json=payload, timeout=3)
        print(f"✅ Message saved: {res.status_code}")
    except Exception as e:
        print(f"❌ Failed to save message to chatfront API: {e}")


async def on_connect(websocket):
    path = websocket.request.path
    query_dict = parse_qs(urlparse(path).query)
    token = query_dict.get("token", [None])[0]
    # print(f"[chat_server_ws.py] token: {token}")


    if not token:
        await websocket.close(code=4401, reason="Missing token")
        return

    try:
        payload = jwt.decode(token, jwt_secret_key, [jwt_algorithm]) 

        user_id = payload.get("sub", None) or payload.get("identity", None) or payload.get("user_id", None)

        if not user_id:
            raise jwt.InvalidTokenError("Missing user ID in token")
        
        # print(f"✅ Authenticated user ID: {user_id}")
    except jwt.ExpiredSignatureError:
        await websocket.close(code=4401, reason="Token expired")
        return
    except jwt.InvalidTokenError as e:
        await websocket.close(code=4401, reason=f"Invalid token: {e}")
        return
    

    print(f"✅ Client connected: user_id: {user_id}")

    session = ClientSession(websocket, user_id)
    connected_clients[websocket] = session
    return session


async def on_message(websocket, message, session):
    print(f"📨 Message from user_id {session.user_id} -> {message}")

    try:
        data = json.loads(message)
    except json.JSONDecodeError:
        await websocket.send(json.dumps({
            "type": "error",
            "content": "Invalid message format. Expecting JSON"
        }))
        return 
    
    timestamp = datetime.now(timezone.utc).isoformat()
    # print(f"[chat_server_ws.py] timestamp: {timestamp}")

    payload = {
        "type": data.get("type", "chat"),
        "sender": data.get("sender", "unknown"),
        "room": data.get("room", "general"),
        "content": data.get("content", ""),
        "timestamp": timestamp,
    }

    # broadcast
    for client in connected_clients:
        try:
            await client.send(json.dumps(payload))
        except Exception as e:
            print(f"⚠️ Error sending to a client: {e}")

    if payload["type"] == "chat":
        # send to chatfront api for saving in db
        loop = asyncio.get_event_loop()
        loop.run_in_executor(None, post_message_to_chatfront, payload)    


async def on_disconnect(websocket, session):
    session.left_at = datetime.now(timezone.utc)
    connected_clients.pop(websocket, None)
    print(f"❌ Client disconnected: user_id: {session.user_id}")

async def on_error(websocket, error):
    print(f"🔥 WebSocket error: {error}")
    try:
        await websocket.send(json.dumps({
            "type": "error",
            "content": str(error)
        }))
    except:
        pass  # Socket may already be closed


async def handler(websocket):

    session = await on_connect(websocket)

    # Handle early disconnect (e.g., invalid token)
    if session is None:
        return


    try:
        async for message in websocket:
            await on_message(websocket, message, session)
    except websockets.exceptions.ConnectionClosed as e:
        print(f"🔌 Connection closed for user_id {session.user_id}: {e}")
    except Exception as e:
        await on_error(websocket, e)
    finally:
        await on_disconnect(websocket, session)


async def main():
    async with websockets.serve(handler, HOST, PORT):
        print(f"🚀 WebSocket server started at ws://{HOST}:{PORT}")
        await asyncio.Future()  # Run forever
            

if __name__ == "__main__":
    asyncio.run(main())


