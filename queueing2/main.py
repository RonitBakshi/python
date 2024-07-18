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
    request_id: str = ""
    prompt: str
    response: str = ""


@app.post("/process")
async def process_request(request: RequestModel):

    request.request_id = str(uuid.uuid4())

    request_payload = {
        'request_id': request.request_id,
        'prompt': request.prompt
    }

    try:
        await redis_client.lpush('request_queue', json.dumps(request_payload))
        print(json.dumps(request_payload))
    except Exception as e:
        print(e)

    while await redis_client.hget("hash",request.request_id) == None:
        await asyncio.sleep(0.0001)

    request.response = str(await redis_client.hget("hash",request.request_id))
    await redis_client.hdel("hash",request.request_id)

    return request


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
