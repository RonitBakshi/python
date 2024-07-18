from openai import OpenAI

client = OpenAI(
    base_url="http://122.176.159.126:8000/v1",
    api_key="token-abc123",
)

prompt = ""

n = 15000

while True:
    prompt = ""

    for _ in range(n):
        prompt += "-"

    try:
        completion = client.chat.completions.create(
        model="TheBloke/Amethyst-13B-Mistral-GPTQ",
        messages = [ 
                {
                    "role": "system",
                    "content": prompt,
                },
            ],
            #stop: requestData.stop,
            stream = True,
            top_p = 0.9,
            temperature = 0.8,
            frequency_penalty = 0.5,
            presence_penalty = 0.5,
            max_tokens = 250,
            seed = -1,
        )

        n += 1

    except Exception as e:
        print(f"Exception : {e} | Total characters {n}")
        break  