from utils.red_flag import check_red_flags
from utils.matcher import match_department, find_doctors
from config import (
    URGENCY_EMERGENCY, URGENCY_URGENT,
    URGENCY_SEMI_URGENT, URGENCY_ROUTINE,
    EMERGENCY_NUMBER,
)
from utils.logger import logger

def triage(symptoms: str, severity: int, age: int) -> dict:
    """Core triage logic. Returns decision dictionary."""

    # 1. Emergency red flags (highest priority)
    flags = check_red_flags(symptoms)
    if flags:
        logger.warning("EMERGENCY triage triggered")
        return {
            "urgency": URGENCY_EMERGENCY,
            "red_flags": flags,
            "department": "Emergency Department",
            "doctors": [],
            "message": (
                f"Call {EMERGENCY_NUMBER} immediately or go to the nearest "
                "Emergency Room. Do not wait."
            ),
        }

    # 2. Very high severity
    if severity >= 8:
        logger.info("URGENT triage triggered (severity)")
        return {
            "urgency": URGENCY_URGENT,
            "red_flags": [],
            "department": "Emergency Department",
            "doctors": [],
            "message": (
                "Your severity score is high. Please go to urgent care or "
                "the emergency department now."
            ),
        }

    # 3. Age safety
    if age <= 2 or age >= 75:
        dept = "General Medicine"
        logger.info("Age safety rule applied")
        return {
            "urgency": URGENCY_SEMI_URGENT,
            "red_flags": [],
            "department": dept,
            "doctors": find_doctors(dept),
            "message": (
                "Given your age group, please consult a general physician "
                "first. They will refer you if needed."
            ),
        }

    # 4. Normal routing
    dept = match_department(symptoms)
    urgency = URGENCY_SEMI_URGENT if severity >= 5 else URGENCY_ROUTINE

    logger.info(f"Routine triage: {dept} ({urgency})")
    return {
        "urgency": urgency,
        "red_flags": [],
        "department": dept,
        "doctors": find_doctors(dept),
        "message": f"Please book an appointment with {dept}.",
    }