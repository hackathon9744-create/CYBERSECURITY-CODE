"""
enrich.py
- domain_age_days(domain)  (uses python-whois when available; fallback heuristics)
- ssl_check(host)  (simple https GET)
- fetch_redirect_chain(url)  (requests GET with redirects)
Note: Fetching remote URLs can expose your notebook's IP. Use only for labeled test data or local tests.
"""

import time
import requests
from datetime import datetime

# whois usage (may fail in Colab due to network)
try:
    import whois
    WHOIS_AVAILABLE = True
except Exception:
    WHOIS_AVAILABLE = False

def domain_age_days(domain: str):
    if not domain:
        return None
    if not WHOIS_AVAILABLE:
        return None
    try:
        w = whois.whois(domain)
        creation = w.creation_date
        if isinstance(creation, list):
            creation = creation[0]
        if creation is None:
            return None
        if isinstance(creation, str):
            creation = datetime.fromisoformat(creation)
        delta = datetime.now() - creation
        return int(delta.days)
    except Exception:
        return None

def domain_age_heuristic(domain: str):
    """Cheap heuristic when whois fails: suspicious TLDs and digits imply new/suspect."""
    suspicious_tlds = ['.xyz', '.top', '.loan', '.info', '.pw', '.site', '.online', '.rest', '.space', '.ru']
    if any(domain.endswith(t) for t in suspicious_tlds):
        return 7
    if any(ch.isdigit() for ch in domain):
        return 14
    return None

def ssl_check(host: str, timeout=3):
    if not host:
        return False
    try:
        r = requests.get("https://" + host, timeout=timeout)
        return r.status_code < 400
    except Exception:
        return False

def fetch_redirect_chain(url: str, timeout=5):
    try:
        r = requests.get(url, timeout=timeout, allow_redirects=True, headers={"User-Agent":"Mozilla/5.0 (Colab)"})
        chain = [resp.url for resp in r.history] + [r.url]
        hosts = [requests.utils.urlparse(u).hostname for u in chain]
        return {"chain": chain, "hosts": hosts, "final_url": r.url, "status_code": r.status_code}
    except Exception as e:
        return {"error": str(e), "chain": [], "hosts": [], "final_url": None}
