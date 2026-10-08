import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.triage import triage

def test_emergency_red_flag():
    r = triage("I have chest pain and cannot breathe", 5, 30)
    assert r["urgency"] == "EMERGENCY"
    assert r["department"] == "Emergency Department"

def test_high_severity():
    r = triage("stomach ache", 9, 30)
    assert r["urgency"] == "URGENT"

def test_routine_orthopedics():
    r = triage("knee pain for 3 weeks", 4, 30)
    assert r["department"] == "Orthopedics"
    assert r["urgency"] == "ROUTINE"

def test_age_safety():
    r = triage("mild fever", 3, 80)
    assert r["department"] == "General Medicine"
    assert r["urgency"] == "SEMI-URGENT"

def test_skin_department():
    r = triage("itching and rash on arms", 3, 25)
    assert r["department"] == "Dermatology"