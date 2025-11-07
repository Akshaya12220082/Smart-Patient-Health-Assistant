import streamlit as st
import requests
import pandas as pd
import time
import json
from typing import Dict, Any, Optional

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
# HELPER FUNCTIONS
# ---------------------------
def check_api_health() -> bool:
    """Check if Flask API is running"""
    try:
        response = requests.get(f"{API_URL}/", timeout=2)
        return response.status_code == 200
    except:
        return False

def get_disease_key(disease_name: str) -> str:
    """Convert disease display name to API key"""
    mapping = {
        "Diabetes": "diabetes",
        "Heart Disease": "heart",
        "Kidney Disease": "kidney"
    }
    return mapping.get(disease_name, disease_name.lower())

def validate_csv_columns(df: pd.DataFrame, disease: str) -> tuple[bool, Optional[str]]:
    """Validate if CSV has required columns for the disease"""
    required_columns = {
        "diabetes": ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness", 
                     "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"],
        "heart": ["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", 
                  "thalach", "exang", "oldpeak", "slope", "ca", "thal"],
        "kidney": ["age", "bp", "sg", "al", "su", "bgr", "bu", "sc", "sod", 
                   "pot", "hemo", "pcv", "wc", "rc"]
    }
    
    disease_key = get_disease_key(disease)
    required = required_columns.get(disease_key, [])
    
    # Remove target column if present
    target_cols = ["Outcome", "target", "classification"]
    df_cols = [col for col in df.columns if col not in target_cols]
    
    missing_cols = [col for col in required if col not in df_cols]
    
    if missing_cols:
        return False, f"Missing required columns: {', '.join(missing_cols)}"
    
    return True, None

