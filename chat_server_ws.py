"""/chat_server_ws.py"""

import asyncio
import json
import jwt
import os
import websockets

from websockets.asyncio.server import serve

from dotenv import load_dotenv

load_dotenv()


from urllib.parse import urlparse, parse_qs
from pprint import pprint

connected_clients = set()

HOST = "0.0.0.0"
PORT = 8000

jwt_secret_key = os.getenv("JWT_SECRET_KEY")
jwt_algorithm = os.getenv("JWT_ALGORITHM")

async def on_connect(websocket):
    peername = websocket.remote_address
    client_ip, client_port = peername
    print(f"[chat_server_ws.py] client_ip: {client_ip}, client_port: {client_port}")

    path = websocket.request.path
    print(f"[chat_server_ws.py] Got path: {path}")
    query_dict = parse_qs(urlparse(path).query)
    print(f"[chat_server_ws.py] query_dict: {query_dict}")
    token = query_dict.get("token", [None])[0]
    print(f"[chat_server_ws.py] token: {token}")


    if not token:
        print(f"[chat_server_ws.py] under 'if not token'")
        await websocket.close(code=4401, reason="Missing token")
        return

    try:
        print(f"[chat_server_ws.py] under 'try:'")

        payload = jwt.decode(token, jwt_secret_key, [jwt_algorithm]) 
        print(f"[chat_server_ws.py] after 'payload'")

        user_id = payload.get("sub", None) or payload.get("identity", None) or payload.get("user_id", None)
        print(f"[chat_server_ws.py] user_id: {user_id}")

        if not user_id:
            raise jwt.InvalidTokenError("Missing user ID in token")
        
        print(f"✅ Authenticated user ID: {user_id}")
    except jwt.ExpiredSignatureError:
        await websocket.close(code=4401, reason="Token expired")
        return
    except jwt.InvalidTokenError as e:
        await websocket.close(code=4401, reason=f"Invalid token: {e}")
        return
    

    print(f"✅ Client connected: {client_ip}:{client_port}")

    connected_clients.add(websocket)
    return (client_ip, client_port)


async def on_message(websocket, message, client_ip, client_port):
    print(f"📨 Message from {client_ip}:{client_port} -> {message}")

    try:
        data = json.loads(message)
    except json.JSONDecodeError:
        await websocket.send(json.dumps({
            "type": "error",
            "message": "Invalid message format. Expecting JSON"
        }))
        return 
    
    for client in connected_clients:
        if client != websocket:
            try:
                await client.send(json.dumps({
                    "type": data.get("type", "chat"),
                    "sender": data.get("sender", f"{client_ip}:{client_port}"),
                    "room": data.get("room", "general"),
                    "message": data.get("message", "")
                }))
            except Exception as e:
                print(f"⚠️ Error sending to a client: {e}")


async def on_disconnect(websocket, client_ip, client_port):
    connected_clients.remove(websocket)
    print(f"❌ Client disconnected: {client_ip}:{client_port}")

async def on_error(websocket, error):
    print(f"🔥 WebSocket error: {error}")
    try:
        await websocket.send(json.dumps({
            "type": "error",
            "message": str(error)
        }))
    except:
        pass  # Socket may already be closed


async def handler(websocket):

    connection_info = await on_connect(websocket)

    # Handle early disconnect (e.g., invalid token)
    if connection_info is None:
        return

    client_ip, client_port = connection_info

    try:
        async for message in websocket:
            await on_message(websocket, message, client_ip, client_port)
    except websockets.exceptions.ConnectionClosed as e:
        print(f"🔌 Connection closed for {client_ip}:{client_port}: {e}")
    except Exception as e:
        await on_error(websocket, e)
    finally:
        await on_disconnect(websocket, client_ip, client_port)


async def main():
    async with websockets.serve(handler, HOST, PORT):
        print(f"🚀 WebSocket server started at ws://{HOST}:{PORT}")
        await asyncio.Future()  # Run forever


if __name__ == "__main__":
    asyncio.run(main())


