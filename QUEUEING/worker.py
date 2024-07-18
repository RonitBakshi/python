import redis
import json
import asyncio

# Connect to Redis (replace with your actual connection details)
redis_url = 'rediss://default:AVNS_8yYBIS_I3QFT7P0uI6m@caching-120e037e-ronit-0e44.e.aivencloud.com:21605'
redis_client = redis.asyncio.from_url(redis_url, decode_responses=True)

async def process_data(prompts, endpoint):

    responses = []
    # Simulate processing
    for prompt in prompts:
        responses.append(f"{prompt} : {endpoint}")

    await asyncio.sleep(6)
    return responses


async def batch_processing(endpoint):
    while True:
        queue_length = await redis_client.llen('request_queue')
        if queue_length > 0:
            i = 0
            request_ids = []
            prompts = []

            while i < 6 and queue_length > 0:
                message = await redis_client.rpop('request_queue')
                if message is None:
                    break
                request = json.loads(message)
                request_id = request['request_id']
                data = request['data']

                request_ids.append(request_id)
                prompts.append(data)
                i += 1
                queue_length -= 1

            # Process the data
            responses = await process_data(prompts, endpoint)

            for i in range(len(responses)):
                response_payload = {
                    'request_id': request_ids[i],
                    'result': responses[i]
                }

                await redis_client.hset("hash", request_ids[i], json.dumps(response_payload))
        else:
            await asyncio.sleep(1)


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
