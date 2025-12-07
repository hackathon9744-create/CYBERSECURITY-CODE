🔐 CyberSec Intelligence

AI-Powered Scam & Phishing Detection System

Made for PKP Hackathon 2025

CyberSec Intelligence is a project we built to help people detect fake links, scam messages, and impersonation attempts using a mix of Machine Learning, LLM reasoning, and rule-based analysis.
Our goal was to create something that actually works in real-world Indian scenarios (KYC scams, refund scams, phishing SMS, etc.)

We also added a section that shows recent cyber attacks dynamically so users stay up to date.


---

🌟 What the System Can Do

🔍 URL Fraud Check

The system can inspect a URL and tell whether it's safe or suspicious.
We trained a Random Forest model (11k+ phishing URLs) and added extra logic for:

Fake TLDs

Homoglyph tricks

Brand impersonation

Redirect-based attacks

Suspicious keywords like verify, update, bank, etc.


✉️ Scam Message Detection

Just paste any SMS or WhatsApp message.
The model detects:

KYC scams

Fake refund messages

OTP scams

Urgency/scare tactics

Hidden URLs inside text

AI-generated scam content


🤖 LLM Reasoning

Instead of depending only on ML, we use an LLM to analyze:

The tone of the message

Scam writing patterns

Intent (refund, impersonation, urgency, etc.)

Clues that normal ML classifiers usually miss


🧠 Fusion Engine

We combine outputs from:

ML model

LLM reasoning

Custom heuristics

URL feature analysis


After merging all signals, we give a final “risk level” and explanation.

🌐 Live Cyber Attack Feed

We fetch latest cyberattack alerts directly from CERT-IN RSS feed.
This keeps the dashboard fresh and relevant.


---

🧱 Architecture Overview

Frontend (GitHub Pages)
        │
        ▼
FastAPI Backend (Render)
        │
        ├── URL ML Model (Random Forest)
        ├── Message Analyzer (Rules + LLM)
        ├── Fusion Engine
        └── CERT-IN RSS Attack Feed
        │
        ▼
JSON Output → Shown in Dashboard


---

🚀 Demo Links

Frontend (GitHub Pages):
<https://hackathon9744-create.github.io/CYBERSECURITY-CODE/>

---

🛠 Tools We Used

Frontend

HTML, CSS (Tailwind)

Vanilla JavaScript

GitHub Pages for hosting


Backend

Python FastAPI

Render for deployment

Joblib + scikit-learn

Requests

OpenAI API (optional, fallback included)


ML/AI

Random Forest URL classifier

Message heuristics

LLM-based text reasoning

Hybrid risk scoring



---

⚙️ How to Run Locally

1. Clone repo

git clone <repo-url>
cd CYBERSECURITY-CODE

2. Install backend packages

pip install -r requirements.txt

3. Start backend

uvicorn main:app --reload

4. Open frontend

Just open index.html in a browser.


---

🔌 Backend API

POST /analyze

Send either a URL or a message.

Example:

{
  "text": "Your KYC is pending. Verify at https://upi-verify-update.top",
  "use_openai": true
}

Response example:

{
  "final_risk": "High",
  "final_score": 0.89,
  "scam_type": "kyc_verification",
  "explanation": [
    "Suspicious URL detected",
    "Urgency tactics",
    "Brand impersonation pattern"
  ]
}


---

🌐 GET /latest_cyber_attacks

Returns 4–5 latest cyber alerts from CERT-IN.

{
  "attacks": [
    "New phishing campaign targeting SBI users",
    "Critical security vulnerability patched",
    "Ransomware group activity spike"
  ]
}


---

👥 Team

Dhoni – ML + LLM + Fusion Engine

Ved – Message classification system

Aishwarya – Frontend UI

Bhumit – Frontend ↔ Backend integration

ML Model (Trained in Google Colab using joblib)

Heuristic Rules (URL detection, entropy, uppercase ratio, fake links…)

Combined score → final decision


🏆 Built for PKP Mumbai Hackathon 2025

This project was developed in under 24 hours for PKP Mumbai Hack 2025, focusing on Cybersecurity, AI, and Public Safety.

⭐ Future Enhancements

Host backend on cloud (Render, Railway, AWS)

Train advanced transformer-based models

Create a Chrome extensions.


📜 License

This project is licensed under the MIT License.

🎉 Thank You!

If you like this project, don’t forget to ⭐ the repo.
