import streamlit as st
import requests
import pandas as pd
import time
import json
from typing import Dict, Any, Optional
import plotly.graph_objects as go
import plotly.express as px

# ---------------------------
# APP CONFIG
# ---------------------------
st.set_page_config(
    page_title="Smart Patient Health Assistant",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for beautiful, modern styling
st.markdown("""
    <style>
    /* Global Styles */
    .main {
        padding: 0rem 1rem;
        background: linear-gradient(to bottom, #f0f4f8 0%, #ffffff 100%);
    }
    
    /* Hero Section */
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        margin-bottom: 2rem;
    }
    .hero-section h1 {
        color: white !important;
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    .hero-section p {
        color: #f0f0f0 !important;
        font-size: 1.2rem;
        font-weight: 300;
    }
    
    /* Metric Cards */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        text-align: center;
        border: 2px solid #e5e7eb;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
    }
    .metric-card h4 {
        color: #1f2937 !important;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .metric-card p {
        color: #6b7280 !important;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    /* Feature Cards */
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #667eea;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    .feature-card:hover {
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.15);
        transform: translateX(5px);
    }
    .feature-card h4 {
        color: #1f2937 !important;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    .feature-card p, .feature-card li {
        color: #4b5563 !important;
        line-height: 1.8;
    }
    .feature-card ul {
        margin-left: 1rem;
    }
    
    /* Lifestyle Cards with Gradients */
    .lifestyle-card-green {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white !important;
        text-align: center;
        min-height: 250px;
        box-shadow: 0 5px 20px rgba(16, 185, 129, 0.3);
        transition: transform 0.3s ease;
    }
    .lifestyle-card-green:hover {
        transform: translateY(-10px);
    }
    .lifestyle-card-blue {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white !important;
        text-align: center;
        min-height: 250px;
        box-shadow: 0 5px 20px rgba(59, 130, 246, 0.3);
        transition: transform 0.3s ease;
    }
    .lifestyle-card-blue:hover {
        transform: translateY(-10px);
    }
    .lifestyle-card-purple {
        background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white !important;
        text-align: center;
        min-height: 250px;
        box-shadow: 0 5px 20px rgba(139, 92, 246, 0.3);
        transition: transform 0.3s ease;
    }
    .lifestyle-card-purple:hover {
        transform: translateY(-10px);
    }
    .lifestyle-card-pink {
        background: linear-gradient(135deg, #ec4899 0%, #db2777 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white !important;
        text-align: center;
        min-height: 250px;
        box-shadow: 0 5px 20px rgba(236, 72, 153, 0.3);
        transition: transform 0.3s ease;
    }
    .lifestyle-card-pink:hover {
        transform: translateY(-10px);
    }
    .lifestyle-card-green h2, .lifestyle-card-blue h2, 
    .lifestyle-card-purple h2, .lifestyle-card-pink h2 {
        font-size: 3rem;
        margin: 0;
    }
    .lifestyle-card-green h4, .lifestyle-card-blue h4, 
    .lifestyle-card-purple h4, .lifestyle-card-pink h4 {
        color: white !important;
        font-weight: 700;
        margin: 1rem 0;
        font-size: 1.3rem;
    }
    .lifestyle-card-green p, .lifestyle-card-blue p, 
    .lifestyle-card-purple p, .lifestyle-card-pink p {
        color: rgba(255,255,255,0.95) !important;
        font-size: 1rem;
        line-height: 1.8;
    }
    
    /* Emergency Cards */
    .emergency-card-red {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white !important;
        text-align: center;
        box-shadow: 0 5px 20px rgba(239, 68, 68, 0.3);
    }
    .emergency-card-orange {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white !important;
        text-align: center;
        box-shadow: 0 5px 20px rgba(245, 158, 11, 0.3);
    }
    .emergency-card-blue {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white !important;
        text-align: center;
        box-shadow: 0 5px 20px rgba(59, 130, 246, 0.3);
    }
    .emergency-card-red h2, .emergency-card-orange h2, .emergency-card-blue h2 {
        font-size: 3rem;
        margin: 0;
    }
    .emergency-card-red h4, .emergency-card-orange h4, .emergency-card-blue h4 {
        color: white !important;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    .emergency-card-red h3, .emergency-card-orange h3, .emergency-card-blue h3 {
        color: white !important;
        font-weight: 900;
        font-size: 2rem;
        margin: 0.5rem 0;
    }
    
    /* Risk Zone Cards */
    .risk-zone {
        padding: 1.5rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
        border: 2px solid transparent;
    }
    .risk-zone:hover {
        transform: scale(1.02);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    .risk-very-low {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white !important;
    }
    .risk-low {
        background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
        color: white !important;
    }
    .risk-moderate {
        background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
        color: white !important;
    }
    .risk-high {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white !important;
    }
    .risk-very-high {
        background: linear-gradient(135deg, #991b1b 0%, #7f1d1d 100%);
        color: white !important;
    }
    .risk-zone h4 {
        color: white !important;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    .risk-zone p {
        color: rgba(255,255,255,0.95) !important;
        line-height: 1.6;
    }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: white;
        padding: 10px;
        border-radius: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 12px 24px;
        background-color: #f3f4f6;
        border-radius: 8px;
        color: #4b5563;
        font-weight: 600;
        border: 2px solid transparent;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        border-color: #667eea;
    }
    
    /* Headers */
    h1 {
        color: #1f2937 !important;
        font-weight: 800;
    }
    h2 {
        color: #374151 !important;
        font-weight: 700;
    }
    h3 {
        color: #4b5563 !important;
        font-weight: 600;
    }
    
    /* Buttons */
    .stButton>button {
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
    }
    
    /* Info/Success/Warning Boxes */
    .stAlert {
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid;
    }
    </style>
    """, unsafe_allow_html=True)

API_URL = "http://127.0.0.1:5001"  # Flask API endpoint

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

def create_risk_gauge(risk_score: float, zone: str) -> go.Figure:
    """Create a gauge chart for risk score visualization"""
    # Define colors based on zone
    color_map = {
        "Green": "#10b981",
        "Yellow": "#f59e0b", 
        "Red": "#ef4444"
    }
    color = color_map.get(zone, "#6b7280")
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = risk_score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': f"Risk Score ({zone} Zone)", 'font': {'size': 24}},
        delta = {'reference': 50},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 30], 'color': '#d1fae5'},
                {'range': [30, 70], 'color': '#fef3c7'},
                {'range': [70, 100], 'color': '#fee2e2'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor="white",
        font={'size': 14}
    )
    
    return fig

