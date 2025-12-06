import re
from ai_engine.message_engine import analyze_message_pipeline
from ai_engine.predictor import analyze_url_pipeline

def extract_url_from_text(text):
    url_pattern = r'(https?://\S+)'
    matches = re.findall(url_pattern, text)
    if matches:
        return matches[0]
    else:
        return None

def clean_message(text):
    url = extract_url_from_text(text)
    if url:
        return text.replace(url, "").strip()
    return text

def fuse_results(message_result=None, url_result=None):
    """
    Combines message + URL analysis into a final unified risk score.
    Works even if only one of them is provided.
    """

    # Case 1: Only message exists
    if message_result and not url_result:
        return {
            "final_risk": message_result["risk_level"],
            "final_score": message_result["final_score"],
            "source": "message_only",
            "message_analysis": message_result,
            "url_analysis": None,
            "scam_type": message_result["scam_type"],
            "explanation": message_result["llm"]["reasons"]
        }

    # Case 2: Only URL exists
    if url_result and not message_result:
        return {
            "final_risk": url_result["risk_level"],
            "final_score": url_result["final_score"],
            "source": "url_only",
            "message_analysis": None,
            "url_analysis": url_result,
            "scam_type": url_result["llm"]["scam_type"],
            "explanation": url_result["llm"]["reasons"] + url_result["structural_reasons"]
        }

    # Case 3: BOTH message + URL exist
    # Weighted fusion
    m_score = message_result["final_score"]
    u_score = url_result["final_score"]

    # weights: URL is usually more important than message
    final_score = round((0.55 * u_score) + (0.45 * m_score), 3)

    # risk classification
    if final_score >= 0.75:
        final_risk = "High"
    elif final_score >= 0.50:
        final_risk = "Suspicious"
    else:
        final_risk = "Low"

    # Choose scam type:
    # URL has priority; if message agrees, unify them
    if url_result["llm"]["scam_type"] != "unknown":
        scam_type = url_result["llm"]["scam_type"]
    else:
        scam_type = message_result["scam_type"]

    # Merge explanations
    explanation = []
    explanation.extend(message_result["llm"]["reasons"])
    explanation.extend(url_result["llm"]["reasons"])
    explanation.extend(url_result["structural_reasons"])

    return {
        "final_risk": final_risk,
        "final_score": final_score,
        "message_analysis": message_result,
        "url_analysis": url_result,
        "scam_type": scam_type,
        "source": "message+url",
        "explanation": explanation
    }


def analyze_combined(message=None, url=None, use_openai=False):
    """
    High-level wrapper: give message and URL, get final fused output.
    """
    msg_res = analyze_message_pipeline(message, use_openai=use_openai) if message else None
    url_res = analyze_url_pipeline(url, use_openai=use_openai) if url else None

    return fuse_results(msg_res,url_res)

def analyze_raw_input(raw_text, use_openai=True):
    url = extract_url_from_text(raw_text)
    msg = clean_message(raw_text)

    return analyze_combined(
        message=msg,
        url=url,
        use_openai=use_openai
    )
