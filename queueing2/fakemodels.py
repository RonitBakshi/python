from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import asyncio

app = FastAPI()

class DataList(BaseModel):
    request_id: str
    prompt: str
    response: str = ""

class ModelRequest(BaseModel):
    batch_id: int
    data: List[DataList]

@app.post("/model1")
async def model1(request: ModelRequest):

    for item in request.data:
        item.response = f"Batch number: {request.batch_id} | Model no. 1 | Prompt: {item.prompt} | Request Id: {item.request_id}"

    await asyncio.sleep(6)

    print(request.batch_id)
    return request

@app.post("/model2")
async def model1(request: ModelRequest):

    for item in request.data:
        item.response = f"Batch number: {request.batch_id} | Model no. 2 | Prompt: {item.prompt} | Request Id: {item.request_id}"

    await asyncio.sleep(6)

    print(request.batch_id)
    return request

@app.post("/model3")
async def model1(request: ModelRequest):

    for item in request.data:
        item.response = f"Batch number: {request.batch_id} | Model no. 3 | Prompt: {item.prompt} | Request Id: {item.request_id}"

    await asyncio.sleep(6)

    print(request.batch_id)
    return request

@app.post("/model4")
async def model1(request: ModelRequest):

    for item in request.data:
        item.response = f"Batch number: {request.batch_id} | Model no. 4 | Prompt: {item.prompt} | Request Id: {item.request_id}"

    await asyncio.sleep(6)

    print(request.batch_id)
    return request

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7000)
