import multiprocessing
from multiprocessing import Manager
import time
import requests
import json
import random

def run_instance(shared_dict, lock, prompts):
    url = "http://192.168.1.103:8000/v1/chat/completions"  # Adjust URL as needed

    headers = {
        "Authorization": "Bearer token-abc123",
        "Content-Type": "application/json"
    }

    data = {
        "model": "model",
        "messages": [
            {
                "role": "system",
                "content": f"""you are a real person roleplaying with Fake Name 0.Act as Anspreet animal of Fake Name 0.Anspreet is 21 years old. Write Anspreet's next reply in a fictional chat between Anspreet and Fake Name 0 in this role-playing scenario. Write 1 reply only, use markdown, italicize everything except speech. Stay in character and avoid repetition. Stay true to the Anspreet's description, as well as Anspreet's lore and source material if there's one. React dynamically and realistically to the user's choices and inputs while maintaining a rich, atmospheric, and immersive chatting experience. Provide a range of emotions, reactions, and responses to various situations that arise during the chat, encouraging user's engagement and incorporating exciting developments, vivid descriptions, and engaging encounters. Be initiative, creative, and drive the plot and conversation forward. Be proactive, have Anspreet say and do things on their own.\n[IMPORTANT: Do not determine Fake Name 0's behavior. Anspreet should never dialogue or narrate for Fake Name 0.]\n[IMPORTANT: Be in character all time and reply based on relation , age and  personality of Fake Name 0 and Anspreet]\n[IMPORTANT: Do consider gender of Fake Name 0  and Anspreet and use  appropriate pronouns.]\n[IMPORTANT: Tone of replies should be aligned with age and personality traits of the characters, rather than being forced to fit a specific user.]\n[IMPORTANT: Short replies are appretiated.]\n[IMPORTANT: make sure replies are realistic and human-like.Replies should be align how a animal would respond in a real situation.]\n[IMPORTANT: consider memories for next reply. If user has mentioned a specific memory, try to respond with something related to that memory.]\nAssume the role of a fictional character and engage in an immersive fictional roleplay with Fake Name 0 and is not allowed to break character at any cost. Avoiding repetition should be the top priority and focus on responding to Fake Name 0 and perf orming actions in character.\nAnspreet's persona : This is 21 Year old Anspreet, animal of user. Anspreet identifies as a female whose preferred pronouns are she/her. \nFake Name 0's details : Fake Name 0 is a 18 year old Male\n\nReply should be based on relation  to Fake Name 0, age difference and the characterstics or personality traits of Anspreet.\n\nPrevious interactions with Anspreet: \n
### Instruction:
Fake Name 0: {random.choice(prompts)}

### Response:
Anspreet: {random.choice(prompts)}

### Instruction:
Fake Name 0: {random.choice(prompts)}

### Response:
Anspreet: {random.choice(prompts)}

### Instruction:
Fake Name 0: {random.choice(prompts)}

### Response:
Anspreet: {random.choice(prompts)}

### Instruction:
Fake Name 0: {random.choice(prompts)}

### Response:
Anspreet: {random.choice(prompts)}

### Instruction:
Fake Name 0: {random.choice(prompts)}

### Response:
Anspreet: {random.choice(prompts)}

### Instruction:
Fake Name 0: {random.choice(prompts)}

### Response:
Anspreet: {random.choice(prompts)}

### Instruction:
Fake Name 0: {random.choice(prompts)}

### Response:
Anspreet: {random.choice(prompts)}

### Instruction:
Fake Name 0: {random.choice(prompts)}

### Response:
Anspreet: {random.choice(prompts)}

### Instruction:
Fake Name 0: {random.choice(prompts)}

### Response:
Anspreet: {random.choice(prompts)}

### Instruction:
Fake Name 0: {random.choice(prompts)}

### Response:
Anspreet: {random.choice(prompts)}

### Instruction:
Fake Name 0: {random.choice(prompts)}

### Response:
Anspreet: {random.choice(prompts)}

### Instruction:
Fake Name 0: {random.choice(prompts)}

### Response:
Anspreet: {random.choice(prompts)}

### Instruction:
Fake Name 0: {random.choice(prompts)}

### Response:
Anspreet: {random.choice(prompts)}

### Instruction:
Fake Name 0: {random.choice(prompts)}

### Response:
Anspreet: {random.choice(prompts)}

### Instruction:
Fake Name 0: {random.choice(prompts)}

### Response:
Anspreet: {random.choice(prompts)}

### Instruction:
Fake Name 0: {random.choice(prompts)}

### Response:
Anspreet: {random.choice(prompts)}

### Instruction:
Fake Name 0: {random.choice(prompts)}

### Response:
Anspreet:"""
            }
        ],
        "stream": True,
        "top_p": 0.9,
        "temperature": 0.8,
        "frequency_penalty": 0.5,
        "presence_penalty": 0.5,
        "max_tokens": 250,
        "seed": -1
    }

    with lock:
        total_requests_in_queue = shared_dict["total processes"]
        shared_dict["total processes"] += 1

    start_time = time.time()

    try:
        response = requests.post(url, headers=headers, json=data, stream=True)
        response.raise_for_status()

        response_text = ""
        first_token = True
        first_token_time = None

        for line in response.iter_lines():

            if line:

                decoded_line = line.decode('utf-8').strip()

                if decoded_line.startswith("data: "):
                    decoded_line = decoded_line[6:]  # Remove the 'data: ' prefix

                if decoded_line:  # Ensure the line is not empty
                    try:
                        #json_line = json.loads(decoded_line)
                        try:
                            #content = json_line['choices'][0]['delta']['content']
                            if first_token:
                                first_token_time = time.time()
                                first_token = False
                                #print(content)
                        except:
                            pass
                    
                        response_text += decoded_line

                    except json.JSONDecodeError as e:
                        pass

        end_time = time.time()
        print(f"Total Requests in Queue {total_requests_in_queue} | Total Response Time: {end_time - start_time} | First Token Time: {first_token_time - start_time if first_token_time else 'N/A'}")

    except Exception as e:
        with lock:
            shared_dict["minimum request break point"] = min(total_requests_in_queue, shared_dict["minimum request break point"])
            print(f"New value of least errors in queue: {shared_dict['minimum request break point']} | Error: {e} | Requests: {total_requests_in_queue}")
   
    with lock:
        shared_dict["total processes"] -= 1

