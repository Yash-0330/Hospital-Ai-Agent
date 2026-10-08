import os
from dotenv import load_dotenv
from utils.logger import logger

load_dotenv()

_api_key = os.getenv("GEMINI_API_KEY", "").strip()
_model = None

if _api_key:
    try:
        import google.generativeai as genai
        genai.configure(api_key=_api_key)
        _model = genai.GenerativeModel("gemini-1.5-flash")
        logger.info("Gemini LLM initialized")
    except Exception as e:
        logger.error(f"Gemini init failed: {e}")
else:
    logger.info("No GEMINI_API_KEY — LLM features disabled")

def extract_symptoms_with_llm(text: str) -> str:
    """Optional symptom summarizer. Falls back to raw text."""
    if not _model or not text:
        return text

    prompt = f"""
You are a hospital intake assistant.
Summarize the patient's main symptoms, duration, and severity in 1-2 lines.
Do NOT diagnose. Do NOT give medical advice.

Patient message: {text}
"""
    try:
        response = _model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        logger.error(f"LLM error: {e}")
        return text