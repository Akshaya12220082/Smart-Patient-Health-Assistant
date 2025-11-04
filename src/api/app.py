from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
from src.utils.config import load_config

app = Flask(__name__)
CORS(app)

# Load config
config = load_config()

# Load models
models = {
    "diabetes": joblib.load(config["ml_models"]["diabetes"]),
    "heart": joblib.load(config["ml_models"]["heart"]),
    "kidney": joblib.load(config["ml_models"]["kidney"])
}

@app.route("/")
def home():
    return jsonify({"message": "Smart Patient Health Assistant API is running!"})

@app.route("/predict/<disease>", methods=["POST"])
def predict(disease):
    try:
        data = request.get_json()
        if disease not in models:
            return jsonify({"error": "Invalid disease type"}), 400

        model = models[disease]
        features = np.array(list(data.values())).reshape(1, -1)
        prediction = model.predict_proba(features)[0][1] * 100

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
            "zone": zone
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
