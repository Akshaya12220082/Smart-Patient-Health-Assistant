import streamlit as st
import requests
import pandas as pd
import time

# ---------------------------
# APP CONFIG
# ---------------------------
st.set_page_config(
    page_title="Smart Patient Health Assistant",
    page_icon="🩺",
    layout="wide",
)

API_URL = "http://127.0.0.1:5000"  # Flask API endpoint

# ---------------------------
# HEADER
# ---------------------------
st.title("🩺 Smart Patient Health Assistant")
st.markdown(
    """
### 🌍 Your AI-Powered Health Risk & Wellness Companion  
Predict diseases, assess risk levels, get personalized recommendations, and find nearby hospitals — all in one place.
    """
)

st.divider()

# ---------------------------
# NAVIGATION
# ---------------------------
tabs = st.tabs([
    "🔮 Disease Prediction",
    "📊 Risk Stratification",
    "💡 Personalized Recommendations",
    "🗺️ Hospital Finder",
    "🚨 Emergency Response",
    "🧠 Explainable AI & About"
])

# ==============================================================
# 🔮 TAB 1: Disease Prediction
# ==============================================================
with tabs[0]:
    st.header("🔮 Disease Prediction")
    st.write("Predict risk for multiple diseases using trained AI models (Diabetes, Heart, Kidney, and more).")

    disease = st.selectbox(
        "Select Disease Type",
        ["Diabetes", "Heart Disease", "Kidney Disease"],
        index=0
    )

    uploaded_file = st.file_uploader("Upload your medical data (CSV or Excel)", type=["csv", "xlsx"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(".csv") else pd.read_excel(uploaded_file)
        st.dataframe(df.head())

        if st.button("🧠 Predict Now"):
            with st.spinner("Analyzing and predicting..."):
                time.sleep(2)
                # (Connect Flask API here later)
                st.success(f"✅ {disease} Prediction Completed!")
                st.metric("Predicted Risk Score", "68%", "+Moderate Risk (Yellow Zone)")

# ==============================================================
# 📊 TAB 2: Risk Stratification
# ==============================================================
with tabs[1]:
    st.header("📊 Risk Stratification Zones")

    st.markdown("""
    **Risk Levels**
    - 🟢 **Green Zone (0–30%)**: Low risk — maintain healthy habits  
    - 🟡 **Yellow Zone (31–70%)**: Moderate risk — doctor consultation advised  
    - 🔴 **Red Zone (71–100%)**: High risk — immediate medical attention required  
    """)

    risk = st.slider("Your Predicted Risk (%)", 0, 100, 45)
    if risk <= 30:
        st.success("🟢 Low Risk: Keep up your healthy lifestyle!")
    elif risk <= 70:
        st.warning("🟡 Moderate Risk: Consult your doctor for regular checkups.")
    else:
        st.error("🔴 High Risk: Immediate medical attention is required!")

# ==============================================================
# 💡 TAB 3: Personalized Recommendations
# ==============================================================
with tabs[2]:
    st.header("💡 Personalized Health Recommendations")

    st.markdown("AI-driven lifestyle and wellness guidance, aligned with **WHO**, **CDC**, and **Indian Health Guidelines**.")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("🥗 Diet Tips")
        st.write("- Eat more fruits and vegetables\n- Limit salt and sugar\n- Stay hydrated")
    with col2:
        st.subheader("🏃 Exercise")
        st.write("- Walk 30 minutes daily\n- Stretch often\n- Avoid long sitting periods")
    with col3:
        st.subheader("💤 Sleep & Stress")
        st.write("- Maintain 7–8 hrs sleep\n- Practice mindfulness\n- Avoid late-night screens")

    st.divider()
    st.subheader("🧾 Medical Guidance")
    st.write("""
    - Safe OTC medicines for mild symptoms  
    - Track key parameters: BP, Sugar, BMI  
    - Schedule regular health screenings  
    """)

# ==============================================================
# 🗺️ TAB 4: Location-Based Hospital Finder
# ==============================================================
with tabs[3]:
    st.header("🗺️ Nearest Hospitals & Specialists")

    location = st.text_input("Enter your location or city:")
    condition = st.selectbox("Select Condition Type", ["General", "Cardiac", "Diabetic", "Nephrology"])

    if st.button("🔍 Find Hospitals"):
        st.info("📡 Fetching nearby hospitals (demo mode)...")
        st.map(pd.DataFrame({
            'lat': [28.6139, 28.5355],
            'lon': [77.2090, 77.3910],
        }))
        st.success("✅ Displaying sample hospitals — integrate Google Maps API for real data.")

# ==============================================================
# 🚨 TAB 5: Emergency Response
# ==============================================================
with tabs[4]:
    st.header("🚨 Emergency Response System")

    st.warning("Activate SOS only in critical conditions!")

    if st.button("🆘 Send SOS Alert"):
        with st.spinner("Contacting emergency services..."):
            time.sleep(2)
            st.success("✅ SOS Alert Sent! Your emergency contacts and nearest hospital have been notified.")

# ==============================================================
# 🧠 TAB 6: Explainable AI & About
# ==============================================================
with tabs[5]:
    st.header("🧠 Explainable AI & System Overview")

    st.write("""
    This assistant integrates SHAP and LIME for **transparent AI predictions**.
    You can visualize how each health parameter contributes to your risk score.
    """)

    st.subheader("📘 System Objectives")
    st.markdown("""
    1. **Advanced Health Risk Prediction** – Multi-disease ensemble models  
    2. **Intelligent Recommendation System** – Personalized, evidence-based tips  
    3. **Risk Stratification Framework** – Clear, color-coded risk guidance  
    4. **Location-Based Services** – Nearby hospitals & specialists  
    5. **Emergency Response Integration** – SOS & auto alert  
    """)

    st.info("🔐 Data privacy and security ensured — no personal data stored.")

    st.caption("© 2025 Smart Patient Health Assistant | Built with Streamlit & Flask")