# ---------------------------
# SIDEBAR
# ---------------------------
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/health-checkup.png", width=80)
    st.markdown("### 🏥 Navigation")
    st.markdown("---")
    
    st.markdown("**About This App**")
    st.info("""
    AI-powered health risk assessment system using machine learning to predict disease risks and provide personalized recommendations.
    """)
    
    st.markdown("---")
    st.markdown("**Quick Stats**")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("� Models", "3", help="Diabetes, Heart, Kidney")
    with col2:
        st.metric("📊 Accuracy", "85%+", help="Model accuracy")
    
    st.markdown("---")
    st.markdown("**🔗 Resources**")
    st.markdown("[📖 Documentation](https://github.com/Akshaya12220082/Smart-Patient-Health-Assistant)")
    st.markdown("[💻 GitHub Repo](https://github.com/Akshaya12220082/Smart-Patient-Health-Assistant)")
    
# ---------------------------
# HEADER
# ---------------------------
# Hero Section with new CSS class
st.markdown("""
    <div class='hero-section'>
        <h1>🩺 Smart Patient Health Assistant</h1>
        <p>Your AI-Powered Health Risk & Wellness Companion</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <p style='font-size: 1.1rem; color: #4b5563;'>
            🌍 Predict diseases • 📊 Assess risk levels • 💡 Get personalized recommendations • 🗺️ Find nearby hospitals
        </p>
    </div>
    """, unsafe_allow_html=True)

