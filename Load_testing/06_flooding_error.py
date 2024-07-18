import multiprocessing
from multiprocessing import Manager
import requests
import random
import json

def run_instance(url, prompts, character_names, headers, shared_dict):
    prompt = random.choice(prompts).strip()
    character = random.choice(character_names)

    body = {
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "mode": "chat",
        "model": "chronos-hermes-13b-v2.Q4_K_M.gguf",
        "character": character,
        "name1": "Sumit",
        "name2": character,
        "stream": False,
        "temperature": 2,
        "top_p": 0.7,
        "top_k": 100,
        "repetition_penalty": 1,
        "max_tokens": 4096,
        "user": "Sumit",
        "guidance_scale": 1
    }

    total_requests_in_queue = shared_dict["total_processes"]
    print(total_requests_in_queue)

    shared_dict["total_processes"] += 1
    response = requests.post(url, headers=headers, data=json.dumps(body))
    shared_dict["total_processes"] -= 1

    if response.status_code != 200:
        shared_dict["error"] = total_requests_in_queue



if __name__ == "__main__":
    processes = []

    url = "http://192.168.1.34:5000/v1/chat/completions"

    with open("Load_testing/assets/prompts.txt", "r") as file:
        prompts = file.readlines()

    character_names = [
        "Marlowe",
        "Cassy",
        "Example"
    ]

    headers = {
        "Content-Type": "application/json"
    }

    manager = Manager()

    shared_dict = manager.dict()
    shared_dict["total_processes"] = 0
    shared_dict["error"] = -1

    while True:
        p = multiprocessing.Process(target=run_instance, args=(url, prompts, character_names, headers, shared_dict))
        processes.append(p)
        p.start()

        if shared_dict["error"] != -1:
            break

    for p in processes:
        p.join()

    print(f"Total requests: {shared_dict['error']}")