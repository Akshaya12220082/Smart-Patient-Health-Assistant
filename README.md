# 🏥 Smart Patient Health Assistant

> **AI-Driven Healthcare System for Preventive Care and Emergency Response**

An intelligent healthcare assistant that goes beyond traditional disease prediction to provide comprehensive health guidance, personalized recommendations, and emergency response capabilities.

---

## 🌟 Overview

The **Smart Patient Health Assistant** is a comprehensive AI-powered healthcare system designed to address critical gaps in healthcare delivery, particularly in resource-constrained environments. The system combines advanced machine learning algorithms with practical healthcare guidance to provide:

- **Multi-disease risk prediction** (Diabetes, Heart Disease, Kidney Disease)
- **Intelligent risk stratification** (Green/Yellow/Red zones)
- **Personalized health recommendations**
- **Location-based hospital finder**
- **Emergency response integration**

### 🎯 Key Objectives

1. **Advanced Health Risk Prediction** - Achieve ≥85% accuracy across all disease categories
2. **Intelligent Recommendations** - Evidence-based suggestions following WHO/CDC guidelines
3. **Risk Stratification** - Three-tier classification with clear action protocols
4. **Location Services** - Integration with Google Maps API for nearest hospitals
5. **Emergency Response** - SOS functionality with automatic contact notification

---

## ✨ Features

### 🔮 Disease Prediction

- **Multi-disease models**: Diabetes, Cardiovascular Disease, Chronic Kidney Disease
- **Ensemble methods**: Combines multiple ML algorithms for improved accuracy
- **Explainable AI**: SHAP and LIME integration for model transparency

### 📊 Risk Stratification

- **Green Zone (0-30)**: Low risk - Preventive measures recommended
- **Yellow Zone (31-70)**: Moderate risk - Doctor consultation advised
- **Red Zone (71-100)**: High risk - Immediate medical attention required

### 💡 Personalized Recommendations

- Lifestyle modifications (diet, exercise, sleep)
- Safe OTC medication suggestions for mild conditions
- Health monitoring parameters and frequency
- When to seek professional medical help

### 🗺️ Location-Based Services

- Find nearest hospitals based on condition type
- Specialized facility recommendations
- Distance, ratings, and contact information
- Direct navigation integration

### 🚨 Emergency Response

- Manual SOS button activation
- Automatic emergency detection based on critical risk scores
- Instant emergency contact notification
- Hospital alert system with patient medical summary

---

## � Quick Start

### Prerequisites

- Python 3.9 or higher
- pip package manager
- Git

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/Akshaya12220082/Smart-Patient-Health-Assistant.git
   cd Smart-Patient-Health-Assistant
   ```

2. **Create a virtual environment (recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   Copy the example environment file:

   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your API keys:

   ```bash
   GOOGLE_MAPS_API_KEY=your_actual_google_maps_key
   TWILIO_ACCOUNT_SID=your_twilio_sid
   TWILIO_AUTH_TOKEN=your_twilio_token
   TWILIO_PHONE_NUMBER=your_twilio_number
   ```

5. **Create config file from template**
   ```bash
   cp config/config.yaml.template config/config.yaml
   ```

### Running the Application

The application consists of two parts that need to run simultaneously:

#### 1. Start the Flask API Backend

Open a terminal and run:

```bash
python -m src.api.app
```

The API will start on `http://127.0.0.1:5000`

You should see:

```
✅ Models loaded successfully
 * Running on http://127.0.0.1:5000
```

#### 2. Start the Streamlit Frontend

Open a **new terminal** (keep the API running) and run:

```bash
streamlit run app.py
```

The web interface will open automatically at `http://localhost:8501`

---

## 🧪 Testing

Run the test suite:

```bash
pytest tests/ -v
```

Run tests with coverage:

```bash
pytest tests/ --cov=src --cov-report=html
```

View coverage report:

```bash
open htmlcov/index.html  # On macOS
# On Linux: xdg-open htmlcov/index.html
# On Windows: start htmlcov/index.html
```

---

## 📊 Usage Guide

### 1. Disease Prediction

1. Navigate to the **Disease Prediction** tab
2. Select disease type (Diabetes, Heart Disease, or Kidney Disease)
3. Click "View Sample Data Format" to see required columns
4. Upload your CSV file with patient data
5. Click "Predict Now" to get risk assessment

**Sample Data Files:**

- Diabetes: `data/raw/diabetes.csv`
- Heart: `data/raw/heart.csv`
- Kidney: `data/raw/kidney.csv`

### 2. Risk Stratification

View your risk zone classification:

- 🟢 **Green (0-30%)**: Low risk - maintain healthy habits
- 🟡 **Yellow (31-70%)**: Moderate risk - consult doctor
- 🔴 **Red (71-100%)**: High risk - seek immediate care

### 3. Personalized Recommendations

After making a prediction, get AI-generated recommendations:

- Lifestyle modifications
- Dietary guidelines
- Exercise suggestions
- Medical checkup schedules

### 4. Hospital Finder

Find nearby hospitals based on:

- Your location
- Condition type
- Specialty requirements

### 5. Emergency Response

For critical situations:

- Click "Send SOS Alert"
- Emergency contacts are notified via SMS and email
- Nearest hospital receives patient summary

---

## 🔧 Configuration

### Environment Variables

