import streamlit as st
from config import APP_TITLE, APP_CAPTION, DISCLAIMER, EMERGENCY_NUMBER, DOCTORS_FILE
from utils.triage import triage
from utils.llm_helper import extract_symptoms_with_llm
from utils.matcher import load_json
from utils.logger import logger

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Hospital AI Agent",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Load CSS
try:
    with open("assets/style.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    logger.warning("style.css not found")

# ---------------- HERO ----------------
st.markdown(f"""
<div class="hero-header">
    <h1>🏥 {APP_TITLE}</h1>
    <p>{APP_CAPTION}</p>
</div>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("⚙️ Settings")
    use_llm = st.checkbox("Enable AI Symptom Summary (Gemini)", value=False)
    st.divider()
    st.header("🚨 Emergency")
    st.error(f"Life-threatening? Call **{EMERGENCY_NUMBER}** immediately.")
    st.divider()
    st.caption("Professional Edition · v1.0")

# ---------------- TABS ----------------
tab1, tab2, tab3 = st.tabs(["🩺 Patient Intake", "👨‍⚕️ Doctors Directory", "ℹ️ About"])

# ============================================================
# TAB 1 — PATIENT INTAKE
# ============================================================
with tab1:
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("📝 Symptom Assessment")
        with st.form("triage_form"):
            symptoms = st.text_area(
                "Describe your symptoms",
                placeholder="e.g., sharp knee pain for 3 weeks, mild swelling...",
                height=130,
            )
            c1, c2 = st.columns(2)
            with c1:
                severity = st.slider("Severity (1 = mild, 10 = severe)", 1, 10, 5)
            with c2:
                age = st.number_input("Age", 0, 120, 30)

            submitted = st.form_submit_button("🔍 Find Appropriate Department")

    with col2:
        st.subheader("💡 Quick Tips")
        st.info("Be specific about symptoms, duration, and pain level.")
        st.warning("This tool does NOT replace a doctor's judgment.")
        st.success(f"Emergency? Call {EMERGENCY_NUMBER}")

    if submitted:
        if not symptoms.strip():
            st.error("Please describe your symptoms first.")
        else:
            final_symptoms = symptoms
            if use_llm:
                with st.spinner("AI analyzing symptoms..."):
                    final_symptoms = extract_symptoms_with_llm(symptoms)
                st.info(f"**AI Summary:** {final_symptoms}")

            result = triage(final_symptoms, severity, age)
            urgency = result["urgency"]
            logger.info(f"Triage result: {urgency}")

            st.divider()
            st.subheader("📋 Triage Result")

            if urgency == "EMERGENCY":
                st.markdown(f"""
                <div class="result-card emergency-card">
                    <h3 style="color:#dc2626; margin-top:0;">🚨 EMERGENCY DETECTED</h3>
                    <p>{result['message']}</p>
                </div>
                """, unsafe_allow_html=True)
                if result["red_flags"]:
                    st.write("**Warning signs:**")
                    for f in result["red_flags"]:
                        st.write(f"- {f}")
                st.error(f"📞 Call {EMERGENCY_NUMBER} now or go to the nearest ER.")

            elif urgency == "URGENT":
                st.markdown(f"""
                <div class="result-card urgent-card">
                    <h3 style="color:#d97706; margin-top:0;">⚠️ URGENT CARE NEEDED</h3>
                    <p>{result['message']}</p>
                </div>
                """, unsafe_allow_html=True)

            else:
                st.markdown(f"""
                <div class="result-card routine-card">
                    <h3 style="color:#16a34a; margin-top:0;">✅ Recommended: {result['department']}</h3>
                    <p>{result['message']}</p>
                </div>
                """, unsafe_allow_html=True)

                st.subheader("👨‍⚕️ Recommended Doctors")
                doctors = result.get("doctors", [])
                if doctors:
                    for d in doctors:
                        st.markdown(f"""
                        <div class="doctor-card">
                            <div class="doctor-name">👨‍⚕️ {d['name']}</div>
                            <div class="doctor-specialty">{d['specialty']} · {d['department']}</div>
                            <div style="font-size:0.85rem; color:#475569;">
                                🕒 <b>Availability:</b> {d['availability']}<br>
                                📍 <b>Location:</b> {d['location']}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("No specific doctor data. Please contact reception.")

            st.caption("This is not a medical diagnosis. Consult a qualified doctor.")

# ============================================================
# TAB 2 — DOCTORS DIRECTORY
# ============================================================
with tab2:
    st.subheader("🏥 Hospital Doctors Directory")
    st.write("Browse specialists across all departments.")

    doctors_data = load_json(DOCTORS_FILE)

    if not doctors_data:
        st.warning("No doctor data available.")
    else:
        departments_list = sorted(set(d["department"] for d in doctors_data))
        selected = st.selectbox("Filter by Department", ["All"] + departments_list)

        filtered = doctors_data if selected == "All" else [
            d for d in doctors_data if d["department"] == selected
        ]

        cols = st.columns(2)
        for i, d in enumerate(filtered):
            with cols[i % 2]:
                st.markdown(f"""
                <div class="doctor-card">
                    <div class="doctor-name">👨‍⚕️ {d['name']}</div>
                    <div class="doctor-specialty">{d['specialty']} · {d['department']}</div>
                    <div style="font-size:0.85rem; color:#475569;">
                        🕒 <b>Availability:</b> {d['availability']}<br>
                        📍 <b>Location:</b> {d['location']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("📅 Book Appointment", key=f"book_{d['id']}"):
                    st.success(f"Appointment request sent to {d['name']}!")

# ============================================================
# TAB 3 — ABOUT
# ============================================================
with tab3:
    st.subheader("ℹ️ About This Project")
    st.markdown(f"""
    **Hospital AI Agent** is a navigation assistant that helps patients
    find the appropriate department or doctor based on symptoms and urgency.

    ### 🏗️ Architecture
    - **Frontend:** Streamlit + Custom CSS (medical theme)
    - **Logic:** Rule-based triage + optional LLM summarizer
    - **Data:** JSON hospital records
    - **Safety:** Red-flag detection · Emergency escalation · Audit logging

    ### ⚠️ Disclaimer
    {DISCLAIMER}

    This is a demonstration project. Always consult a qualified healthcare professional.
    """)
    st.divider()
    st.caption("Built with ❤️ using Python & Streamlit")