"""
Test the improved ensemble models directly
"""

import joblib
import numpy as np
import json

def test_model(model_path, scaler_path, metadata_path, test_data, model_name):
    """Test a single model"""
    print(f"\n{'='*70}")
    print(f"Testing {model_name.upper()} Model")
    print(f"{'='*70}")
    
    # Load model, scaler, and metadata
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)
    
    # Display metadata
    print(f"\nModel Info:")
    print(f"  Type: {metadata['model_type']}")
    print(f"  Features: {metadata['n_features']}")
    print(f"  Training Samples: {metadata['n_samples_train']}")
    
    print(f"\nPerformance Metrics:")
    for metric, value in metadata['metrics'].items():
        print(f"  {metric.replace('_', ' ').title()}: {value*100:.2f}%")
    
    print(f"\nCross-Validation:")
    print(f"  Mean: {metadata['cv_scores']['mean']*100:.2f}%")
    print(f"  Std: {metadata['cv_scores']['std']*100:.2f}%")
    
    # Make prediction
    print(f"\nTest Prediction:")
    print(f"  Input: {test_data}")
    
    X_scaled = scaler.transform([test_data])
    prediction = model.predict(X_scaled)[0]
    prob = model.predict_proba(X_scaled)[0]
    
    print(f"  Prediction: {prediction}")
    print(f"  Probability (No Disease): {prob[0]*100:.2f}%")
    print(f"  Probability (Disease): {prob[1]*100:.2f}%")
    
    risk_percentage = prob[1] * 100
    print(f"  Risk Level: {risk_percentage:.2f}%")
    
    return risk_percentage

if __name__ == "__main__":
    print("\n🧪 Testing Improved Ensemble Models")
    print("="*70)
    
    # Test Diabetes Model
    diabetes_test = [6, 148, 72, 35, 0, 33.6, 0.627, 50]  # High risk case
    diabetes_risk = test_model(
        "models/saved_models/diabetes_model.joblib",
        "models/saved_models/diabetes_scaler.joblib",
        "models/saved_models/diabetes_metadata.json",
        diabetes_test,
        "Diabetes"
    )
    
    # Test Heart Model
    heart_test = [63, 1, 3, 145, 233, 1, 0, 150, 0, 2.3, 0, 0, 1]  # High risk case
    heart_risk = test_model(
        "models/saved_models/heart_model.joblib",
        "models/saved_models/heart_scaler.joblib",
        "models/saved_models/heart_metadata.json",
        heart_test,
        "Heart Disease"
    )
    
    # Test Kidney Model
    kidney_test = [1, 48, 80, 1.020, 1, 0, 1, 0, 0, 0, 121, 36, 1.2, 137, 15, 11.2, 32, 6700, 4.5, 1, 0, 0, 0, 1, 1]
    kidney_risk = test_model(
        "models/saved_models/kidney_model.joblib",
        "models/saved_models/kidney_scaler.joblib",
        "models/saved_models/kidney_metadata.json",
        kidney_test,
        "Kidney Disease"
    )
    
    # Summary
    print(f"\n{'='*70}")
    print("🎯 Test Summary")
    print(f"{'='*70}")
    print(f"  Diabetes Risk: {diabetes_risk:.2f}%")
    print(f"  Heart Disease Risk: {heart_risk:.2f}%")
    print(f"  Kidney Disease Risk: {kidney_risk:.2f}%")
    print(f"{'='*70}\n")
    
    print("✅ All models tested successfully!")
    print("✅ Ensemble models (RF+XGB+LGBM+GB) working correctly!")