The application uses environment variables for sensitive data. Set these in your `.env` file:

| Variable              | Description                             | Required |
| --------------------- | --------------------------------------- | -------- |
| `GOOGLE_MAPS_API_KEY` | Google Maps API key for hospital finder | Optional |
| `TWILIO_ACCOUNT_SID`  | Twilio account SID for SMS              | Optional |
| `TWILIO_AUTH_TOKEN`   | Twilio auth token                       | Optional |
| `TWILIO_PHONE_NUMBER` | Twilio phone number                     | Optional |
| `SMTP_HOST`           | SMTP server for emails                  | Optional |
| `SMTP_USERNAME`       | SMTP username                           | Optional |
| `SMTP_PASSWORD`       | SMTP password                           | Optional |

### Risk Thresholds

Modify risk zone boundaries in `config/config.yaml`:

```yaml
risk_thresholds:
  green: [0, 30]
  yellow: [31, 70]
  red: [71, 100]
```

---

## 🏗️ Project Structure

```
Smart-Patient-Health-Assistant/
├── app.py                      # Streamlit frontend
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── config/
│   ├── config.yaml.template   # Configuration template
│   └── config.yaml            # Your config (gitignored)
├── data/
│   └── raw/                   # Training datasets
│       ├── diabetes.csv
│       ├── heart.csv
│       └── kidney.csv
├── models/
│   └── saved_models/          # Trained ML models
│       ├── diabetes_model.joblib
│       ├── heart_model.joblib
│       └── kidney_model.joblib
├── src/
│   ├── api/
│   │   └── app.py            # Flask REST API
│   ├── models/
│   │   ├── trainer.py        # Model training utilities
│   │   └── explain.py        # SHAP explanations
│   ├── recommendation/
│   │   └── engine.py         # Recommendation logic
│   ├── services/
│   │   ├── maps.py           # Google Maps integration
│   │   └── notify.py         # Twilio/Email notifications
│   └── utils/
│       └── config.py         # Configuration loader
└── tests/
    ├── test_api.py           # API tests
    ├── test_recommendations.py
    ├── test_trainer.py
    └── test_config.py
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 API Documentation

### Endpoints

#### `GET /`

Health check - Returns API status

#### `GET /health`

Detailed health check with loaded models info

#### `POST /predict/<disease>`

Make a prediction for a specific disease

**Parameters:**

- `disease`: One of `diabetes`, `heart`, `kidney`

**Request Body (JSON):**

```json
{
  "Pregnancies": 6,
  "Glucose": 148,
  "BloodPressure": 72,
  "SkinThickness": 35,
  "Insulin": 0,
  "BMI": 33.6,
  "DiabetesPedigreeFunction": 0.627,
  "Age": 50
}
```

**Response:**

```json
{
  "disease": "diabetes",
  "risk_score": 68.5,
  "zone": "Yellow",
  "features_used": ["Pregnancies", "Glucose", ...]
}
```

#### `GET /recommendations/<disease>?risk_score=<score>`

Get personalized recommendations

**Parameters:**

- `disease`: One of `diabetes`, `heart`, `kidney`
- `risk_score`: Float between 0-100

**Response:**

```json
{
  "condition": "diabetes",
  "risk_score": 68.5,
  "risk_band": "yellow",
  "recommendations": [
    "Schedule a consultation with a primary care physician...",
    "Track BP, weight, and symptoms weekly...",
    ...
  ]
}
```

---

## 🔒 Security Notes

⚠️ **Important Security Reminders:**

1. **Never commit secrets** to version control
2. **Rotate API keys** if accidentally exposed
3. **Use environment variables** for all sensitive data
4. **Keep `.env` and `config/config.yaml`** in `.gitignore`
5. **Use HTTPS** in production
6. **Implement authentication** for production deployments

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👥 Team

- **Project Lead**: Your Name
- **Contributors**: See [CONTRIBUTORS.md](CONTRIBUTORS.md)

---

## 🙏 Acknowledgments

- Dataset sources: UCI Machine Learning Repository
- Medical guidelines: WHO, CDC, Indian Health Ministry
- Libraries: Scikit-learn, Flask, Streamlit, SHAP

---

## 📧 Contact

For questions or support:

- Email: your.email@example.com
- GitHub Issues: [Create an issue](https://github.com/Akshaya12220082/Smart-Patient-Health-Assistant/issues)

---

**Built with ❤️ for better healthcare accessibility**

### Machine Learning & Data Science

- **Python 3.9+** - Primary programming language
- **Scikit-learn** - Traditional ML algorithms
- **XGBoost/LightGBM** - Gradient boosting frameworks
- **TensorFlow/PyTorch** - Deep learning models
- **Pandas/NumPy** - Data manipulation and analysis

### Web Framework & API

- **Flask/FastAPI** - Backend API development
- **SQLAlchemy** - Database ORM
- **Flask-CORS** - Cross-origin resource sharing

### Frontend & Visualization

- **Streamlit/React** - User interface
- **Matplotlib/Seaborn** - Statistical plotting
- **Plotly** - Interactive visualizations

### External APIs & Services

- **Google Maps API** - Hospital location services
- **Twilio/SMTP** - Emergency notifications

### Development Tools

- **Jupyter Notebooks** - Data exploration and analysis
- **VS Code** - Primary IDE
- **Git/GitHub** - Version control
- **pytest** - Testing framework
