import joblib
import pandas as pd

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

MODEL_PATH = "flare_risk_model.pkl"
ENCODER_PATH = "skin_condition_encoder.pkl"

FEATURE_COLUMNS = [
    "skinConditionType",
    "sleepHours",
    "stressLevel",
    "waterIntakeLitres",
    "dietQuality",
    "symptomSeverity",
    "temperature",
    "humidity",
]

model = joblib.load(MODEL_PATH)
encoder = joblib.load(ENCODER_PATH)


@app.route("/")
def home():
    return jsonify({
        "message": "AI Skin Health Flask API is running"
    })


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        skin_condition = data.get("skinConditionType")

        if skin_condition not in encoder.classes_:
            return jsonify({
                "error": "Invalid skinConditionType",
                "allowedValues": list(encoder.classes_)
            }), 400

        encoded_condition = encoder.transform([skin_condition])[0]

        input_data = pd.DataFrame([{
            "skinConditionType": encoded_condition,
            "sleepHours": float(data.get("sleepHours")),
            "stressLevel": int(data.get("stressLevel")),
            "waterIntakeLitres": float(data.get("waterIntakeLitres")),
            "dietQuality": int(data.get("dietQuality")),
            "symptomSeverity": int(data.get("symptomSeverity")),
            "temperature": float(data.get("temperature")),
            "humidity": float(data.get("humidity")),
        }], columns=FEATURE_COLUMNS)

        prediction = model.predict(input_data)[0]

        return jsonify({
            "riskLevel": prediction
        })

    except Exception as error:
        return jsonify({
            "error": str(error)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)