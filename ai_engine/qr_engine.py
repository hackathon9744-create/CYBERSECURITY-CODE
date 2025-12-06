# ai_engine/qr_engine.py
import io
import requests

from PIL import Image

# Optional import; used if zbar is available
try:
    from pyzbar.pyzbar import decode as zbar_decode
    _HAS_PYZBAR = True
except Exception:
    _HAS_PYZBAR = False

QR_API_FALLBACK = "https://api.qrserver.com/v1/read-qr-code/"

def decode_qr_with_pyzbar(image_bytes):
    """
    Try local decode using pyzbar + Pillow.
    Returns decoded string or None.
    """
    if not _HAS_PYZBAR:
        return None
    try:
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        decoded = zbar_decode(img)
        if not decoded:
            return None
        # use first result
        return decoded[0].data.decode("utf-8", errors="ignore")
    except Exception:
        return None

def decode_qr_with_api(image_bytes):
    """
    Fallback: send the image to api.qrserver.com to decode.
    Returns decoded string or None.
    """
    try:
        files = {"file": ("qr.png", image_bytes, "image/png")}
        r = requests.post(QR_API_FALLBACK, files=files, timeout=15)
        r.raise_for_status()
        resp = r.json()
        # API returns list; look for first non-empty data
        if isinstance(resp, list) and len(resp) > 0:
            # resp[0] -> {'type':..., 'symbol': [{'data': '...', 'error': None}]}
            symbols = resp[0].get("symbol", [])
            if symbols and isinstance(symbols, list):
                d = symbols[0].get("data")
                if d:
                    return d
        return None
    except Exception:
        return None

def analyze_qr_bytes(image_bytes):
    """
    Return dict: { "ok": True|False, "data": <decoded str> or "error": msg }
    """
    # Try local
    decoded = decode_qr_with_pyzbar(image_bytes)
    if decoded:
        return {"ok": True, "data": decoded, "source": "local"}
    # Fallback to API
    decoded = decode_qr_with_api(image_bytes)
    if decoded:
        return {"ok": True, "data": decoded, "source": "qrserver"}
    return {"ok": False, "error": "No QR code found / decoding failed"}
