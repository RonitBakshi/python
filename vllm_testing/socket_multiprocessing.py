import socketio
import asyncio
import socketio.client
import aiohttp


async def user_emulate(endpoint,user_number):
    connector = aiohttp.TCPConnector(ssl=False)

    async with aiohttp.ClientSession(connector=connector,headers={"token": "mytoken"}) as http_session:

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


        try:
            await sio.connect(endpoint)

            while True:
                await sio.emit("chat", {"kid": str(user_number), "action": "getQueueStatus"})
                await asyncio.sleep(20)
               
            #await sio.wait()

        except Exception as e:
            print(f"Failed to connect to the server: {e}")


async def main():
    total_users = 100
    socket_endpoint = "http://localhost:3001"

    tasks = []

    for user in range(total_users):
        task = asyncio.create_task(user_emulate(socket_endpoint,user))
        tasks.append(task)

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())