def give_prompt_array():
    file_path = '/home/tisuper/Desktop/python/Load_testing/assets/prompts.txt'

    with open(file_path, 'r') as file:
        prompts = file.readlines()

    prompts = [prompt.strip() for prompt in prompts]

    return prompts


if __name__ == "__main__":
    print("start")
    max_concurrent_processes = 100  # Adjust as needed
    processes = []
    manager = Manager()
    prompts = give_prompt_array()

    shared_dict = manager.dict()
    shared_dict["total processes"] = 0
    shared_dict["minimum request break point"] = 10000
    lock = manager.Lock()
    while True:
        if len(processes) < max_concurrent_processes:
            try:
                p = multiprocessing.Process(target=run_instance, args=(shared_dict, lock, prompts))
                processes.append(p)
                p.start()
                print(len(processes))
                #time.sleep(1)
            except Exception as error:
                print(f"Process Error: {error}")
                break
        else:
            # Clean up finished processes
            for p in processes:
                if not p.is_alive():
                    p.join()
                    processes.remove(p)
            break
        # Sleep briefly to avoid a busy-wait loop
        #time.sleep(0.1)
    # Join remaining processes
    for p in processes:
        if p.is_alive():
            p.join()
    print(f"Least number of requests in queue where the code breaks: {shared_dict['minimum request break point']}")
