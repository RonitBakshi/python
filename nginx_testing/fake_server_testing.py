import httpx
import asyncio
from multiprocessing import Process, Manager
from pydantic import BaseModel

class RequestPayload(BaseModel):
    text: str

def send_request(url, payload, response_queue):
    async def fetch(client, url, payload):
        print("hello")
        response = await client.post(url, json=payload.dict())
        return response.text

    async def main():
        try:
            async with httpx.AsyncClient() as client:
                result = await fetch(client, url, payload)
                response_queue.put(result)
        except Exception as e:
            response_queue.put(e)

    asyncio.run(main())

def process_request(url, payload, response_queue):
    send_request(url, payload, response_queue)

if __name__ == "__main__":
    url = "http://localhost:8005/v1/chat/completions"  # Replace with your NGINX endpoint
    payload = RequestPayload(text="test")
    num_requests = 12  # Number of requests to send

    # Create a manager to handle shared state
    manager = Manager()
    response_queue = manager.Queue()

    # Create and start processes
    processes = []
    for _ in range(num_requests):
        p = Process(target=process_request, args=(url, payload, response_queue))
        processes.append(p)
        p.start()

    # Collect all responses
    all_responses = []
    for p in processes:
        p.join()
        while not response_queue.empty():
            all_responses.append(response_queue.get())

    # Print all responses
    for i, response in enumerate(all_responses):
        print(f"Response {i + 1}: {response}")
