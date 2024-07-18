import requests
import json

url = "http://192.168.1.34:5000/v1/chat/completions"

headers = {
    "Content-Type":"application/json"
}

body = {
    "messages": [
        {
            "role": "user",
            "content": "*Sumit raises from his chair*\nWhat if I were to tell you that he is a key element to all of this !!! The dog lies at the heart of this mystery, only you are too self involved to see it."
        }
    ],
    "mode": "chat",
    "model": "chronos-hermes-13b-v2.Q4_K_M.gguf",
    "character": "Marlowe",
    "name1": "Sumit",
    "name2": "Marlowe",
    "stream": False,
    "temperature": 2,
    "top_p": 0.7,
    "top_k": 100,
    "repetition_penalty": 1,
    "max_tokens": 4096,
    "user": "Sumit",
    "guidance_scale": 1
}

response = requests.post(url, headers=headers, data=json.dumps(body))

print(response.status_code)
print(response.text)  