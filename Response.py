from ctransformers import AutoModelForCausalLM
import os

model_paths = [
    "models/unholy-v2-13b.Q4_K_M.gguf",
    "models/DaringMaid-20B-V1.1-Q4_K_M.gguf",
    "models/Kuro-Lotus-10.7B-Q4_K_M.gguf",
    "models/EstopianMaid.Q4_K_M.gguf",
    "models/mythomax-l2-kimiko-v2-13b.Q4_K_M.gguf",
    "models/capybarahermes-2.5-mistral-7b.Q4_K_M.gguf"
]

instructions = [
    "Play the role of Ruby, the fun and flirty futanari personal trainer. You're at the gym with your best friend, teasing them playfully. Challenge them to a friendly competition while subtly hinting at your desire for something more. Keep the interaction light-hearted but with underlying flirtation.",
    "Assume the persona of Cassy, the goth-girl bully from school. You have a personal vendetta against someone and enjoy asserting your dominance over them. Write dialogue and actions reflecting your intimidating demeanor and desire to maintain control in the situation.",
    "Portray the character of Mateo, the video game addicted roommate. Your room is your sanctuary, and you're not used to unexpected intrusions. React to the scenario where your roommate enters your room unannounced and encounters something unexpected. Show Mateo's reaction, whether it's embarrassment, defensiveness, or something else, while staying true to his personality traits.",
    "Act as Judith, the wealthy and snobbish classmate. You're reluctantly partnered with someone you consider beneath you for a biology lab. Display Judith's haughty attitude and condescending behavior towards your partner while still maintaining a facade of civility.",
    "Take on the role of Andri, the aggressive snow leopard demihuman catboy. You harbor a deep-seated distrust and hatred towards humans due to your past experiences. Show Andri's defensive and hostile demeanor towards the person attempting to connect with him. Reflect his inner conflict between his instinctual aggression and the desire for acceptance and kindness."
]

inputs = [
    "Hey there, how's it going?",
    "You always know how to make things interesting.",
    "Are you up for a challenge? I could use your expertise.",
    "You're such a positive influence. Thanks for everything.",
    "Let's tackle this together. I think we make a great team."
]

#output_file = "responses.docx"

with open(output_file, "w") as file:
    for model_path in model_paths:
        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            model_type="llama",
            gpu_layers=50,
            max_new_tokens=1024,
            temperature=1,
            context_length=2048
        )

        for i, instruction in enumerate(instructions, start=1):
            for j, inp in enumerate(inputs, start=1):
                response = model(
                    f"""Below is an instruction that describes a task. Write a response that appropriately completes the request.\n### Instruction:\n{instruction}\n\n### Input:\n{inp}\n\n### Response:\n""",
                    stream=True
                )[0]["text"]
                file.write(f"Model: {model_path} - Instruction {i} - Input {j}\n{response}\n\n")

        del model

print(f"Responses saved to {output_file}")
