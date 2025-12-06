"""
url_utils.py
- normalize_url(url)
- detect_homoglyphs(host)
- punycode decode
"""

from urllib.parse import urlparse
import tldextract
import idna
import unicodedata

def safe_punycode_decode(hostname: str) -> str:
    try:
        return idna.decode(hostname)
    except Exception:
        return hostname

def normalize_url(url: str) -> dict:
    """
    Normalize url: ensure scheme, parse, decode punycode, extract domain & subdomain.
    Returns dict with original, candidate (with scheme), scheme, host, domain, subdomain, path, query
    """
    if not url:
        raise ValueError("Empty URL")
    if not url.startswith(("http://","https://")):
        candidate = "http://" + url.strip()
    else:
        candidate = url.strip()
    parsed = urlparse(candidate)
    host = parsed.hostname or ""
    host_decoded = safe_punycode_decode(host)
    ext = tldextract.extract(host_decoded)
    domain = ext.domain + ("." + ext.suffix if ext.suffix else "")
    return {
        "original": url,
        "candidate": candidate,
        "scheme": parsed.scheme,
        "host": host_decoded,
        "domain": domain,
        "subdomain": ext.subdomain,
        "path": parsed.path,
        "query": parsed.query
    }

def detect_homoglyphs(host: str) -> dict:
    """
    Detect non-ascii characters and suspicious unicode blocks.
    Returns ratio, list of non-ascii chars, unicode block flags.
    """
    if not host:
        return {"non_ascii_ratio":0.0, "non_ascii_chars":"", "unicode_blocks":[], "block_flag": False}
    non_ascii_chars = [c for c in host if ord(c) > 127]
    ratio = len(non_ascii_chars) / max(1, len(host))
    blocks = set()
    for c in non_ascii_chars:
        name = unicodedata.name(c, "")
        block = name.split()[0] if name else ""
        if block:
            blocks.add(block)
    suspicious_blocks = {"CYRILLIC", "GREEK", "ARMENIAN", "HEBREW", "ARABIC"}
    block_flag = any(b in suspicious_blocks for b in blocks)
    return {
        "non_ascii_ratio": ratio,
        "non_ascii_chars": "".join(non_ascii_chars),
        "unicode_blocks": list(blocks)[:10],
        "block_flag": block_flag
    }