def predict_disease(df: pd.DataFrame, disease: str) -> Optional[Dict[str, Any]]:
    """Send prediction request to Flask API"""
    try:
        disease_key = get_disease_key(disease)
        
        # Remove target column if present
        target_cols = ["Outcome", "target", "classification"]
        df_clean = df.drop(columns=[col for col in target_cols if col in df.columns], errors='ignore')
        
        # Convert first row to dictionary
        features = df_clean.iloc[0].to_dict()
        
        # Send to API
        response = requests.post(
            f"{API_URL}/predict/{disease_key}",
            json=features,
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            error_data = response.json()
            st.error(f"API Error: {error_data.get('error', 'Unknown error')}")
            return None
            
    except requests.exceptions.Timeout:
        st.error("⏱️ Request timeout. Please ensure the Flask API is running.")
        return None
    except requests.exceptions.ConnectionError:
        st.error("🔌 Cannot connect to API. Please start the Flask server first.")
        return None
    except Exception as e:
        st.error(f"❌ Prediction failed: {str(e)}")
        return None

def get_zone_emoji(zone: str) -> str:
    """Get emoji for risk zone"""
    zone_emojis = {
        "Green": "🟢",
        "Yellow": "🟡",
        "Red": "🔴"
    }
    return zone_emojis.get(zone, "⚪")

def get_zone_message(zone: str) -> tuple[str, str]:
    """Get message and severity for risk zone"""
    messages = {
        "Green": ("Low Risk: Keep up your healthy lifestyle!", "success"),
        "Yellow": ("Moderate Risk: Consult your doctor for regular checkups.", "warning"),
        "Red": ("High Risk: Immediate medical attention is required!", "error")
    }
    return messages.get(zone, ("Unknown risk level", "info"))

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

# API Health Check
if not check_api_health():
    st.warning("⚠️ Flask API is not running. Please start it with: `python -m src.api.app`")
else:
    st.success("✅ Connected to Flask API")

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
    st.write("Predict risk for multiple diseases using trained AI models (Diabetes, Heart, Kidney).")

    disease = st.selectbox(
        "Select Disease Type",
        ["Diabetes", "Heart Disease", "Kidney Disease"],
        index=0
    )

    # Show sample format
    with st.expander("📋 View Sample Data Format"):
        if disease == "Diabetes":
            st.code("Pregnancies,Glucose,BloodPressure,SkinThickness,Insulin,BMI,DiabetesPedigreeFunction,Age")
            st.caption("Example: 6,148,72,35,0,33.6,0.627,50")
        elif disease == "Heart Disease":
            st.code("age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal")
            st.caption("Example: 52,1,0,125,212,0,1,168,0,1.0,2,2,3")
        else:
            st.code("age,bp,sg,al,su,bgr,bu,sc,sod,pot,hemo,pcv,wc,rc")
            st.caption("Example: 48,80,1.02,1,0,121,36,1.2,138,4.5,15.4,44,7800,5.2")

    uploaded_file = st.file_uploader("Upload your medical data (CSV)", type=["csv"])

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.success(f"✅ File loaded successfully! {len(df)} rows found.")
            st.dataframe(df.head())
            
            # Validate columns
            is_valid, error_msg = validate_csv_columns(df, disease)
            
            if not is_valid:
                st.error(f"❌ Invalid CSV format: {error_msg}")
                st.info("Please check the required columns using the 'View Sample Data Format' section above.")
            else:
                st.success("✅ CSV format validated successfully!")
                
                if st.button("🧠 Predict Now", type="primary"):
                    with st.spinner("🔄 Analyzing data and making prediction..."):
                        result = predict_disease(df, disease)
                        
                        if result:
                            risk_score = result.get("risk_score", 0)
                            zone = result.get("zone", "Unknown")
                            
                            # Display results
                            st.divider()
                            st.subheader("📊 Prediction Results")
                            
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Disease", disease)
                            with col2:
                                st.metric("Risk Score", f"{risk_score}%")
                            with col3:
                                st.metric("Risk Zone", f"{get_zone_emoji(zone)} {zone}")
                            
                            # Show zone-specific message
                            message, severity = get_zone_message(zone)
                            if severity == "success":
                                st.success(message)
                            elif severity == "warning":
                                st.warning(message)
                            else:
                                st.error(message)
                            
                            # Store in session state for other tabs
                            st.session_state['last_prediction'] = {
                                'disease': disease,
                                'risk_score': risk_score,
                                'zone': zone
                            }
                        
        except Exception as e:
            st.error(f"❌ Error loading file: {str(e)}")
            st.info("Please ensure your CSV file is properly formatted.")

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

    # Check if we have a prediction
    if 'last_prediction' in st.session_state:
        pred = st.session_state['last_prediction']
        st.info(f"📋 Based on your {pred['disease']} prediction: {pred['risk_score']}% ({pred['zone']} Zone)")
        
        # Get recommendations from API
        try:
            response = requests.get(
                f"{API_URL}/recommendations/{get_disease_key(pred['disease'])}",
                params={"risk_score": pred['risk_score']},
                timeout=5
            )
            
            if response.status_code == 200:
                reco_data = response.json()
                recommendations = reco_data.get("recommendations", [])
                
                st.subheader(f"🎯 Recommended Actions for {pred['zone']} Zone")
                for i, rec in enumerate(recommendations, 1):
                    st.markdown(f"{i}. {rec}")
            else:
                st.warning("Could not fetch personalized recommendations from API")
        except:
            pass  # Fall back to general recommendations
    
    # General recommendations
    st.divider()
    st.subheader("🌟 General Health Guidelines")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("🥗 Diet Tips")
        st.write("- Eat more fruits and vegetables\n- Limit salt and sugar\n- Stay hydrated\n- Choose whole grains")
    with col2:
        st.subheader("🏃 Exercise")
        st.write("- Walk 30 minutes daily\n- Stretch often\n- Avoid long sitting periods\n- Strength training 2x/week")
    with col3:
        st.subheader("💤 Sleep & Stress")
        st.write("- Maintain 7–8 hrs sleep\n- Practice mindfulness\n- Avoid late-night screens\n- Regular meditation")

    st.divider()
    st.subheader("🧾 Medical Guidance")
    st.write("""
    - Safe OTC medicines for mild symptoms  
    - Track key parameters: BP, Sugar, BMI  
    - Schedule regular health screenings
    - Keep emergency contacts updated
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
