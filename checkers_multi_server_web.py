import asyncio
import websockets
import os
import sys

clients = []
ADMIN_PASS = "supersecret99"

async def handler(websocket):
    global clients
    clients.append(websocket)
    player_id = len(clients) - 1 
    print(f"Connection {player_id} established.")
    
    try:
        await websocket.send(str(player_id))
        async for message in websocket:
            if message.startswith("ADMIN:"):
                parts = message.split(":")
                if len(parts) >= 3 and parts[1] == ADMIN_PASS:
                    cmd = parts[2]
                    if cmd == "QUIT":
                        print("Admin initiated shutdown.")
                        sys.exit(0) 
                    elif cmd == "RESET":
                        print("Admin reset the lobby.")
                        clients.clear() 
                    continue 

            for client in clients:
                if client != websocket:
                    await client.send(message)
                    
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        if websocket in clients:
            clients.remove(websocket)

async def main():
    # DigitalOcean assigns a port dynamically, we MUST catch it here:
    port = int(os.environ.get("PORT", 8080))
    print(f"Starting WebSocket server on port {port}...")
    async with websockets.serve(handler, "0.0.0.0", port):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())