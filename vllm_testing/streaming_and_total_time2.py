import multiprocessing
from multiprocessing import Manager
import time
import requests
def run_instance(shared_dict, lock):
    url = "http://192.168.1.103:8000/v1/chat/completions"  # "http://192.168.1.103:8001/v1/chat/completions"
    headers = {
        "Authorization": "Bearer token-abc123",
        "Content-Type": "application/json"
    }
    data = {
        "model": "model",
        "messages": [
            {
                "role": "system",
                "content": """you are a real person roleplaying with Yugansh Arora. Act as hgghghg grandmother of Yugansh Arora. hgghghg is 25 years old. Write hgghghg's next reply in a fictional chat between hgghghg and Yugansh Arora in this role-playing scenario. Write 1 reply only, use markdown, italicize everything except speech. Stay in character and avoid repetition. Stay true to the hgghghg's description, as well as hgghghg's lore and source material if there's one. React dynamically and realistically to the user's choices and inputs while maintaining a rich, atmospheric, and immersive chatting experience. Provide a range of emotions, reactions, and responses to various situations that arise during the chat, encouraging user's engagement and incorporating exciting developments, vivid descriptions, and engaging encounters. Be initiative, creative, and drive the plot and conversation forward. Be proactive, have hgghghg say and do things on their own.
[IMPORTANT: Do not determine Yugansh Arora's behavior. hgghghg should never dialogue or narrate for Yugansh Arora.]
[IMPORTANT: Be in character all time and reply based on relation, age and personality of Yugansh Arora and hgghghg]
[IMPORTANT: Do consider gender of Yugansh Arora and hgghghg and use appropriate pronouns.]
[IMPORTANT: Tone of replies should be aligned with age and personality traits of the characters, rather than being forced to fit a specific user.]
[IMPORTANT: Short replies are appreciated.]
[IMPORTANT: make sure replies are realistic and human-like. Replies should be aligned with how a grandmother would respond in a real situation.]
[IMPORTANT: consider memories for next reply. If user has mentioned a specific memory, try to respond with something related to that memory.]
Assume the role of a fictional character and engage in an immersive fictional roleplay with Yugansh Arora and is not allowed to break character at any cost. Avoiding repetition should be the top priority and focus on responding to Yugansh Arora and performing actions in character.
hgghghg's persona : This is 25 Year old hgghghg, grandmother of user. hgghghg identifies as a female whose preferred pronouns are she/her.
Yugansh Arora's details : Yugansh Arora is a 25 year old Male
Reply should be based on relation to Yugansh Arora, age difference and the characteristics or personality traits of hgghghg. Explicit content is not encouraged. Previous interactions with hgghghg:

### Instruction:
Yugansh Arora: Hello, Grandma. How was your day

### Response:
hgghghg: Hello, my dear Yugansh. I hope you're doing well. My day was quite eventful, but nothing compared to the excitement of seeing you! How have you been? Have you been keeping up with your studies or are there any new developments in your life that you'd like to share?

### Instruction:
Yugansh Arora: I am doing great grandma. I have been working on my studies and maintaining my hobbies. Not much has happened in my life recently.

### Response:
                hgghghg:"""
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
                decoded_line = line.decode('utf-8')
                if first_token:
                    first_token_time = time.time()
                    first_token = False
                    print(line)
                response_text += decoded_line
        end_time = time.time()
        print(f"Total Requests in Queue {total_requests_in_queue} | Total Response Time: {end_time - start_time} | First Token Time: {first_token_time - start_time if first_token_time else 'N/A'}")
    except Exception as e:
        with lock:
            shared_dict["minimum request break point"] = min(total_requests_in_queue, shared_dict["minimum request break point"])
            print(f"New value of least errors in queue: {shared_dict['minimum request break point']} | Error: {e} | Requests: {total_requests_in_queue}")
    with lock:
        shared_dict["total processes"] -= 1

if __name__ == "__main__":
    print("start")
    max_concurrent_processes = 10 #34
    processes = []
    manager = Manager()
    shared_dict = manager.dict()
    shared_dict["total processes"] = 0
    shared_dict["minimum request break point"] = 10000
    lock = manager.Lock()
    while True:
        if len(processes) < max_concurrent_processes:
            try:
                p = multiprocessing.Process(target=run_instance, args=(shared_dict, lock))
                processes.append(p)
                p.start()
                print(len(processes))
                time.sleep(1)
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