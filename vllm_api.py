from vllm import LLM, SamplingParams
from pydantic import BaseModel
from typing import List
from fastapi import FastAPI

app = FastAPI()

class DataList(BaseModel):
    request_id: str
    prompt: str
    response: str = ""

class ModelRequest(BaseModel):
    batch_id: int
    data: List[DataList]

llm = LLM(
    model="TheBloke/Unholy-v2-13B-GPTQ", 
    quantization="Marlin", 
    gpu_memory_utilization=0.9, 
    kv_cache_dtype="fp8",
    swap_space=0,
    max_seq_len_to_capture=4000 
)

sampling_params = SamplingParams(
    temperature=0.8, 
    top_p=0.95, 
    max_tokens=512, 
    min_tokens=100, 
    stop=["{{user}}:"]
)

@app.post("/model")
async def model1(request: ModelRequest):
    model_input = [item.prompt for item in request.data]

    print(model_input)
    received_data = llm.generate(model_input, sampling_params)

    for i in range(len(model_input)):
        request.data[i].response =  received_data[i].outputs[0].text

    return request

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7001)
