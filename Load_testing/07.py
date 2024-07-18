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

    total_requests_in_queue = shared_dict["total processes"]

    shared_dict["total processes"] += 1

    try:
        response = requests.post(url, headers=headers, data=json.dumps(body))
        print(f"{total_requests_in_queue} : {response.status_code}")

    except Exception:
        shared_dict["minimum request break point"] = min(total_requests_in_queue,shared_dict["minimum request break point"])
        print(f"New value of least errors in queue: {shared_dict['minimum request break point']}")

    shared_dict["total processes"] -= 1

    
if __name__ == "__main__":
    processes = []

    url = "http://192.168.1.34:5001/v1/chat/completions"

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
    shared_dict["total processes"] = 0
    shared_dict["minimum request break point"] = 10000

    while True:
        try:
            p = multiprocessing.Process(target=run_instance, args=(url, prompts, character_names, headers, shared_dict))
            processes.append(p)
            p.start()
        except Exception as error:
            print(f"Process Error: {error}")
            break

    for p in processes:
        if p.is_alive():
            p.join()

    print(f"Least no of requests in queue where the code breaks: {shared_dict['minimum request break point']}")
