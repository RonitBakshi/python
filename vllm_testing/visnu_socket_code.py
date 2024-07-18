import socketio
import threading
import time
import uuid
import requests
import asyncio
import socketio.client
import aiohttp
import json
import random

users = range(1, 100)

async def main():

    connector = aiohttp.TCPConnector(ssl=False)

    async with aiohttp.ClientSession(connector=connector,headers={
            "token": "mytoken"
        }) as http_session:

        sio = socketio.AsyncClient(http_session=http_session)

        @sio.event
        async def connect():
            print("Connected to server")

        @sio.event
        async def chat(data):
         if data["action"] == "getQueueStatus":
            print("Received data", data)
            parsed = data["data"]
            if(data["data"]["status"] == "access"):
                print("access",parsed["kid"])
            else:
                print("waiting",parsed["kid"],parsed["position"])


        async def updateActiveAt():
                # await asyncio.sleep(30)
                await sio.emit("chat", {"kid": "1", "action": "updateActiveAt"})
                await sio.emit("chat", {"kid": "8", "action": "updateActiveAt"})

                
        try:
            await sio.connect('http://localhost:3001')
            await sio.emit("chat", {"kid": "1", "action": "getQueueStatus"})
            await sio.emit("chat", {"kid": "8", "action": "getQueueStatus"})
            while True:
                randomStart = random.randint(1, 10)
                randomIds = range(randomStart, randomStart + 10)
                await asyncio.sleep(20)
                await updateActiveAt()
                for i in randomIds:
                    await sio.emit("chat", {"kid": str(i), "action": "getQueueStatus"})
                    await asyncio.sleep(0.0001)
            await sio.wait()

        except Exception as e:
            print(f"Failed to connect to the server: {e}")


if __name__ == "__main__":
    asyncio.run(main())