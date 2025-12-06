"""
features.py
- extract_features(url, fetch_page=False)
Uses url_utils, brand_sim, enrich, and optionally fetch page content.
"""

from ai_engine.url_utils import normalize_url, detect_homoglyphs
from ai_engine.brand_sim import brand_similarity
from ai_engine.enrich import domain_age_days, domain_age_heuristic, ssl_check, fetch_redirect_chain
import re

def has_suspicious_tokens(path_or_query: str):
    tokens = ["verify","login","secure","update","account","confirm","bank","payment","otp"]
    text = (path_or_query or "").lower()
    return any(t in text for t in tokens)

def extract_features(url: str, fetch_page: bool=False) -> dict:
    parsed = normalize_url(url)
    homog = detect_homoglyphs(parsed['host'])
    brand_sim = brand_similarity(parsed['host'])
    # whois
    age = domain_age_days(parsed['domain'])
    if age is None:
        age = domain_age_heuristic(parsed['domain'])
    # ssl
    ssl_ok = False
    redirect_info = None
    page_meta = {"title":"","password_inputs":0,"snippet":""}
    if fetch_page:
        # attempt redirect/ssl/page fetch (may expose notebook IP)
        redirect_info = fetch_redirect_chain(parsed['candidate'])
        final_host = None
        if redirect_info.get('final_url'):
            from urllib.parse import urlparse
            final_host = urlparse(redirect_info['final_url']).hostname
        ssl_ok = ssl_check(final_host or parsed['host'])
        # simple content fetch is left to enrich.fetch_redirect_chain + page fetch in production if safe
    else:
        ssl_ok = ssl_check(parsed['host'])  # cheap check
    features = {
        "url": parsed['original'],
        "host": parsed['host'],
        "domain": parsed['domain'],
        "subdomain": parsed['subdomain'],
        "path": parsed['path'],
        "query": parsed['query'],
        "length": len(parsed['original']),
        "hyphen_count": parsed['host'].count('-'),
        "digit_flag": int(bool(re.search(r'\d', parsed['host']))),
        "homoglyph_ratio": homog['non_ascii_ratio'],
        "homoglyph_flag": int(homog['block_flag']),
        "brand_best": brand_sim.get('best_brand'),
        "brand_sim": float(brand_sim.get('sim',0.0)),
        "whois_age_days": age,
        "ssl_valid": bool(ssl_ok),
        "suspicious_path_token": int(has_suspicious_tokens(parsed['path'] + " " + parsed['query'])),
        "redirect_info": redirect_info,
        "page": page_meta
    }
    return features