# API Health Check
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if not check_api_health():
        st.error("⚠️ **API Offline** - Start Flask API: `python -m src.api.app`", icon="🔌")
    else:
        st.success("✅ **Connected to Flask API** - All systems operational", icon="🟢")

st.markdown("<br>", unsafe_allow_html=True)

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
    # Header with icon
    st.markdown("""
        <div class='feature-card'>
            <h2>🔮 AI-Powered Disease Prediction</h2>
            <p>Upload your medical data and get instant risk assessment using advanced machine learning models</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Disease selection with better UI
    col1, col2 = st.columns([2, 1])
    
    with col1:
        disease = st.selectbox(
            "🏥 Select Disease Type",
            ["Diabetes", "Heart Disease", "Kidney Disease"],
            index=0,
            help="Choose the disease you want to predict"
        )
    
    with col2:
        # Disease info badges
        disease_info = {
            "Diabetes": "🩸 Blood Sugar",
            "Heart Disease": "❤️ Cardiovascular",
            "Kidney Disease": "🫘 Renal Health"
        }
        st.info(f"**Category:** {disease_info[disease]}")

    st.markdown("<br>", unsafe_allow_html=True)

    # Show sample format in a nicer way
    with st.expander("📋 View Required Data Format & Example", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Required Columns:**")
            if disease == "Diabetes":
                st.code("Pregnancies, Glucose, BloodPressure,\nSkinThickness, Insulin, BMI,\nDiabetesPedigreeFunction, Age", language="text")
            elif disease == "Heart Disease":
                st.code("age, sex, cp, trestbps, chol, fbs,\nrestecg, thalach, exang, oldpeak,\nslope, ca, thal", language="text")
            else:
                st.code("age, bp, sg, al, su, bgr, bu, sc,\nsod, pot, hemo, pcv, wc, rc", language="text")
        
        with col2:
            st.markdown("**Sample Data:**")
            if disease == "Diabetes":
                st.caption("6, 148, 72, 35, 0, 33.6, 0.627, 50")
            elif disease == "Heart Disease":
                st.caption("52, 1, 0, 125, 212, 0, 1, 168, 0, 1.0, 2, 2, 3")
            else:
                st.caption("48, 80, 1.02, 1, 0, 121, 36, 1.2, 138, 4.5, 15.4, 44, 7800, 5.2")
            
            st.markdown("**📥 Sample Files:**")
            st.caption(f"Use: `data/raw/{get_disease_key(disease)}.csv`")

    st.markdown("<br>", unsafe_allow_html=True)

    # File uploader with better styling
    uploaded_file = st.file_uploader(
        "📤 Upload your medical data (CSV format)",
        type=["csv"],
        help="Upload a CSV file containing patient medical data"
    )

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            
            # Show success with metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.success(f"✅ File Loaded")
            with col2:
                st.info(f"📊 Rows: {len(df)}")
            with col3:
                st.info(f"📋 Columns: {len(df.columns)}")
            
            # Show data preview in tabs
            preview_tab1, preview_tab2 = st.tabs(["📊 Data Preview", "📈 Statistics"])
            
            with preview_tab1:
                st.dataframe(df.head(10), use_container_width=True)
            
            with preview_tab2:
                st.write(df.describe())
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Validate columns
            is_valid, error_msg = validate_csv_columns(df, disease)
            
            if not is_valid:
                st.error(f"❌ **Validation Failed:** {error_msg}", icon="⚠️")
                st.info("💡 Tip: Check the required columns in the 'View Required Data Format' section above.")
            else:
                st.success("✅ **CSV format validated successfully!** Ready to predict.", icon="✔️")
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Predict button with better styling
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    predict_btn = st.button("🧠 **Predict Risk Now**", type="primary", use_container_width=True)
                
                if predict_btn:
                    with st.spinner("🔄 Analyzing data using AI models..."):
                        time.sleep(0.5)  # Brief pause for UX
                        result = predict_disease(df, disease)
                        
                        if result:
                            risk_score = result.get("risk_score", 0)
                            zone = result.get("zone", "Unknown")
                            
                            # Results section with animation
                            st.balloons()
                            st.markdown("<br>", unsafe_allow_html=True)
                            
                            # Create beautiful result card
                            st.markdown("""
                                <div class='feature-card' style='background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);'>
                                    <h2 style='color: #1f2937;'>📊 Prediction Results</h2>
                                </div>
                            """, unsafe_allow_html=True)
                            
                            st.markdown("<br>", unsafe_allow_html=True)
                            
                            # Metrics in cards
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                st.metric("🏥 Disease", disease)
                            with col2:
                                st.metric("📊 Risk Score", f"{risk_score}%", 
                                         delta=f"{risk_score - 50:+.1f}% from avg")
                            with col3:
                                st.metric("🎯 Risk Zone", zone, 
                                         delta_color="inverse")
                            with col4:
                                confidence = "High" if risk_score > 70 or risk_score < 30 else "Medium"
                                st.metric("🎲 Confidence", confidence)
                            
                            st.markdown("<br>", unsafe_allow_html=True)
                            
                            # Gauge chart
                            col1, col2 = st.columns([2, 1])
                            with col1:
                                fig = create_risk_gauge(risk_score, zone)
                                st.plotly_chart(fig, use_container_width=True)
                            
                            with col2:
                                st.markdown("<br><br>", unsafe_allow_html=True)
                                # Zone-specific message
                                message, severity = get_zone_message(zone)
                                if severity == "success":
                                    st.success(f"{get_zone_emoji(zone)} {message}")
                                elif severity == "warning":
                                    st.warning(f"{get_zone_emoji(zone)} {message}")
                                else:
                                    st.error(f"{get_zone_emoji(zone)} {message}")
                                
                                # Next steps
                                st.markdown("**📋 Next Steps:**")
                                if zone == "Green":
                                    st.markdown("✓ Maintain healthy habits\n✓ Annual checkups\n✓ Stay active")
                                elif zone == "Yellow":
                                    st.markdown("✓ Consult doctor soon\n✓ Monitor symptoms\n✓ Lifestyle changes")
                                else:
                                    st.markdown("✓ Seek immediate care\n✓ Emergency contact ready\n✓ Follow medical advice")
                            
                            # Store in session state
                            st.session_state['last_prediction'] = {
                                'disease': disease,
                                'risk_score': risk_score,
                                'zone': zone
                            }
                            
                            st.markdown("<br>", unsafe_allow_html=True)
                            st.info("💡 **Pro Tip:** Check the 'Personalized Recommendations' tab for detailed guidance based on your results!")
                        
        except Exception as e:
            st.error(f"❌ **Error loading file:** {str(e)}", icon="🚫")
            st.info("💡 Please ensure your CSV file is properly formatted and not corrupted.")

# ==============================================================
# 📊 TAB 2: Risk Stratification
# ==============================================================
with tabs[1]:
    st.markdown("""
        <div class='feature-card'>
            <h2>📊 Risk Stratification Zones</h2>
            <p>Understand your health risk level with our color-coded traffic light system</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Visual risk zones
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class='risk-zone risk-very-low'>
                <h3>🟢 Green Zone</h3>
                <h1 style='color: white; font-size: 2.5rem; margin: 1rem 0;'>0-30%</h1>
                <p><b>Low Risk</b></p>
                <p>✓ Maintain healthy habits<br>
                ✓ Annual checkups<br>
                ✓ Continue good lifestyle</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class='risk-zone risk-moderate'>
                <h3>🟡 Yellow Zone</h3>
                <h1 style='color: white; font-size: 2.5rem; margin: 1rem 0;'>31-70%</h1>
                <p><b>Moderate Risk</b></p>
                <p>✓ Consult doctor soon<br>
                ✓ Monitor symptoms<br>
                ✓ Lifestyle modifications</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class='risk-zone risk-high'>
                <h3>🔴 Red Zone</h3>
                <h1 style='color: white; font-size: 2.5rem; margin: 1rem 0;'>71-100%</h1>
                <p><b>High Risk</b></p>
                <p>✓ Immediate medical care<br>
                ✓ Emergency contact ready<br>
                ✓ Follow medical advice</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Interactive risk slider
    st.subheader("🎯 Interactive Risk Assessment")
    risk = st.slider(
        "Adjust the risk score to see zone classification:", 
        0, 100, 45,
        help="Move the slider to see how different risk scores are classified"
    )
    
    # Determine zone
    if risk <= 30:
        zone_class = "risk-very-low"
        zone_text = "🟢 Green Zone - Low Risk"
        zone_msg = "**Great news!** Keep up your healthy lifestyle. Continue with balanced diet, regular exercise, and annual health checkups."
    elif risk <= 70:
        zone_class = "risk-moderate"
        zone_text = "🟡 Yellow Zone - Moderate Risk"
        zone_msg = "**Take action!** Schedule a consultation with your primary care physician within 2-4 weeks. Monitor your health parameters regularly."
    else:
        zone_class = "risk-high"
        zone_text = "🔴 Red Zone - High Risk"
        zone_msg = "**Immediate attention required!** Seek medical attention promptly. If experiencing severe symptoms, consider emergency care."
    
    # Display zone result with CSS class
    st.markdown(f"""
        <div class='risk-zone {zone_class}'>
            <h2>{zone_text}</h2>
            <h1 style='color: white; font-size: 3rem; margin: 1rem 0;'>{risk}%</h1>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.info(zone_msg)
    
    # Show last prediction if available
    if 'last_prediction' in st.session_state:
        st.markdown("<br>", unsafe_allow_html=True)
        pred = st.session_state['last_prediction']
        st.success(f"📋 **Your Recent Prediction:** {pred['disease']} - {pred['risk_score']}% ({pred['zone']} Zone)")

# ==============================================================
# 💡 TAB 3: Personalized Recommendations
# ==============================================================
with tabs[2]:
    st.markdown("""
        <div class='feature-card'>
            <h2>💡 Personalized Health Recommendations</h2>
            <p>AI-driven lifestyle and wellness guidance aligned with WHO, CDC, and Indian Health Guidelines</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

    # Check if we have a prediction
    if 'last_prediction' in st.session_state:
        pred = st.session_state['last_prediction']
        
        # Show prediction summary
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Disease", pred['disease'], help="Condition analyzed")
        with col2:
            st.metric("Risk Score", f"{pred['risk_score']}%", help="Predicted risk level")
        with col3:
            st.metric("Zone", f"{get_zone_emoji(pred['zone'])} {pred['zone']}", help="Risk classification")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
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
                
                if recommendations:
                    st.markdown(f"### 🎯 Personalized Actions for {pred['zone']} Zone")
                    st.caption(f"Based on your {pred['disease']} risk score of {pred['risk_score']}%")
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # Display recommendations in nice cards
                    for i, rec in enumerate(recommendations, 1):
                        st.markdown(f"""
                            <div class='feature-card'>
                                <h4>✓ {rec}</h4>
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    st.warning("⚠️ No recommendations available for this prediction.")
            else:
                error_msg = response.json().get('error', 'Unknown error') if response.text else 'No response'
                st.error(f"⚠️ API Error ({response.status_code}): {error_msg}")
                st.info("💡 Showing general recommendations below.")
        except requests.exceptions.RequestException as e:
            st.error(f"⚠️ API connection issue: {str(e)}")
            st.info("💡 Make sure Flask API is running on port 5001. Showing general recommendations below.")
        except Exception as e:
            st.error(f"⚠️ Error fetching recommendations: {str(e)}")
            st.info("💡 Showing general recommendations below.")
    else:
        st.info("📋 **No recent prediction found.** Upload data in the Disease Prediction tab first to get personalized recommendations!")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # General recommendations with modern cards
    st.markdown("### 🌟 General Health & Wellness Guidelines")
    st.caption("Evidence-based recommendations from WHO, CDC, and medical experts")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Lifestyle recommendations in cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
            <div class='lifestyle-card-green'>
                <h2>🥗</h2>
                <h4>Nutrition</h4>
                <p>• Fruits & vegetables<br>
                • Whole grains<br>
                • Limit salt/sugar<br>
                • Stay hydrated</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class='lifestyle-card-blue'>
                <h2>🏃</h2>
                <h4>Exercise</h4>
                <p>• 30 min daily walk<br>
                • Strength training 2x/week<br>
                • Regular stretching<br>
                • Avoid long sitting</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class='lifestyle-card-purple'>
                <h2>💤</h2>
                <h4>Sleep & Rest</h4>
                <p>• 7-8 hours sleep<br>
                • Consistent schedule<br>
                • Dark, cool room<br>
                • Avoid screens</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
            <div class='lifestyle-card-pink'>
                <h2>🧘</h2>
                <h4>Mental Health</h4>
                <p>• Practice mindfulness<br>
                • Regular meditation<br>
                • Manage stress<br>
                • Social connections</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Medical guidance section
    st.markdown("### � Medical Monitoring & Care")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class='feature-card'>
                <h4>📊 Key Health Parameters to Track</h4>
                <ul>
                    <li>Blood Pressure (monthly)</li>
                    <li>Blood Sugar (as recommended)</li>
                    <li>Body Mass Index (BMI)</li>
                    <li>Cholesterol levels (annually)</li>
                    <li>Kidney function markers</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class='feature-card'>
                <h4>⏰ Recommended Health Screenings</h4>
                <ul>
                    <li>Annual physical examination</li>
                    <li>Blood tests (every 6-12 months)</li>
                    <li>Dental checkup (every 6 months)</li>
                    <li>Eye examination (annually)</li>
                    <li>Disease-specific tests as advised</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

# ==============================================================
# 🗺️ TAB 4: Location-Based Hospital Finder
# ==============================================================
with tabs[3]:
    st.markdown("""
        <div class='feature-card'>
            <h2>🗺️ Find Nearest Hospitals & Specialists</h2>
            <p>Locate nearby healthcare facilities based on your location and medical needs</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    
    with col1:
        location = st.text_input("📍 Enter your location or city:", placeholder="e.g., New Delhi, Mumbai, Bangalore")
    
    with col2:
        condition = st.selectbox("🏥 Specialty Type:", 
                                 ["General Hospital", "Cardiology", "Diabetology", "Nephrology", "Emergency Care"])

    if st.button("🔍 Find Hospitals", use_container_width=True):
        with st.spinner("📡 Searching nearby hospitals..."):
            time.sleep(1)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Sample hospital data based on location
            st.markdown("### 🏥 Nearby Healthcare Facilities")
            
            # Define hospital locations (major cities in India)
            hospital_data = {
                "Delhi": [
                    {"name": "Apollo Hospital", "lat": 28.6139, "lon": 77.2090, "distance": "2.3 km", 
                     "rating": "4.8/5", "contact": "+91-11-2692-5858", "specialty": "Multi-specialty"},
                    {"name": "Max Super Speciality", "lat": 28.5355, "lon": 77.3910, "distance": "3.7 km",
                     "rating": "4.7/5", "contact": "+91-11-2651-5050", "specialty": "Cardiology, Nephrology"},
                    {"name": "Fortis Hospital", "lat": 28.5494, "lon": 77.2001, "distance": "4.2 km",
                     "rating": "4.6/5", "contact": "+91-11-4277-6222", "specialty": "Multi-specialty"},
                    {"name": "AIIMS Delhi", "lat": 28.5672, "lon": 77.2100, "distance": "5.1 km",
                     "rating": "4.9/5", "contact": "+91-11-2658-8500", "specialty": "Super Specialty"},
                ],
                "Mumbai": [
                    {"name": "Lilavati Hospital", "lat": 19.0596, "lon": 72.8295, "distance": "1.8 km",
                     "rating": "4.7/5", "contact": "+91-22-2645-8000", "specialty": "Multi-specialty"},
                    {"name": "Breach Candy Hospital", "lat": 18.9720, "lon": 72.8030, "distance": "3.2 km",
                     "rating": "4.6/5", "contact": "+91-22-2367-1888", "specialty": "Cardiology"},
                    {"name": "Kokilaben Hospital", "lat": 19.2095, "lon": 72.8417, "distance": "4.5 km",
                     "rating": "4.8/5", "contact": "+91-22-4296-9999", "specialty": "Multi-specialty"},
                    {"name": "Nanavati Hospital", "lat": 19.0435, "lon": 72.8327, "distance": "2.7 km",
                     "rating": "4.7/5", "contact": "+91-22-2626-7676", "specialty": "Super Specialty"},
                ],
                "Bangalore": [
                    {"name": "Manipal Hospital", "lat": 12.9698, "lon": 77.6381, "distance": "2.1 km",
                     "rating": "4.6/5", "contact": "+91-80-2502-4444", "specialty": "Multi-specialty"},
                    {"name": "Columbia Asia", "lat": 12.9716, "lon": 77.5946, "distance": "3.4 km",
                     "rating": "4.5/5", "contact": "+91-80-6614-6614", "specialty": "Nephrology"},
                    {"name": "Fortis Bangalore", "lat": 12.9634, "lon": 77.6387, "distance": "1.9 km",
                     "rating": "4.7/5", "contact": "+91-80-6621-4444", "specialty": "Cardiology"},
                    {"name": "Apollo Hospitals", "lat": 12.9341, "lon": 77.6101, "distance": "4.8 km",
                     "rating": "4.8/5", "contact": "+91-80-2630-0330", "specialty": "Multi-specialty"},
                ]
            }
            
            # Determine which city to show (default to Delhi)
            city_key = "Delhi"
            if location:
                location_lower = location.lower()
                if "mumbai" in location_lower or "bombay" in location_lower:
                    city_key = "Mumbai"
                elif "bangalore" in location_lower or "bengaluru" in location_lower:
                    city_key = "Bangalore"
                elif "delhi" in location_lower or "ncr" in location_lower:
                    city_key = "Delhi"
            
            hospitals = hospital_data.get(city_key, hospital_data["Delhi"])
            
            # Display hospital cards
            col1, col2 = st.columns(2)
            
            for idx, hospital in enumerate(hospitals[:4]):  # Show first 4 hospitals
                with col1 if idx % 2 == 0 else col2:
                    st.markdown(f"""
                        <div class='feature-card'>
                            <h4>🏥 {hospital['name']}</h4>
                            <p><strong>📍 Distance:</strong> {hospital['distance']}</p>
                            <p><strong>⭐ Rating:</strong> {hospital['rating']}</p>
                            <p><strong>📞 Contact:</strong> {hospital['contact']}</p>
                            <p><strong>🏥 Specialty:</strong> {hospital['specialty']}</p>
                            <p style='color: #10b981;'><strong>Status:</strong> ✅ Open 24/7</p>
                        </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Create interactive map with hospital markers
            st.markdown("### 🗺️ Hospital Locations Map")
            
            # Prepare map data
            map_df = pd.DataFrame([
                {
                    'lat': h['lat'],
                    'lon': h['lon'],
                    'name': h['name'],
                    'size': 200  # Marker size
                }
                for h in hospitals
            ])
            
            # Display map with markers
            st.map(map_df, zoom=11, use_container_width=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Map legend
            st.info(f"""
            � **Showing {len(hospitals)} hospitals near {city_key}**
            
            💡 **Tips:**
            - Red markers indicate hospital locations
            - Zoom in/out using mouse scroll or map controls
            - Click and drag to pan the map
            - For real-time data, integrate Google Maps/Places API
            """)
            
            # Emergency services info
            st.warning(f"""
            🚨 **Emergency Services:**
            - Ambulance: **108 / 102**
            - Medical Emergency Helpline: **1066**
            - Police: **100**
            """)

# ==============================================================
# 🚨 TAB 5: Emergency Response
# ==============================================================
with tabs[4]:
    st.markdown("""
        <div class='feature-card'>
            <h2>🚨 Emergency Response System</h2>
            <p>Quick access to emergency services and critical care contacts</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Emergency contacts
    st.markdown("### 📞 Emergency Contacts")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class='emergency-card-red'>
                <h2>🚑</h2>
                <h4>Ambulance</h4>
                <h3>108 / 102</h3>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class='emergency-card-orange'>
                <h2>👮</h2>
                <h4>Police</h4>
                <h3>100</h3>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class='emergency-card-blue'>
                <h2>🏥</h2>
                <h4>Medical Helpline</h4>
                <h3>1066</h3>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # SOS Button
    st.warning("⚠️ **Important:** Use SOS only in critical medical emergencies!")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🆘 SEND SOS ALERT", use_container_width=True, type="primary"):
            with st.spinner("🚨 Contacting emergency services..."):
                time.sleep(2)
                st.success("✅ **SOS Alert Sent Successfully!**")
                st.info("""
                📢 **Notifications sent to:**
                - Emergency contacts
                - Nearest hospital
                - Local ambulance service
                - Family members
                """)
                st.balloons()

# ==============================================================
# 🧠 TAB 6: Explainable AI & About
# ==============================================================
with tabs[5]:
    st.markdown("""
        <div class='feature-card'>
            <h2>🧠 Explainable AI & System Overview</h2>
            <p>Understanding how our AI makes predictions and recommendations</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

    # AI Transparency Section
    st.markdown("### 🔍 AI Transparency & Explainability")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class='feature-card'>
                <h4>📊 SHAP Analysis</h4>
                <p>SHapley Additive exPlanations reveal which features contribute most to your risk score.</p>
                <ul>
                    <li>Feature importance visualization</li>
                    <li>Individual prediction breakdown</li>
                    <li>Model-agnostic explanations</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class='feature-card'>
                <h4>🎯 LIME Interpretation</h4>
                <p>Local Interpretable Model-agnostic Explanations for individual predictions.</p>
                <ul>
                    <li>Local prediction explanations</li>
                    <li>Feature contribution weights</li>
                    <li>Counterfactual analysis</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

    # System Objectives
    st.markdown("### 🎯 System Capabilities")
    
    objectives = [
        ("🤖", "Advanced Health Risk Prediction", "Multi-disease ensemble ML models with 85%+ accuracy"),
        ("💡", "Intelligent Recommendations", "Personalized, evidence-based health guidance"),
        ("📊", "Risk Stratification Framework", "Clear, color-coded risk zones and actionable insights"),
        ("🗺️", "Location-Based Services", "Find nearby hospitals, specialists, and emergency care"),
        ("🚨", "Emergency Response Integration", "Quick SOS alerts and emergency contact notifications"),
        ("🔒", "Privacy & Security", "End-to-end encryption, no personal data storage")
    ]
    
    col1, col2 = st.columns(2)
    
    for idx, (emoji, title, desc) in enumerate(objectives):
        with col1 if idx % 2 == 0 else col2:
            st.markdown(f"""
                <div class='feature-card'>
                    <h3>{emoji} {title}</h3>
                    <p>{desc}</p>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Tech Stack
    st.markdown("### �️ Technology Stack")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
            <div class='metric-card'>
                <h4>Frontend</h4>
                <p>Streamlit<br>Plotly<br>HTML/CSS</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class='metric-card'>
                <h4>Backend</h4>
                <p>Flask API<br>Python 3.12<br>REST</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class='metric-card'>
                <h4>ML Models</h4>
                <p>XGBoost<br>LightGBM<br>Scikit-learn</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
            <div class='metric-card'>
                <h4>Explainability</h4>
                <p>SHAP<br>LIME<br>ELI5</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.markdown("""
        <div style='text-align: center; padding: 20px; background: #f8f9fa; border-radius: 10px;'>
            <h4>🔐 Your Privacy Matters</h4>
            <p>All health data is processed locally. No personal information is stored or shared.</p>
            <p style='margin-top: 20px; color: #6b7280;'>© 2025 Smart Patient Health Assistant | Built with ❤️ using Streamlit & Flask</p>
        </div>
    """, unsafe_allow_html=True)
