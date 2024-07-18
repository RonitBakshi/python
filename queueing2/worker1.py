import redis
import json
import asyncio
import requests

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
            print(len(data))
            async with batch_id_lock:
                batch_id = batch_id_counter
                batch_id_counter += 1

            request = {}
            request["batch_id"] = batch_id # want to set it here
            request["data"] = data
            
            headers = {
                "Content-Type": "application/json"
            }

            response = requests.post(endpoint, headers=headers, data=json.dumps(request))
            response_data = json.loads(response.text)

            for item in response_data["data"]:
                request_id = item["request_id"]
                response_value = item["response"]
                await redis_client.hset("hash", request_id, response_value)

        else:
            await asyncio.sleep(0.0001)


async def main():
    model_endpoints = [
        "http://localhost:7000/model1",
        "http://localhost:7000/model2",
        "http://localhost:7000/model3",
        "http://localhost:7000/model4"
    ]


    tasks = []
    for endpoint in model_endpoints:
        # Launch worker tasks using asyncio.create_task
        task = asyncio.create_task(batch_processing(endpoint))
        tasks.append(task)

    # Wait for all tasks to complete (optional)
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
