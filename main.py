from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ai_engine.fusion_engine import analyze_raw_input
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="PhishGuard API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    text: str
    use_openai: bool = True

@app.post("/analyze")
def analyze(req: AnalyzeRequest):
    try:
        result = analyze_raw_input(req.text, use_openai=req.use_openai)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def home():
    return {"status": "Backend running successfully"}

import requests

@app.get("/latest_cyber_attacks")
def latest_attacks():
    try:
        FEED_URL = "https://thehackernews.com/feeds/posts/default?alt=rss"
        r = requests.get(FEED_URL, timeout=5)

        if r.status_code != 200:
            return {"attacks": []}

        attacks = []
        items = r.text.split("<item>")[1:6]

        for item in items:
            start = item.find("<title>") + 7
            end = item.find("</title>")
            title = item[start:end].strip()
            attacks.append(title)

        return {"attacks": attacks}

    except Exception as e:
        return {"attacks": []}
