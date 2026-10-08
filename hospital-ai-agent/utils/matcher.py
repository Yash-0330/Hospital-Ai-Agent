import json
from config import DEPARTMENTS_FILE, DOCTORS_FILE
from utils.logger import logger

def load_json(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"File not found: {filepath}")
        return []
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON: {filepath}")
        return []
    except Exception as e:
        logger.error(f"Error loading {filepath}: {e}")
        return []

def match_department(symptoms: str) -> str:
    """Score-based keyword matching to pick best department."""
    text = symptoms.lower()
    departments = load_json(DEPARTMENTS_FILE)

    best_match = "General Medicine"
    best_score = 0

    for dept in departments:
        score = sum(1 for kw in dept.get("keywords", []) if kw in text)
        if score > best_score:
            best_score = score
            best_match = dept["name"]

    logger.info(f"Matched department: {best_match} (score={best_score})")
    return best_match

def find_doctors(department: str) -> list:
    doctors = load_json(DOCTORS_FILE)
    return [d for d in doctors if d["department"] == department]