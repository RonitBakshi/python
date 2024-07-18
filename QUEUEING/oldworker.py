import redis
import json
import asyncio

# Connect to Redis (replace with your actual connection details)
redis_url = 'rediss://default:AVNS_8yYBIS_I3QFT7P0uI6m@caching-120e037e-ronit-0e44.e.aivencloud.com:21605'
redis_client = redis.asyncio.from_url(redis_url, decode_responses=True)

async def process_data(data, endpoint):
    # Simulate processing
    await asyncio.sleep(6)
    return f"Processed data: {data} at endpoint {endpoint}"


async def batch_processing(endpoint):

    while True:

        if redis_client.llen('request_queue'):
            message = await redis_client.rpop('request_queue')
            
            if message is None:
                # If message is None, it means the queue is empty, so we wait before trying again
                await asyncio.sleep(1)
                continue

            print(message)
            request = json.loads(message)
            request_id = request['request_id']
            data = request['data']

            # Process the data
            result = await process_data(data, endpoint)

            # Add the response to the 'response_queue'
            response_payload = {
                'request_id': request_id,
                'result': result
            }

            await redis_client.hset("hash", request_id, json.dumps(response_payload))


async def main():
    model_endpoints = [
        "localhost-1",
        "localhost-2",
        "localhost-3",
        "localhost-4"
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
