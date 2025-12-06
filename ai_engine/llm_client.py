import os
import json
import openai

def openai_client():
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OpenAI API key missing. Set with os.environ['OPENAI_API_KEY']='...'")
    openai.api_key = key
    return openai

BASE_PROMPT = """
You are an AI cybersecurity analyst specializing in scam message detection.
You will be given structured metadata from an SMS/WhatsApp message.

Your task:
1. Assess risk level: Low, Suspicious, or High.
2. Predict scam type (credential_harvesting, fake_kyc, otp_scam, payment_scam, refund_scam, unknown).
3. Provide a short list of reasons.
4. Output STRICT JSON only:
{
 "risk_level": "...",
 "confidence": float,
 "scam_type": "...",
 "reasons": ["...", "..."]
}
"""

def llm_analyze_mock(struct):
    score = 0
    reasons = []

    if struct.get("suspicious_tokens"):
        score += 0.45
        reasons.append("Suspicious scam-related words detected.")

    if struct.get("has_urgency"):
        score += 0.30
        reasons.append("Urgency language present.")

    if struct.get("numbers_present", 0) > 2:
        score += 0.15
        reasons.append("High number usage (OTP/ref IDs).")

    risk = "High" if score >= 0.7 else ("Suspicious" if score >= 0.4 else "Low")
    scam = "credential_harvesting" if struct.get("suspicious_tokens") else "unknown"

    return {
        "risk_level": risk,
        "confidence": round(min(score,1),3),
        "scam_type": scam,
        "reasons": reasons or ["No strong indicators."]
    }

def llm_analyze_openai(struct):
    client = openai_client()

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"system","content":BASE_PROMPT},
            {"role":"user","content":json.dumps(struct)}
        ],
        temperature=0.0,
        max_tokens=300
    )

    raw = resp.choices[0].message.content

    # Try JSON
    try:
        return json.loads(raw)
    except:
        import re
        match = re.search(r"\{[\s\S]*\}", raw)
        if match:
            try:
                return json.loads(match.group())
            except:
                pass
        return llm_analyze_mock(struct)
