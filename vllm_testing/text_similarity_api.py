from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer, util
import uvicorn

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
app = FastAPI()


class requestPayload(BaseModel):
    string1: str
    string2: str


@app.post('/similarity_score')
def getSimilarityScore(payload:requestPayload):
    embedding_1= model.encode(payload.string1, convert_to_tensor=True)
    embedding_2 = model.encode(payload.string2, convert_to_tensor=True)
    similarity_score = float(util.pytorch_cos_sim(embedding_1, embedding_2))

    return { "similarityScore": similarity_score}


if __name__ == "__main__":
    uvicorn.run("text_similarity_api:app",host="0.0.0.0",port=8001,log_level="info")