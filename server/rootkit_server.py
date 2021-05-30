import asyncio
import websockets
from datetime import datetime
import os

async def hello(websocket, path):
    name = await websocket.recv()
    print(path)
    print(f" {datetime.now()} {name}")
    f = open("data.txt", "a")
    f.write(f" {datetime.now()} {name} \n")
    f.close()

start_server = websockets.serve(hello, "0.0.0.0", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()