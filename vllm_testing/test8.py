import time
import asyncio
import aiohttp

# This dictionary should be shared across all tasks
shared_dict = {
    "total processes": 0,
    "minimum request break point": 10000
}

async def emulate_user(lock):
    api_key = "token-abc123"
    endpoint = "http://122.176.159.126:8000/v1/chat/completions"

    payload = {
        "model": "TheBloke/Amethyst-13B-Mistral-GPTQ",
        "messages": [ 
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
                "role": "assistant",
                "content": "hgghghg: That's good to hear, my dear. I'm glad you're managing your time well and still finding the energy for your hobbies. You know how important it is to stay focused on your goals while also taking care of yourself. Speaking of which, have you been eating properly? Are there any particular dishes you miss from home? Perhaps we could try making some together when we have the chance."
            },
            {
                "role": "autogenerate",
                "content": "Yugansh Arora:"
            }
        ],
        "stop": ["###","\n\n"],
        "frequency_penalty": 0.5,
        "presence_penalty": 0.5,
        "max_tokens": 250,
        "stream": True,
        "temperature": 0.8,
        "seed": -1,
        "repetition_penalty": 1.15
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        'Content-Type': 'application/json',
    }


    async with aiohttp.ClientSession() as session:
        async with lock:
            shared_dict["total processes"] += 1
            total_requests_in_queue = shared_dict["total processes"]

        try:
            start_time = time.time()
            first_token = True

            async with session.post(endpoint, json=payload, headers=headers) as response:
                async for data, _ in response.content.iter_chunks():
                    if first_token:
                        first_token_time = time.time()
                        first_token = False
                    #print(data)

            end_time = time.time()

            print(f"Total Requests in Queue {total_requests_in_queue} | Total Response Time: {end_time-start_time} | First Token Time: {first_token_time-start_time}")

        except Exception as e:
            async with lock:
                shared_dict["minimum request break point"] = min(total_requests_in_queue, shared_dict["minimum request break point"])
                print(f"New value of least errors in queue: {shared_dict['minimum request break point']} | Error: {e} | Requests: {total_requests_in_queue}")

        async with lock:
            shared_dict["total processes"] -= 1


async def main():
    max_concurrent_processes = 10
    background_tasks = set()

    lock = asyncio.Lock()

    for _ in range(max_concurrent_processes):
        task = asyncio.create_task(emulate_user(lock))
        background_tasks.add(task)

    await asyncio.gather(*background_tasks)

    async with lock:
        print(f"\nTotal processes left : {shared_dict['total processes']}")
        print(f"Minimum Breakpoint: {shared_dict['minimum request break point']}")



if __name__ == "__main__":
    asyncio.run(main())

