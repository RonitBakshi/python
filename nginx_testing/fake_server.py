from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from multiprocessing import Process
import time
import asyncio

app1 = FastAPI()
app2 = FastAPI()
app3 = FastAPI()
app4 = FastAPI()
app6 = FastAPI()

class RequestPayload(BaseModel):
    text: str

@app1.post('/v1/chat/completions')
async def check_first_server(payload: RequestPayload):
    await asyncio.sleep(2)
    result = 'Server 1 up'
    print(result)
    return result

@app2.post('/v1/chat/completions')
async def check_first_server(payload: RequestPayload):
    await asyncio.sleep(2)
    result = 'Server 2 up'
    print(result)
    return result

@app3.post('/v1/chat/completions')
async def check_first_server(payload: RequestPayload):
    await asyncio.sleep(2)
    result = 'Server 3 up'
    print(result)
    return result

@app4.post('/v1/chat/completions')
async def check_first_server(payload: RequestPayload):
    await asyncio.sleep(2)
    result = 'Server 4 up'
    print(result)
    return result

@app6.post('/v1/chat/completions')
async def check_first_server(payload: RequestPayload):
    await asyncio.sleep(2)
    result = 'Server 6 up'
    print(result)
    return result


def run_server(app, port):
    uvicorn.run(app, port=port, host="0.0.0.0", log_level="info")

if __name__ == "__main__":
    # Create and start processes for each server
    p1 = Process(target=run_server, args=(app1, 8001))
    p2 = Process(target=run_server, args=(app2, 8002))
    p3 = Process(target=run_server, args=(app3, 8003))
    p4 = Process(target=run_server, args=(app4, 8004))
    p6 = Process(target=run_server, args=(app6, 8006))

    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p6.start()

    # Optionally, wait for all processes to finish
    p1.join()
    p2.join()
    p3.join()
    p4.join()
    p6.join()
