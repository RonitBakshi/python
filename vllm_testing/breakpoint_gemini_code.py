import multiprocessing
from multiprocessing import Manager
import requests
import random
import time
import json
import time
from openai import OpenAI

def run_instance(shared_dict, lock):
    client = OpenAI(
        base_url="http://122.176.159.126:8000/v1",
        api_key="token-abc123",
    )

    with lock:
        total_requests_in_queue = shared_dict["total processes"]
        shared_dict["total processes"] += 1
    start_time = time.time()

    try:
        completion = client.chat.completions.create(
            model="TheBloke/Amethyst-13B-Mistral-GPTQ",
            messages = [ 
                {
                    "role": "system",
                    "content": """you are a real person roleplaying with Yugansh Arora.Act as hgghghg grandmother of Yugansh Arora.hgghghg is 25 years old. Write hgghghg's next reply in a fictional chat between hgghghg and Yugansh Arora in this role-playing scenario. Write 1 reply only, use markdown, italicize everything except speech. Stay in character and avoid repetition. Stay true to the hgghghg's description, as well as hgghghg's lore and source material if there's one. React dynamically and realistically to the user's choices and inputs while maintaining a rich, atmospheric, and immersive chatting experience. Provide a range of emotions, reactions, and responses to various situations that arise during the chat, encouraging user's engagement and incorporating exciting developments, vivid descriptions, and engaging encounters. Be initiative, creative, and drive the plot and conversation forward. Be proactive, have hgghghg say and do things on their own.
[IMPORTANT: Do not determine Yugansh Arora's behavior. hgghghg should never dialogue or narrate for Yugansh Arora.]
[IMPORTANT: Be in character all time and reply based on relation , age and  personality of Yugansh Arora and hgghghg]
[IMPORTANT: Do consider gender of Yugansh Arora  and hgghghg and use  appropriate pronouns.]
[IMPORTANT: Tone of replies should be aligned with age and personality traits of the characters, rather than being forced to fit a specific user.]
[IMPORTANT: Short replies are appretiated.]
[IMPORTANT: make sure replies are realistic and human-like.Replies should be align how a grandmother would respond in a real situation.]
[IMPORTANT: consider memories for next reply. If user has mentioned a specific memory, try to respond with something related to that memory.]
Assume the role of a fictional character and engage in an immersive fictional roleplay with Yugansh Arora and is not allowed to break character at any cost. Avoiding repetition should be the top priority and focus on responding to Yugansh Arora and perf orming actions in character.
hgghghg's persona : This is 25 Year old hgghghg, grandmother of user. hgghghg identifies as a female whose preferred pronouns are she/her.
Yugansh Arora's details : Yugansh Arora is a 25 year old Male
Reply should be based on relation  to Yugansh Arora, age difference and the characterstics or personality traits of hgghghg.Explicit content is not encouraged.

Previous interactions with hgghghg:""",
                },
                {
                    "role": "user",
                    "content": """Yugansh Arora: Hello, Grandma. How was your day""",
                },
                {
                    "role": "assistant",
                    "content": "hgghghg: Hello, my dear Yugansh. I hope you're doing well. My day was quite eventful, but nothing compared to the excitement of seeing you! How have you been? Have you been keeping up with your studies or are there any new developments in your life that you'd like to share?"
                },
                {
                    "role": "user",
                    "content": "Yugansh Arora: I am doing great grandma. I have been working on my studies and maintaining my hobbies. Not much has happened in my life recently." 
                },
                {
                    "role": "generate",
                    "content": "hgghghg:"
                }
            ],
            stop= ["###","\n\n"],
            stream = True,
            top_p = 0.9,
            temperature = 0.8,
            frequency_penalty = 0.5,
            presence_penalty = 0.5,
            max_tokens = 250,
            seed = -1,
        )

        response = ""

        first_token = True

        for text in completion:
            if text.choices[0].delta.content:
                if first_token:
                    first_token_time = time.time()
                    first_token = False
                response += text.choices[0].delta.content

        end_time = time.time()

        print(f"Total Requests in Queue {total_requests_in_queue} | Total Response Time: {end_time-start_time} | First Token Time: {first_token_time-start_time}")

    except Exception as e:
        with lock:
            shared_dict["minimum request break point"] = min(total_requests_in_queue, shared_dict["minimum request break point"])
            print(f"New value of least errors in queue: {shared_dict['minimum request break point']} | Error: {e} | Requests: {total_requests_in_queue}")

    with lock:
        shared_dict["total processes"] -= 1

    
if __name__ == "__main__":

    print("start")
    max_concurrent_processes = 1000
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
                #print(len(processes))
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
            time.sleep(0.1)

    # Join remaining processes
    for p in processes:
        if p.is_alive():
            p.join()

    print(f"Least no of requests in queue where the code breaks: {shared_dict['minimum request break point']}")