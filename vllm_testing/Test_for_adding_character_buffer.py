import httpx
import asyncio
import json
import random
import statistics
import time

async def give_prompt_array():
    file_path = 'assets/prompts.txt'

    with open(file_path, 'r') as file:
        prompts = file.readlines()

    prompts = [prompt.strip() for prompt in prompts]

    return prompts

async def run_single_instance(prompts):
    url = 'http://generation.chatreal.ai/v1/chat/completions'  # Adjust URL as needed
    inter_token_times = []
    per_character_times = []

    headers = {
        "Authorization": "Bearer 4way-LOVE@2023",
        "Content-Type": "application/json"
    }

    data = {
        "model": "model",
        "messages": [
            {
                "role": "system",
                "content": f"""you are a real person roleplaying with Fake Name 0. Act as Anspreet animal of Fake Name 0. Anspreet is 21 years old. Write Anspreet's next reply in a fictional chat between Anspreet and Fake Name 0 in this role-playing scenario. Write 1 reply only, use markdown, italicize everything except speech. Stay in character and avoid repetition. Stay true to Anspreet's description, as well as Anspreet's lore and source material if there's one. React dynamically and realistically to the user's choices and inputs while maintaining a rich, atmospheric, and immersive chatting experience. Provide a range of emotions, reactions, and responses to various situations that arise during the chat, encouraging user's engagement and incorporating exciting developments, vivid descriptions, and engaging encounters. Be initiative, creative, and drive the plot and conversation forward. Be proactive, have Anspreet say and do things on their own.\n[IMPORTANT: Do not determine Fake Name 0's behavior. Anspreet should never dialogue or narrate for Fake Name 0.]\n[IMPORTANT: Be in character all time and reply based on relation , age and  personality of Fake Name 0 and Anspreet]\n[IMPORTANT: Do consider gender of Fake Name 0  and Anspreet and use  appropriate pronouns.]\n[IMPORTANT: Tone of replies should be aligned with age and personality traits of the characters, rather than being forced to fit a specific user.]\n[IMPORTANT: Short replies are appretiated.]\n[IMPORTANT: make sure replies are realistic and human-like. Replies should be align how a animal would respond in a real situation.]\n[IMPORTANT: consider memories for next reply. If user has mentioned a specific memory, try to respond with something related to that memory.]\nAssume the role of a fictional character and engage in an immersive fictional roleplay with Fake Name 0 and is not allowed to break character at any cost. Avoiding repetition should be the top priority and focus on responding to Fake Name 0 and performing actions in character.\nAnspreet's persona: This is 21 Year old Anspreet, animal of user. Anspreet identifies as a female whose preferred pronouns are she/her. \nFake Name 0's details: Fake Name 0 is a 18 year old Male\n\nReply should be based on relation to Fake Name 0, age difference and the characteristics or personality traits of Anspreet.\n\nPrevious interactions with Anspreet:

### Instruction:
Fake Name 0: {random.choice(prompts)}

### Response:
Anspreet:"""
            }
        ],
        "stream": True,
        "top_p": 0.9,
        "temperature": 0.8,
        "stop": ['###', '\n\n'],
        "frequency_penalty": 0.5,
        "presence_penalty": 0.5,
        "max_tokens": 250,
        "seed": -1
    }

    print(data["messages"][0],end="\n\n\n")

    timeout = httpx.Timeout(60.0, read=600.0)

    async with httpx.AsyncClient(timeout=timeout) as client:
        start_time = time.time()
        async with client.stream("POST", url, headers=headers, json=data) as response:
            response.raise_for_status()
            first_token = True
            first_token_time = None
            previous_token_time = time.time()  # Initialize this here

            async for line in response.aiter_lines():
                if line:
                    decoded_line = line.strip()

                    if decoded_line.startswith("data: "):
                        decoded_line = decoded_line[6:]  # Remove the 'data: ' prefix

                    if decoded_line:  # Ensure the line is not empty
                        try:
                            json_line = json.loads(decoded_line)
                            try:
                                content = json_line['choices'][0]['delta']['content']

                                if content:
                                    
                                    #print(len(content),end=" ",flush=True)

                                    #printing charcter by character
                                    for character in content:
                                       print(character,end="",flush=True)
                                       #await asyncio.sleep(0.050) #0.06

                                    # printing token by token
                                    #print(content, end='', flush=True)
                                    #await asyncio.sleep(0.5)                               

                                    if first_token and content:
                                        first_token_time = time.time()
                                        previous_token_time = time.time()
                                        first_token = False
                                    else:
                                        current_token_time = time.time()
                                        inter_token_time = current_token_time - previous_token_time
                                        previous_token_time = time.time()
                                        inter_token_times.append(inter_token_time)
                                        per_character_times .append(inter_token_time/len(content))

                                #await asyncio.sleep(0.5)
                            except KeyError:
                                pass

                        except json.JSONDecodeError:
                            pass

        end_time = time.time()

        if first_token_time:
            print(f"\n\nFirst Token Time: {first_token_time - start_time}")

        #print(f"Total Response Time: {end_time - start_time}")
        #print(f"Max ITL: {max(inter_token_times)}")
        #print(f"Min ITL: {min(inter_token_times)}")
        #print(f"Mean ITL: {statistics.mean(inter_token_times)}")
        #print(f"Variance of ITL: {statistics.variance(inter_token_times)}")
        #print(f"Max time per character: {max(per_character_times)}")
        #print(f"Average time per character: {statistics.mean(per_character_times)}")

        #print(f"\nAll Inter Token times")
        #for inter_token_time in inter_token_times:
            #print(("%.2f" % inter_token_time),end=" ")


        #print(f"\n\nGeneration time per character:")
        #for per_character_time in per_character_times:
           # print(("%.3f" % per_character_time),end=" ")

        print("")

async def main():
    prompts = await give_prompt_array()
    await run_single_instance(prompts)

if __name__ == "__main__":
    print("Start\n")
    asyncio.run(main())
