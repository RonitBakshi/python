import socketio
import time
import json
import asyncio
import re
import random

async def handle_socket_request(server_url, namespace, user_details, prompts):
    headers = {
        'User-Info': json.dumps({
            'email': user_details['email'],
            'sub': user_details['kid']
        })
    }

    request_data = {
        'action': 'getMessageResponse',
        'body': {'content': random.choice(prompts)},
        'params': {'characterId': '66828afc93039b75dad55693'},
        'user': {
            'email': user_details['email'],
            'kid': user_details['kid']
        }
    }

    sio = socketio.AsyncClient()

    emit_time = None
    first_response_time = None
    last_response_time = None
    first_token = True

    @sio.event
    async def connect():
        print('Connected to the server')

    @sio.event
    async def connect_error(data):
        print(f'Failed to connect to the server: {data}')

    @sio.event
    async def disconnect():
        print('Disconnected from server')

    @sio.event
    async def chat(response):
        nonlocal first_response_time, last_response_time, first_token, emit_time

        if response['action'] == 'getMessageResponse':
            if first_token:
                first_token = False
                first_response_time = time.time()
                print(response, first_response_time)
                
            if 'message' in response and response['message'] == 'Message sent successfully':
                last_response_time = time.time()

                first_token_time = first_response_time - emit_time
                complete_token_time = last_response_time - emit_time

                print(f"First Token Time: {first_token_time} | Complete Token Time: {complete_token_time}")

                await sio.disconnect()

    try:
        await sio.connect(server_url + namespace, headers=headers)
        emit_time = time.time()
        await sio.emit('chat', request_data)
        await sio.wait()
    except socketio.exceptions.ConnectionError as e:
        print(f'Connection error: {e}')
    finally:
        await sio.disconnect()


def extract_data(line):
    pattern = r"EMAIL: (.+?) \| KID: (.+?) \| NAME: (.+)"

    match = re.match(pattern, line)
    if match:
        email = match.group(1)
        kid = match.group(2)
        name = match.group(3)
        return {
            'email': email, 
            'kid': kid, 
            'name': name
        }
    return None


def give_prompt_array():
    file_path = '/home/tisuper/Desktop/python/Load_testing/assets/prompts.txt'

    with open(file_path, 'r') as file:
        prompts = file.readlines()

    prompts = [prompt.strip() for prompt in prompts]

    return prompts


async def process_creator():
    print(f'start time: {time.time()}\n\n')
    server_url = 'http://localhost:3001'
    namespace = "/chat/66828afc93039b75dad55693"
    num_requests = 10  # Number of requests to send
    file_path = "socket_tests/user_data.txt"
    tasks = []

    prompts = give_prompt_array()

    with open(file_path, "r") as file:
        for _ in range(num_requests):
            user_data = file.readline()
            extracted_user_data = extract_data(user_data.strip())
            task = asyncio.create_task(handle_socket_request(server_url, namespace, extracted_user_data, prompts))
            tasks.append(task)

        await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(process_creator())
