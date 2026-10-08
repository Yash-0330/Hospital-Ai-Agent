import json
from config import RED_FLAGS_FILE
from utils.logger import logger

def check_red_flags(text: str) -> list:
    """Return list of emergency warning messages found in text."""
    if not text:
        return []

    try:
        with open(RED_FLAGS_FILE, "r", encoding="utf-8") as f:
            flags_data = json.load(f)
    except FileNotFoundError:
        logger.error(f"Missing file: {RED_FLAGS_FILE}")
        return []
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON in: {RED_FLAGS_FILE}")
        return []

    text_lower = text.lower()
    found = []
    for item in flags_data:
        if item["pattern"] in text_lower:
            found.append(item["message"])

    unique = list(set(found))
    if unique:
        logger.warning(f"Red flags detected: {unique}")
    return unique