import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

DEPARTMENTS_FILE = os.path.join(DATA_DIR, "departments.json")
DOCTORS_FILE = os.path.join(DATA_DIR, "doctors.json")
RED_FLAGS_FILE = os.path.join(DATA_DIR, "red_flags.json")

APP_TITLE = "Hospital AI Agent"
APP_CAPTION = "Smart navigation to the right department or doctor"
EMERGENCY_NUMBER = "112 / 108 (India)"
DISCLAIMER = (
    "⚠️ This is NOT a medical diagnosis. "
    f"For emergencies, call {EMERGENCY_NUMBER} immediately."
)

URGENCY_EMERGENCY = "EMERGENCY"
URGENCY_URGENT = "URGENT"
URGENCY_SEMI_URGENT = "SEMI-URGENT"
URGENCY_ROUTINE = "ROUTINE"