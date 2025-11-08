from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import pandas as pd
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.utils.config import load_config
from src.recommendation.engine import generate_recommendations

app = Flask(__name__)
CORS(app)

# Load config
try:
    config = load_config()
except Exception as e:
    print(f"Warning: Could not load config: {e}")
    config = None

# Load models
models = {}
scalers = {}

try:
    if config:
        models = {
            "diabetes": joblib.load(config["ml_models"]["diabetes"]),
            "heart": joblib.load(config["ml_models"]["heart"]),
            "kidney": joblib.load(config["ml_models"]["kidney"])
        }
        print("✅ Models loaded successfully")
except Exception as e:
    print(f"❌ Error loading models: {e}")

# Expected features for each disease
EXPECTED_FEATURES = {
    "diabetes": ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness", 
                 "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"],
    "heart": ["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", 
              "thalach", "exang", "oldpeak", "slope", "ca", "thal"],
    "kidney": ["age", "bp", "sg", "al", "su", "bgr", "bu", "sc", "sod", 
               "pot", "hemo", "pcv", "wc", "rc"]
}

@app.route("/")
def home():
    return jsonify({
        "message": "Smart Patient Health Assistant API is running!",
        "version": "1.0",
        "available_endpoints": [
            "GET /",
            "POST /predict/<disease>",
            "GET /recommendations/<disease>",
            "GET /health"
        ]
    })

@app.route("/health")
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "models_loaded": len(models),
        "available_diseases": list(models.keys())
    })

@app.route("/predict/<disease>", methods=["POST"])
def predict(disease):
    """Predict disease risk from patient data"""
    try:
        # Validate disease type
        if disease not in models:
            return jsonify({
                "error": f"Invalid disease type. Available: {list(models.keys())}"
            }), 400
        
        # Get and validate input data
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Validate required features
        expected = EXPECTED_FEATURES.get(disease, [])
        missing_features = [f for f in expected if f not in data]
        
        if missing_features:
            return jsonify({
                "error": "Missing required features",
                "missing": missing_features,
                "expected": expected
            }), 400
        
        # Extract features in correct order
        features = [data.get(f, 0) for f in expected]
        features_array = np.array(features).reshape(1, -1)
        
        # Validate feature types (all should be numeric)
        try:
            features_array = features_array.astype(float)
        except (ValueError, TypeError):
            return jsonify({
                "error": "All features must be numeric values"
            }), 400
        
        # Check for NaN or infinite values
        if np.isnan(features_array).any() or np.isinf(features_array).any():
            return jsonify({
                "error": "Invalid input: contains NaN or infinite values"
            }), 400
        
        # Make prediction
        model = models[disease]
        
        # Check if model has predict_proba method
        if hasattr(model, 'predict_proba'):
            prediction_proba = model.predict_proba(features_array)[0][1]
        else:
            # Fallback to predict
            prediction_proba = model.predict(features_array)[0]
        
        # Convert to percentage and handle NaN
        if np.isnan(prediction_proba) or np.isinf(prediction_proba):
            # If prediction is invalid, use a moderate risk default
            prediction = 50.0
        else:
            prediction = float(prediction_proba) * 100
            # Clamp between 0 and 100
            prediction = max(0.0, min(100.0, prediction))
        
        # Risk zone classification
        if prediction <= 30:
            zone = "Green"
        elif prediction <= 70:
            zone = "Yellow"
        else:
            zone = "Red"
        
        return jsonify({
            "disease": disease,
            "risk_score": round(prediction, 2),
            "zone": zone,
            "features_used": expected
        })
    
    except Exception as e:
        return jsonify({
            "error": "Prediction failed",
            "details": str(e)
        }), 500

@app.route("/recommendations/<disease>", methods=["GET"])
def recommendations(disease):
    """Get personalized recommendations based on disease and risk score"""
    try:
        risk_score = request.args.get('risk_score', type=float)
        
        if risk_score is None:
            return jsonify({"error": "risk_score parameter required"}), 400
        
        if disease not in ["diabetes", "heart", "kidney"]:
            return jsonify({"error": "Invalid disease type"}), 400
        
        # Generate recommendations
        reco_data = generate_recommendations(disease, risk_score)
        
        return jsonify(reco_data)
    
    except Exception as e:
        return jsonify({
            "error": "Failed to generate recommendations",
            "details": str(e)
        }), 500

@app.errorhandler(404)
def not_found(e):
    return jsonify({
        "error": "Endpoint not found",
        "available_endpoints": [
            "GET /",
            "POST /predict/<disease>",
            "GET /recommendations/<disease>",
            "GET /health"
        ]
    }), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({
        "error": "Internal server error",
        "details": str(e)
    }), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
