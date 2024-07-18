import requests
import json
import random
import time

url = "http://192.168.1.34:5000/v1/chat/completions"

headers = {
    "Content-Type": "application/json"
}

with open("Load_testing/assets/prompts.txt", "r") as file:
    prompts = file.readlines()

character_names = [
    "Marlowe",
    "Cassy",
    "Example"
]

with open("responses.txt", "w") as f:
    for i in range(100):
     
        prompt = random.choice(prompts).strip() 
        character = random.choice(character_names)

        # Create request body
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

        # Send request
        response = requests.post(url, headers=headers, data=json.dumps(body))

        # Write response to file
        #f.write(response.text + "\n")

        #f.write(str(response.status_code)+ "\n")
        print(str(response.status_code))
        #print(response.text + "\n")
        #print(f"Request {i+1} Status Code:", response.status_code)
        #time.sleep(0.001)
        # Pause for a random amount of time to simulate human-like behavior
        #time.sleep(random.uniform(0.5, 2.5))
