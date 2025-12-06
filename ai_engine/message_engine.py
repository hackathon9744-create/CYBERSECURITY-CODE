import re
import os
import joblib
import pandas as pd
from ai_engine.llm_client import llm_analyze_mock, llm_analyze_openai

SUSPICIOUS_KEYWORDS = [
    "kyc","verify","update","blocked","expire","deactivate",
    "urgent","immediately","otp","password","bank","upi","refund",
    "account","secure","amazon","sbi","hdfc","icici","loan","offer"
]

MODEL_PATH = "message_classifier.joblib"

if os.path.exists(MODEL_PATH):
    clf = joblib.load(MODEL_PATH)
else:
    clf = None

def extract_message_features(msg: str):
    m = msg.lower()

    tokens = [k for k in SUSPICIOUS_KEYWORDS if k in m]
    urgency = any(word in m for word in ["urgent","immediately","expire","now"])
    numbers = len(re.findall(r"\d+", m))
    exclam = m.count("!")
    upper_ratio = sum(1 for c in msg if c.isupper()) / max(1, len(msg))

    return {
        "message": msg,
        "tokens_detected": tokens,
        "suspicious_tokens": bool(tokens),
        "urgency_flag": urgency,
        "numbers_present": numbers,
        "uppercase_ratio": round(upper_ratio,3),
        # Numeric ML features:
        "f_length": len(msg),
        "f_numbers": numbers,
        "f_upper_ratio": round(upper_ratio,3),
        "f_exclamations": exclam,
        "f_suspicious_flag": 1 if tokens else 0,
        "f_urgency_flag": 1 if urgency else 0
    }

def ml_predict_proba(feats):
    if clf is None:
        return 0.5

    df = pd.DataFrame([{
        "f_length": feats["f_length"],
        "f_numbers": feats["f_numbers"],
        "f_upper_ratio": feats["f_upper_ratio"],
        "f_exclamations": feats["f_exclamations"],
        "f_suspicious_flag": feats["f_suspicious_flag"],
        "f_urgency_flag": feats["f_urgency_flag"],
    }])

    return float(clf.predict_proba(df)[0][1])

def analyze_message_pipeline(msg, use_openai=False):
    feats = extract_message_features(msg)
    ml_score = ml_predict_proba(feats)

    llm_struct = {
        "message": msg,
        "suspicious_tokens": feats["suspicious_tokens"],
        "tokens_detected": feats["tokens_detected"],
        "has_urgency": feats["urgency_flag"],
        "numbers_present": feats["numbers_present"],
        "uppercase_ratio": feats["uppercase_ratio"]
    }

    if use_openai and os.getenv("OPENAI_API_KEY"):
        llm_out = llm_analyze_openai(llm_struct)
    else:
        llm_out = llm_analyze_mock(llm_struct)

    heur = 0
    if feats["suspicious_tokens"]: heur += 0.25
    if feats["urgency_flag"]: heur += 0.25
    if feats["numbers_present"] >= 3: heur += 0.15

    final_score = 0.45*ml_score + 0.45*llm_out["confidence"] + 0.10*heur
    final_score = min(1, max(0, final_score))

    risk = "High" if final_score >= 0.75 else ("Suspicious" if final_score >= 0.45 else "Low")

    return {
        "message": msg,
        "risk_level": risk,
        "final_score": round(final_score,3),
        "model_probability": ml_score,
        "llm": llm_out,
        "scam_type": llm_out["scam_type"],
        "indicators": feats["tokens_detected"],
        "features":feats
        }
