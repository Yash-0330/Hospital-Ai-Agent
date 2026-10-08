# 🏥 Hospital AI Agent

A navigation assistant that helps patients find the right hospital department or doctor based on symptoms and urgency.

> ⚠️ This is NOT a medical diagnosis. For emergencies, call **112 / 108 (India)** or your local emergency number.

## ✨ Features
- Symptom intake with severity and age
- Emergency red-flag detection
- Rule-based triage (Emergency / Urgent / Semi-Urgent / Routine)
- Department + doctor recommendation
- Doctor directory with filter and booking
- Optional Gemini AI symptom summarizer
- Audit logging for every triage decision
- Custom professional medical UI

## 🏗️ Tech Stack
| Layer | Tool |
|---|---|
| UI | Streamlit |
| Language | Python 3.11+ |
| Data | JSON |
| LLM (optional) | Google Gemini |
| Testing | Pytest |

## 🚀 Setup

```bash
git clone <your-repo-url>
cd hospital-ai-agent
python -m venv venv
venv\Scripts\activate           # Windows
source venv/bin/activate        # Mac/Linux
pip install -r requirements.txt
streamlit run app.py
