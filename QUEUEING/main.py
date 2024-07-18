from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import redis
import uuid
import json
import redis.asyncio
import asyncio


app = FastAPI()

# Connect to Redis
#redis_client = redis.Redis(host='rediss://default:AVNS_8yYBIS_I3QFT7P0uI6m@caching-120e037e-ronit-0e44.e.aivencloud.com:21605', port=21605, db=0)

redis_url = 'rediss://default:AVNS_8yYBIS_I3QFT7P0uI6m@caching-120e037e-ronit-0e44.e.aivencloud.com:21605'
redis_client = redis.asyncio.from_url(redis_url, decode_responses=True)

# Data model for the request
class RequestModel(BaseModel):
    data: str

# Function to handle incoming responses
"""
def handle_responses():
    while True:
        # Block until a response is available
        _, message = redis_client.brpop('response_queue')
        response = json.loads(message)
        request_id = response['request_id']
        redis_client.hset('responses', request_id, json.dumps(response['result']))

# Start the thread to listen for responses
threading.Thread(target=handle_responses, daemon=True).start()
"""

@app.post("/process")
async def process_request(request: RequestModel):

    request_id = str(uuid.uuid4())

    request_payload = {
        'request_id': request_id,
        'data': request.data
    }

    # Add the request to the 'request_queue'
    try:
        await redis_client.lpush('request_queue', json.dumps(request_payload))
        print(json.dumps(request_payload))
    except Exception as e:
        print("exception")

    while await redis_client.hget("hash",request_id) == None:
        await asyncio.sleep(0.5)

    response = await redis_client.hget("hash",request_id)
    await redis_client.hdel("hash",request_id)

    return response


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

    