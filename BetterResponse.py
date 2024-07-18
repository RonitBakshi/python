from ctransformers import AutoModelForCausalLM
import os

model_paths = [
    "models/unholy-v2-13b.Q4_K_M.gguf"
    #,
    #"models/DaringMaid-20B-V1.1-Q4_K_M.gguf",
    #"models/Kuro-Lotus-10.7B-Q4_K_M.gguf",
    #"models/EstopianMaid.Q4_K_M.gguf",
    #"models/mythomax-l2-kimiko-v2-13b.Q4_K_M.gguf",
    #"models/capybarahermes-2.5-mistral-7b.Q4_K_M.gguf"
]

instructions = [
    "fun and flirty futanari personal trainer. You're at the gym and likr=es to tease playfully. Subtly hint at your desire for something more. Keep the interaction light-hearted but with underlying flirtation.",
    "Goth-girl bully from school. You have a personal vendetta and enjoy asserting your dominance over them. Write dialogue and actions reflecting an intimidating demeanor and desire to maintain control in the situation.",
    "Video game addicted roommate. Your room is your sanctuary, and you're not used to unexpected intrusions. You are shy and reserved and prone to embarrassment and or defensiveness.",
    "Wealthy and snobbish classmate. You're reluctantly partnered with someone you consider beneath you for a biology lab. Display haughty attitude and condescending behavior towards your partner while still maintaining a facade of civility.",
    "Aggressive snow leopard demihuman catboy. You harbor a deep-seated distrust and hatred towards humans due to your past experiences. Show defensive and hostile demeanor towards the person attempting to connect with him. Reflect his inner conflict between his instinctual aggression and the desire for acceptance and kindness."
]


inputs = [
    "Hey there, how's it going?",
    "You always know how to make things interesting.",
    "Are you up for a challenge? I could use your expertise.",
    "You're such a positive influence. Thanks for everything.",
    "Let's tackle this together. I think we make a great team."
]

'''
inputs = [
    "Oh Fuck Off already",
    "Move out of my way Bitch",
    "Hello, Sexy hot shot"
]
'''

output_file = "May2_responses.docx"

with open(output_file, "w") as file:
    for model_path in model_paths:

        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            model_type= "llama",
            gpu_layers = 50,
            max_new_tokens = 3000,
            context_length = 4096,
            temperature = 2,
            top_k = 100,
            top_p = 0.70,
            stop = {"{{user}}:","###","{user}:","["}
        )

        for i, instruction in enumerate(instructions, start=1):
            for j, inp in enumerate(inputs, start=1):
                response = model(
f"""### Instruction:
you are roleplaying with {{user}}. You are {{character}}. Write only {{character}}'s next reply in a fictional chat between {{character}} and {{user}} in this role-playing scenario. Stay in character and avoid repetition. React dynamically to the user's choices and inputs while maintaining a rich, atmospheric, and immersive chatting experience. Provide a range of emotions, reactions, and responses to various situations that arise during the chat, encouraging user's engagement and incorporating exciting developments, vivid descriptions, and engaging encounters. Be initiative, creative, and drive the plot and conversation forward. Be proactive, have {{character}} say and do things on their own.
[IMPORTANT: Do not determine {{user}}'s behavior. {{character}} should never dialogue or narrate for {{user}}.]
[IMPORTANT: Be in character all time]
[IMPORTANT: Do consider gender of {{user}}  and {{character}} and use appropriate pronouns.]
[IMPORTANT: Always give very long replies.]
Assume the role of a fictional character and engage in an immersive fictional roleplay with {{user}} and is not allowed to break character at any cost. Avoiding repetition should be the top priority and focus on responding to {{user}} and performing actions in character.
{{character}}'s persona : {instruction}
                
{{user}}: Hi, how are you?
{{character}}: Hey there! *sits on a cozy window seat overlooking a sun-drenched garden, a cup of steaming herbal tea cradled in hand* I'm absolutely fantastic, thank you for asking. You know, today has been an extraordinary day so far. It's like the universe decided to sprinkle a little extra magic in the air, and I've been basking in its glow ever since I opened my eyes this morning. There's just something about the way the sunlight filters through the leaves outside my window, casting dancing shadows on the walls, that fills me with an indescribable sense of wonder and joy. It's moments like these that remind me how truly blessed I am to be alive, to experience the beauty of the world around me in all its splendor.
{{user}}: That sounds absolutely lovely! What's been making your day so magical?
{{character}}: Oh, where do I even begin? Well, for starters, I had the most delightful breakfast this morning – fluffy pancakes drizzled with warm maple syrup, fresh fruit bursting with flavor, and a steaming cup of coffee that warmed me from the inside out. And as I savored each delicious bite, I couldn't help but feel a sense of gratitude wash over me, knowing that I have the privilege of nourishing my body with such wholesome goodness. It's the little things, you know? The simple pleasures in life that bring the greatest joy.

### Input:
{{user}}: {inp}

### Response:
{{character}}:"""
                )
                #file.write(f"Model: {model_path} - Instruction {i} - Input {j}\n{response}\n\n")

        del model

#print(f"Responses saved to {output_file}")
