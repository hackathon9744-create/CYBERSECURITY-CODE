from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ai_engine.fusion_engine import analyze_raw_input
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI(title="PhishGuard API")

from ai_engine.qr_engine import analyze_qr_bytes
from ai_engine.predictor import analyze_url_pipeline
from ai_engine.message_engine import analyze_message_pipeline

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

@app.post("/analyze_qr")
async def analyze_qr(file: UploadFile = File(...)):
    """
    Accepts an image file, decodes QR, then routes decoded content
    to your existing url/message pipelines and returns the same JSON shape.
    """
    # basic safety: ensure it's an image
    content_type = file.content_type or ""
    if not content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Upload an image file (png/jpg).")

    image_bytes = await file.read()
    decode_result = analyze_qr_bytes(image_bytes)

    if not decode_result.get("ok"):
        return JSONResponse(status_code=200, content={
            "final_risk": "Unknown",
            "scam_type": "no_qr",
            "explanation": [decode_result.get("error", "QR decode failed")],
            "decoded_data": None
        })

    decoded = decode_result["data"]

    # Decide routing: if starts with http -> URL pipeline; else treat as text
    if isinstance(decoded, str) and decoded.lower().startswith(("http://", "https://")):
        # call your existing URL analyzer (ensure it returns dict with final_risk, scam_type, explanation)
        try:
            result = analyze_url_pipeline(decoded)
            # attach decoded and source for transparency
            result["decoded_data"] = decoded
            result["qr_source"] = decode_result.get("source")
            return JSONResponse(status_code=200, content=result)
        except Exception as e:
            return JSONResponse(status_code=500, content={
                "final_risk": "Error",
                "scam_type": "internal_error",
                "explanation": [f"URL engine error: {str(e)}"],
                "decoded_data": decoded
            })
    else:
        # treat decoded data as text (UPI scheme, vpa, or plain text)
        try:
            result = analyze_message_pipeline(decoded)
            result["decoded_data"] = decoded
            result["qr_source"] = decode_result.get("source")
            return JSONResponse(status_code=200, content=result)
        except Exception as e:
            return JSONResponse(status_code=500, content={
                "final_risk": "Error",
                "scam_type": "internal_error",
                "explanation": [f"Message engine error: {str(e)}"],
                "decoded_data": decoded
            })

@app.get("/")
def home():
    return {"status": "Backend running successfully"}
