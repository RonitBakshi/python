import redis
import json
import asyncio
import aiohttp  # Use aiohttp for asynchronous HTTP requests

# Connect to Redis (replace with your actual connection details)
redis_url = 'rediss://default:AVNS_8yYBIS_I3QFT7P0uI6m@caching-120e037e-ronit-0e44.e.aivencloud.com:21605'
redis_client = redis.asyncio.from_url(redis_url, decode_responses=True)

# Global variable for batch ID
batch_id_lock = asyncio.Lock()
batch_id_counter = 1  # Initial batch ID

async def process_data(prompts, endpoint):
    responses = []
    # Simulate processing
    for prompt in prompts:
        responses.append(f"{prompt} : {endpoint}")
    await asyncio.sleep(6)
    return responses

async def batch_processing(endpoint):
    global batch_id_counter
    async with aiohttp.ClientSession() as session:  # Create a session for making HTTP requests
        while True:
            i = 0
            data = []

            while i < 6:
                message = await redis_client.rpop('request_queue')
                if message is None:
                    break
                request = json.loads(message)
                data.append(request)
                i += 1

            if len(data) > 0:
                async with batch_id_lock:
                    batch_id = batch_id_counter
                    batch_id_counter += 1

                request_payload = {
                    "batch_id": batch_id,
                    "data": data
                }

                headers = {
                    "Content-Type": "application/json"
                }

                async with session.post(endpoint, headers=headers, json=request_payload) as response:
                    response_data = await response.json()

                for item in response_data["data"]:
                    request_id = item["request_id"]
                    response_value = item["response"]
                    await redis_client.hset("hash", request_id, response_value)
            else:
                await asyncio.sleep(0.0001)

async def main():
    model_endpoints = [
        "http://192.168.1.34:7001/model"
        #"http://localhost:7000/model1",
        #"http://localhost:7000/model2",
        #"http://localhost:7000/model3",
        #"http://localhost:7000/model4"
    ]

    tasks = []
    for endpoint in model_endpoints:
        task = asyncio.create_task(batch_processing(endpoint))
        tasks.append(task)

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
