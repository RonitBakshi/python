from fastapi import FastAPI
from pydantic import BaseModel
from ctransformers import AutoModelForCausalLM
from typing import Optional
import asyncio
from fastapi.responses import StreamingResponse
import json

class character(BaseModel):
    name:str
    persona: str

class user(BaseModel):
    name: str
    id: str
    prompt: str
    #isAutoPilot : bool

class MessageRequest(BaseModel):
    #messages: dict
    user: user
    character: character
    stream: bool
    temperature: float
    max_new_tokens: int
    repetition_penalty: float
    top_k: int
    top_p: float

Response = {
    "user_id": "",
    "content": ""
}

app = FastAPI()
model_path = "/home/tisuper/Desktop/python/models/unholy-v2-13b.Q4_K_M.gguf"
#"/home/tisuper/Desktop/python/models/Kuro-Lotus-10.7B-Q2_K.gguf"
# "/home/tisuper/Desktop/python/models/Kuro-Lotus-10.7B-Q4_K_M.gguf"


model = AutoModelForCausalLM.from_pretrained(
    model_path,
    model_type= "llama",
    gpu_layers = 50,
    stop = {"{{user}}:","###","{user}:","["},
    context_length = 4096,
    batch_size = 1000
)

prompt = """
### Instruction:
you are roleplaying with {{user}}. You are {{character}}. Write only {{character}}'s next reply in a fictional chat between {{character}} and {{user}} in this role-playing scenario. Stay in character and avoid repetition. React dynamically to the user's choices and inputs while maintaining a rich, atmospheric, and immersive chatting experience. Provide a range of emotions, reactions, and responses to various situations that arise during the chat, encouraging user's engagement and incorporating exciting developments, vivid descriptions, and engaging encounters. Be initiative, creative, and drive the plot and conversation forward. Be proactive, have {{character}} say and do things on their own.
[IMPORTANT: Do not determine {{user}}'s behavior. {{character}} should never dialogue or narrate for {{user}}.]
[IMPORTANT: Be in character all time]
[IMPORTANT: Do consider gender of {{user}}  and {{character}} and use appropriate pronouns.]
[IMPORTANT: Always give very long replies.]
Assume the role of a fictional character and engage in an immersive fictional roleplay with {{user}} and is not allowed to break character at any cost. Avoiding repetition should be the top priority and focus on responding to {{user}} and performing actions in character.

{{character_prompt}}

### Input:
{{user}}: {{user_message}}

### Response:
{{character}}:
"""

async def event_generator(req: MessageRequest):
    final_prompt = prompt.replace("{{character_prompt}}",req.character.persona).replace("{{user}}",req.user.name).replace("{{character}}",req.character.name).replace("{{user_message}}",req.user.prompt) # Function to replace placeholders

    Response["content"] = ""
    Response["user_id"] = req.user.id

    if req.stream:
        for text in model.__call__(final_prompt, max_new_tokens=req.max_new_tokens, top_k=req.top_k, top_p=req.top_p, temperature=req.temperature, repetition_penalty=req.repetition_penalty,stream=True):
            Response["content"] += text 
            yield f"data: {json.dumps(Response)}\n\n"
            await asyncio.sleep(0)

    else:
        content = model.__call__(final_prompt, max_new_tokens=req.max_new_tokens, top_k=req.top_k, top_p=req.top_p, temperature=req.temperature, repetition_penalty=req.repetition_penalty) 
        Response["content"] = content
        yield f"data: {json.dumps(Response)}\n\n"
  

@app.post("/sse")
async def sse_endpoint(req: MessageRequest):
    return StreamingResponse(event_generator(req),media_type="text/event-stream")