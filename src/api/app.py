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
        # Load model dictionaries and extract pipelines
        for disease in ["diabetes", "heart", "kidney"]:
            model_data = joblib.load(config["ml_models"][disease])
            # Check if it's a dict with pipeline key or just the model
            if isinstance(model_data, dict) and "pipeline" in model_data:
                models[disease] = model_data["pipeline"]
            else:
                # If it's not a dict, assume it's the model directly
                models[disease] = model_data
        print("✅ Models loaded successfully")
except Exception as e:
    print(f"❌ Error loading models: {e}")
    import traceback
    traceback.print_exc()

# Expected features for each disease
EXPECTED_FEATURES = {
    "diabetes": ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness", 
                 "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"],
    "heart": ["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", 
              "thalach", "exang", "oldpeak", "slope", "ca", "thal"],
    "kidney": ["age", "bp", "sg", "al", "su", "rbc", "pc", "pcc", "ba", 
               "bgr", "bu", "sc", "sod", "pot", "hemo", "pcv", "wc", "rc",
               "htn", "dm", "cad", "appet", "pe", "ane"]
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
            "GET /hospitals/<disease>?lat=X&lng=Y&radius=5000",
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
        
        # Extract features in correct order and create DataFrame
        features = [data.get(f, 0) for f in expected]
        
        # Validate feature types (all should be numeric)
        try:
            features = [float(f) for f in features]
        except (ValueError, TypeError):
            return jsonify({
                "error": "All features must be numeric values"
            }), 400
        
        # Create DataFrame with proper column names (required by sklearn pipeline)
        features_df = pd.DataFrame([features], columns=expected)
        
        # Check for NaN or infinite values
        if features_df.isna().any().any() or np.isinf(features_df.values).any():
            return jsonify({
                "error": "Invalid input: contains NaN or infinite values"
            }), 400
        
        # Make prediction
        model = models[disease]
        
        # Check if model has predict_proba method
        if hasattr(model, 'predict_proba'):
            prediction_proba = model.predict_proba(features_df)[0][1]
        else:
            # Fallback to predict
            prediction_proba = model.predict(features_df)[0]
        
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

@app.route("/hospitals/<disease>", methods=["GET"])
def find_hospitals(disease):
    """Find nearby hospitals/clinics for a specific disease"""
    try:
        # Get location parameters
        lat = request.args.get('lat', type=float)
        lng = request.args.get('lng', type=float)
        radius = request.args.get('radius', type=int, default=5000)
        
        if lat is None or lng is None:
            return jsonify({
                "error": "lat and lng parameters required"
            }), 400
        
        if disease not in ["diabetes", "heart", "kidney"]:
            return jsonify({
                "error": "Invalid disease type. Use: diabetes, heart, or kidney"
            }), 400
        
        # Try OpenStreetMap first (free, no API key needed)
        try:
            from src.services.osm_maps import find_hospitals_nearby_osm, format_osm_results_for_api
            
            print(f"🗺️  Using OpenStreetMap to find hospitals...")
            hospitals_raw = find_hospitals_nearby_osm(lat, lng, disease, radius)
            hospitals = format_osm_results_for_api(hospitals_raw)
            
            return jsonify({
                "disease": disease,
                "location": {"lat": lat, "lng": lng},
                "radius_meters": radius,
                "count": len(hospitals),
                "hospitals": hospitals,
                "source": "OpenStreetMap"
            })
        
        except Exception as osm_error:
            print(f"⚠️  OpenStreetMap failed: {osm_error}")
            
            # Fallback to Google Maps if available
            try:
                from src.services.maps import find_hospitals_nearby
                
                print(f"🔄 Falling back to Google Maps...")
                hospitals = find_hospitals_nearby(lat, lng, disease, radius)
                
                return jsonify({
                    "disease": disease,
                    "location": {"lat": lat, "lng": lng},
                    "radius_meters": radius,
                    "count": len(hospitals),
                    "hospitals": hospitals,
                    "source": "Google Maps"
                })
            
            except ValueError as ve:
                # Google Maps API not configured
                return jsonify({
                    "error": "No map service available",
                    "details": f"OpenStreetMap failed: {str(osm_error)}. Google Maps not configured: {str(ve)}",
                    "instructions": "OpenStreetMap is temporarily unavailable. Please try again later or configure Google Maps API."
                }), 503
    
    except Exception as e:
        return jsonify({
            "error": "Failed to find hospitals",
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
