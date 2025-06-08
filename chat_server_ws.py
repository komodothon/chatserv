"""/chat_server_ws.py"""

import asyncio
import websockets
import json

connected_clients = set()

HOST = "0.0.0.0"
PORT = 8000

async def on_connect(websocket):
    peername = websocket.remote_address
    client_ip, client_port = peername

    print(f"✅ Client connected: {client_ip}:{client_port}")

    connected_clients.add(websocket)
    return client_ip, client_port


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
    client_ip, client_port = await on_connect(websocket)

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
    async with websockets.serve(
        handler,
        HOST,
        PORT,
        ping_interval = 600,
        ping_timeout = 100,
    ):

        print(f"🚀 WebSocket server started at ws://{HOST}:{PORT}")
        await asyncio.Future()  # Run forever


if __name__ == "__main__":
    asyncio.run(main())
