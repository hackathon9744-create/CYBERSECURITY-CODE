🌐 PhishGuard: AI-Powered Fraud Message Detection System
Built for PKP Mumbai Hackathon 2025
<p align="center"> <img src="banner.png" alt="PhishGuard Banner" width="800"> </p>

PhishGuard is a real-time system that detects fraudulent SMS/messages using Machine Learning + Rule-Based Heuristics + Natural Language Features.
Built by Team Hexa for PKP Mumbai Hackathon 2025.

🚀 Features
🔍 1. Fraud Message Scanner (Frontend UI)

Paste any suspicious message

Detect if it's FAKE or REAL

Shows:

Verdict

Score

Reasons for classification

Indicators (URLs, warnings, brand mismatch, etc.)

🧠 2. Hybrid Detection System (Backend)

ML Model (Trained in Google Colab using joblib)

Heuristic Rules (URL detection, entropy, uppercase ratio, fake links…)

Combined score → final decision

📊 3. Reporting System

Save user reports

Store messages with metadata in a local SQLite database

/reports endpoint shows all previous reports

🌐 4. REST API

FastAPI backend

Fully documented using Swagger UI

🏗️ Tech Stack
Layer	Technologies
Frontend	HTML, CSS, JavaScript, Tailwind, Live Server
Backend	Python, FastAPI, Uvicorn
ML Model	scikit-learn, numpy, pandas, joblib
Heuristics	Custom rules (URL detection, entropy, etc.)
Database	SQLite
Deployment	Local server / future cloud-ready
📦 Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/<your-username>/phishguard.git
cd phishguard

2️⃣ Setup Backend
Create venv:
cd backend
python -m venv venv

Activate venv:
Windows:
venv\Scripts\activate

Mac/Linux:
source venv/bin/activate

Install requirements:
pip install -r requirements.txt

3️⃣ Place ML Model

Download model.joblib from Google Colab and place it inside:

backend/models/model.joblib

4️⃣ Run the Backend
python -m uvicorn app:app --reload --port 8000


Backend will be available at:
📌 http://localhost:8000

Swagger Docs:
📌 http://localhost:8000/docs

5️⃣ Start Frontend

Open a new terminal:

cd frontend
python -m http.server 5500


Open in browser:

📌 http://localhost:5500/frontend.html

🧪 API Documentation
POST /scan

Detect if a message is fake or real.

Request
{
  "text": "Your account is suspended. Verify at http://fake-login.com",
  "reporter_name": "bhumit"
}

Response
{
  "verdict": "fake",
  "score": 0.89,
  "reasons": [
    "Suspicious words detected",
    "Link resembles fake domain"
  ],
  "indicators": {
    "has_url": true,
    "suspicious_phrase_count": 2,
    "entropy": 4.5
  }
}

POST /report

Save user report to database.

GET /reports

Fetch last 100 reports.

🧩 Project Architecture
             ┌────────────────┐
             │   Frontend      │
             │  (HTML / JS)    │
             └───────┬────────┘
                     │ fetch()
                     ▼
             ┌────────────────┐
             │   FastAPI      │
             │   Backend      │
             └───────┬────────┘
   ┌─────────────────┼──────────────────┐
   ▼                 ▼                  ▼
ML Model        Rule Engine        SQLite DB
(model.joblib)  (heuristics)      (reports.db)

📷 Screenshots

Replace with your screenshots

/screenshots
  ├── frontend_scan.png
  ├── fake_message_result.png
  ├── safe_message_result.png
  ├── swagger_docs.png

👨‍💻 Team HEXA — Developers
Name	Role
Bhumit Gupta	Backend Developer
Ved	ML Engineer
Dhoni	ML Engineer
Aishwarya	UI/UX Designer
+ Others (If any)	
🏆 Built for PKP Mumbai Hackathon 2025

This project was developed in under 24 hours for PKP Mumbai Hack 2025, focusing on Cybersecurity, AI, and Public Safety.

⭐ Future Enhancements

Host backend on cloud (Render, Railway, AWS)

Train advanced transformer-based models

Create a Chrome extension

Add QR-fraud detection

Mobile app version (React Native)

📜 License

This project is licensed under the MIT License.

🎉 Thank You!

If you like this project, don’t forget to ⭐ the repo.
