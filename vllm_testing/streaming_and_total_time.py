import multiprocessing
from multiprocessing import Manager
import time
from openai import OpenAI

def run_instance(shared_dict, lock):
    client = OpenAI(
        base_url="http://192.168.1.103:8001/v1", # "http://192.168.1.102:8000/v1"
        api_key="token-abc123",
    )

    with lock:
        total_requests_in_queue = shared_dict["total processes"]
        shared_dict["total processes"] += 1

    start_time = time.time()

    try:
        completion = client.chat.completions.create(
            model="model",
            messages = [ 
                {
                    "role": "system",
                    "content": """you are a real person roleplaying with Fake Name 0.Act as Anspreet animal of Fake Name 0.Anspreet is 21 years old. Write Anspreet's next reply in a fictional chat between Anspreet and Fake Name 0 in this role-playing scenario. Write 1 reply only, use markdown, italicize everything except speech. Stay in character and avoid repetition. Stay true to the Anspreet's description, as well as Anspreet's lore and source material if there's one. React dynamically and realistically to the user's choices and inputs while maintaining a rich, atmospheric, and immersive chatting experience. Provide a range of emotions, reactions, and responses to various situations that arise during the chat, encouraging user's engagement and incorporating exciting developments, vivid descriptions, and engaging encounters. Be initiative, creative, and drive the plot and conversation forward. Be proactive, have Anspreet say and do things on their own.\n[IMPORTANT: Do not determine Fake Name 0's behavior. Anspreet should never dialogue or narrate for Fake Name 0.]\n[IMPORTANT: Be in character all time and reply based on relation , age and  personality of Fake Name 0 and Anspreet]\n[IMPORTANT: Do consider gender of Fake Name 0  and Anspreet and use  appropriate pronouns.]\n[IMPORTANT: Tone of replies should be aligned with age and personality traits of the characters, rather than being forced to fit a specific user.]\n[IMPORTANT: Short replies are appretiated.]\n[IMPORTANT: make sure replies are realistic and human-like.Replies should be align how a animal would respond in a real situation.]\n[IMPORTANT: consider memories for next reply. If user has mentioned a specific memory, try to respond with something related to that memory.]\nAssume the role of a fictional character and engage in an immersive fictional roleplay with Fake Name 0 and is not allowed to break character at any cost. Avoiding repetition should be the top priority and focus on responding to Fake Name 0 and perf orming actions in character.\nAnspreet's persona : This is 21 Year old Anspreet, animal of user. Anspreet identifies as a female whose preferred pronouns are she/her. \nFake Name 0's details : Fake Name 0 is a 18 year old Male\n\nReply should be based on relation  to Fake Name 0, age difference and the characterstics or personality traits of Anspreet.\n\nPrevious interactions with Anspreet: \n\n### Instruction:\nFake Name 0: The field of artificial intelligence is evolving rapidly, with new applications and capabilities emerging all the time. I'm particularly interested in the ethical considerations surrounding AI, such as bias in algorithms, job displacement, and the potential for misuse. How can we ensure that AI is developed and deployed responsibly, and what measures are being taken to address these concerns?\n\n### Response:\nAnspreet: Sure, I'd be happy to explain some of the potential uses of blockchain technology beyond finance. Here are a few examples:\n\n### Instruction:\nFake Name 0: I've been reading about the potential health benefits of a plant-based diet. Many people claim that it can improve overall health, reduce the risk of chronic diseases, and support environmental sustainability. I'm curious about the nutritional aspects of a plant-based diet and how to ensure that I'm getting all the essential nutrients. What should I consider when transitioning to a plant-based diet?\n\n### Response:\nAnspreet: You're right to be cautious about the potential risks of AI. As for ethical considerations, here are some steps that can be taken to address them:\n\n### Instruction:\nFake Name 0: Mental health awareness has become increasingly important in recent years. I've been reading about the various ways people can support their mental well-being, such as through therapy, mindfulness practices, and maintaining strong social connections. What are some effective strategies for managing stress and anxiety in today's fast-paced world?\n\n### Response:\nAnspreet: That's a great question. To ensure that AI is developed and deployed responsibly, we can take several steps:\n\n### Instruction:\nFake Name 0: Sustainable living is a topic that has gained a lot of attention in recent years. Many people are looking for ways to reduce their environmental impact and live more eco-friendly lives. I'm interested in practical steps that individuals can take to live sustainably, from reducing waste and conserving energy to supporting renewable resources. What are some effective strategies for sustainable living?\n\n### Response:\nAnspreet: To create a balanced workout routine, you can consider incorporating the following elements:\n\n### Instruction:\nFake Name 0: I've always been fascinated by the history of ancient civilizations. From the pyramids of Egypt to the ruins of Machu Picchu, these ancient structures hold many mysteries. I'm curious about the engineering and architectural feats achieved by these civilizations with the limited technology available at the time. What are some of the most intriguing discoveries in the field of archaeology?\n\n### Response:\nAnspreet: Ronit Bakshi: Ronit looked at her, still undecided. 'What about your job?' He asked after a while.\n\n### Instruction:\nFake Name 0: The concept of blockchain technology is often associated with cryptocurrencies, but I've read that it has potential applications far beyond digital currencies. I'm interested in understanding how blockchain works and what other industries might benefit from this technology. Can you explain some of the most promising use cases for blockchain outside of finance?\n\n### Response:\nAnspreet: To help you manage stress and anxiety, here are some effective strategies:\n\n### Instruction:\nFake Name 0: The rapid advancement of technology has transformed many aspects of our lives, from the way we communicate to how we work and entertain ourselves. While technology offers many benefits, there are also concerns about its impact on privacy, security, and human interaction. How can we balance the advantages of technological innovation with the potential drawbacks, and what measures can we take to ensure responsible use of technology?\n\n### Response:\nAnspreet: To live sustainably, here are some effective strategies:\n\n### Instruction:\nFake Name 0: The field of artificial intelligence is evolving rapidly, with new applications and capabilities emerging all the time. I'm particularly interested in the ethical considerations surrounding AI, such as bias in algorithms, job displacement, and the potential for misuse. How can we ensure that AI is developed and deployed responsibly, and what measures are being taken to address these concerns?\n\n### Response:\nAnspreet: Intriguing discoveries in the field of archaeology include:\n\n### Instruction:\nFake Name 0: The concept of parallel universes and the multiverse theory is a popular topic in science fiction, but some physicists consider it a legitimate area of scientific inquiry. I'm curious about the current theories and evidence supporting the existence of parallel universes, and how we might ever prove or disprove their existence. What are the latest developments in this field of study?\n\n### Response:\nAnspreet: To manage stress and anxiety, consider these practical tips:\n\n### Instruction:\nFake Name 0: Sustainable living is a topic that has gained a lot of attention in recent years. Many people are looking for ways to reduce their environmental impact and live more eco-friendly lives. I'm interested in practical steps that individuals can take to live sustainably, from reducing waste and conserving energy to supporting renewable resources. What are some effective strategies for sustainable living?\n\n### Response:\nAnspreet: To live sustainably, consider the following strategies:\n\n### Instruction:\nFake Name 0: The rapid advancement of technology has transformed many aspects of our lives, from the way we communicate to how we work and entertain ourselves. While technology offers many benefits, there are also concerns about its impact on privacy, security, and human interaction. How can we balance the advantages of technological innovation with the potential drawbacks, and what measures can we take to ensure responsible use of technology?\n\n### Response:\nAnspreet: To manage stress and anxiety, consider these practical tips:\n\n### Instruction:\nFake Name 0: I've been reading about the benefits of mindfulness and meditation for mental health. These practices are said to reduce stress, improve focus, and enhance overall well-being. I'm interested in learning more about different meditation techniques and how to incorporate mindfulness into my daily routine. What are some practical tips for getting started with mindfulness and making it a regular part of my life?\n\n### Response:\nAnspreet: To manage stress and anxiety, consider these practical tips:\n\n### Instruction:\nFake Name 0: I've been reading about the potential health benefits of a plant-based diet. Many people claim that it can improve overall health, reduce the risk of chronic diseases, and support environmental sustainability. I'm curious about the nutritional aspects of a plant-based diet and how to ensure that I'm getting all the essential nutrients. What should I consider when transitioning to a plant-based diet?\n\n### Response:\nAnspreet: To manage stress and anxiety, consider these practical tips:\n\n### Instruction:\nFake Name 0: Sustainable living is a topic that has gained a lot of attention in recent years. Many people are looking for ways to reduce their environmental impact and live more eco-friendly lives. I'm interested in practical steps that individuals can take to live sustainably, from reducing waste and conserving energy to supporting renewable resources. What are some effective strategies for sustainable living?\n\n### Response:\nAnspreet: To ensure a healthy and balanced plant-based diet, consider the following:\n\n### Instruction:\nFake Name 0: The issue of climate change and its impact on the environment is one of the most pressing challenges of our time. Many species are facing habitat loss, changes in food availability, and other challenges due to shifting climate patterns. I'm interested in learning more about the efforts being made to protect endangered species and preserve biodiversity. What are some successful conservation strategies being implemented around the world?\n\n### Response:\nAnspreet: Blockchain technology has the potential to transform various industries, such as supply chain management, healthcare, and even voting systems. Some of the most promising use cases include:\n\n### Instruction:\nFake Name 0: The advancements in genetic research and biotechnology have opened up new possibilities for personalized medicine and treatments for genetic disorders. I'm interested in understanding how these technologies work and what ethical considerations need to be addressed. What are some of the most promising developments in genetic research, and how might they impact healthcare in the future?\n\n### Response:\nAnspreet: To manage stress and anxiety, consider these practical tips:\n\n### Instruction:\nFake Name 0: Mental health awareness has become increasingly important in recent years. Many people are recognizing the value of taking care of their mental well-being, just as they do their physical health. I'm interested in learning more about effective strategies for managing stress, anxiety, and depression. What are some practical tips for maintaining good mental health in today's fast-paced world?\n\n### Response:\nAnspreet: To manage stress and anxiety, consider these practical tips:\n\n### Instruction:\nFake Name 0: The rapid advancement of technology has transformed many aspects of our lives, from the way we communicate to how we work and entertain ourselves. While technology offers many benefits, there are also concerns about its impact on privacy, security, and human interaction. How can we balance the advantages of technological innovation with the potential drawbacks, and what measures can we take to ensure responsible use of technology?\n\n### Response:\nAnspreet: To manage stress and anxiety, consider these practical tips:\n\n### Instruction:\nFake Name 0: With the advent of quantum computing, there has been a lot of excitement about its potential to revolutionize various industries. I'm interested in understanding how quantum computers differ from classical computers and what kinds of problems they can solve more efficiently. What are some of the most promising applications of quantum computing, and how soon might we see them in practice?\n\n### Response:\nAnspreet: To manage stress and anxiety, consider these practical tips:\n\n### Instruction:\nFake Name 0: The field of artificial intelligence is evolving rapidly, with new applications and capabilities emerging all the time. I'm particularly interested in the ethical considerations surrounding AI, such as bias in algorithms, job displacement, and the potential for misuse. How can we ensure that AI is developed and deployed responsibly, and what measures are being taken to address these concerns?\n\n### Response:\nAnspreet: To manage stress and anxiety, consider these practical tips:\n\n### Instruction:\nFake Name 0: I've been hearing a lot about the benefits of a plant-based diet recently. Many people claim that it can improve health, boost energy levels, and even contribute to environmental sustainability. I'm curious about the nutritional aspects of a plant-based diet and how to ensure that I'm getting all the essential nutrients if I decide to make the switch.\n\n### Response:\nAnspreet: To manage stress and anxiety, consider these practical tips:\n\n### Instruction:\nFake Name 0: I've been reading about the benefits of mindfulness and meditation for mental health. These practices are said to reduce stress, improve focus, and enhance overall well-being. I'm interested in learning more about different meditation techniques and how to incorporate mindfulness into my daily routine. What are some practical tips for getting started with mindfulness?\n\n### Response:\nAnspreet: To manage stress and anxiety, consider these practical tips:\n\n### Instruction:\nFake Name 0: The advancements in genetic research and biotechnology have opened up new possibilities for personalized medicine and treatments for genetic disorders. I'm interested in understanding how these technologies work and what ethical considerations need to be addressed. What are some of the most promising developments in genetic research, and how might they impact healthcare in the future?\n\n### Response:\nAnspreet:"""
                }
            ],
            stream = True,
            top_p = 0.9,
            stop=["###","\n\n"],
            temperature = 0.8,
            frequency_penalty = 0.5,
            presence_penalty = 0.5,
            max_tokens = 250,
            seed = -1,
        )

        response = ""

        first_token = True
        first_token_time = None

        for text in completion:
            if text.choices[0].delta.content:
                if first_token:
                    #print(text,'\n\n')
                    first_token_time = time.time()
                    first_token = False
                response += text.choices[0].delta.content

        end_time = time.time()

        # print(response)
        print(f"Total Requests in Queue {total_requests_in_queue} | Total Response Time: {end_time-start_time} | First Token Time: {first_token_time-start_time}")

    except Exception as e:
        with lock:
            shared_dict["minimum request break point"] = min(total_requests_in_queue, shared_dict["minimum request break point"])
            print(f"New value of least errors in queue: {shared_dict['minimum request break point']} | Error: {e} | Requests: {total_requests_in_queue}")

    with lock:
        shared_dict["total processes"] -= 1

    
if __name__ == "__main__":

    print("start")
    max_concurrent_processes = 50
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