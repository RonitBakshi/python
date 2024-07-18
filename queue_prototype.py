from fastapi import FastAPI, BackgroundTasks, HTTPException
from typing import List
from pydantic import BaseModel
import queue

app = FastAPI()

# Define a queue to hold the requests
request_queue = queue.Queue()

# specify vllm model requests
model_endpoints = [
    "fake-endpoint-1",
    "fake-endpoint-2",
    "fake-endpoint-3",
    "fake-endpoint-4"
]

# is model empty or not
model_is_empty = [
    True,
    True,
    True,
    True,
]

# Define a model for the incoming request data
class RequestData(BaseModel):
    data: str

# Endpoint to add a request to the queue
@app.post("/enqueue")
async def enqueue_request(request_data: RequestData, background_tasks: BackgroundTasks):
    
    if request_queue.empty():
        for i in range(len(model_endpoints)):
            if model_is_empty[i] = true:

    else:
        request_queue.put(request_queue.data)

    try:
        # Add the request to the queue
        request_queue.put(request_data.data)
        # Add a background task to process the queue
        background_tasks.add_task(process_queue)
        return {"message": "Request enqueued successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Background task to process the queue
def process_queue():
    while not request_queue.empty():
        request_data = request_queue.get()
        # Simulate processing the request
        process_request(request_data)

# Simulate processing the request
def process_request(request_data: str):
    print(f"Processing request: {request_data}")
    # Here you can add your request processing logic
