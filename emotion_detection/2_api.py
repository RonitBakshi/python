from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
import uvicorn

emotion_classifier = pipeline('sentiment-analysis', model='j-hartmann/emotion-english-distilroberta-base')
app = FastAPI()
target_emotions = ['anger', 'sadness', 'surprise', 'joy', 'neutral']

class requestPayload(BaseModel):
    text: str


@app.post('/emotion_detection')
def getSimilarityScore(payload:requestPayload):
    
    result = emotion_classifier(payload.text)

    filtered_scores = [emotion for emotion in result[0] if emotion['label'] in target_emotions]
    print(f"filtered_scores: {filtered_scores}")
    max_emotion = max(filtered_scores, key=lambda x: x['score'])
    
    return max_emotion['label']


if __name__ == "__main__":
   uvicorn.run("2_api:app",port=8001,host="0.0.0.0",log_level="info")