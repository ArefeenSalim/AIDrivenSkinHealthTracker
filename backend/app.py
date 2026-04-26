import joblib

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

MODEL_PATH = "flare_risk_model.pkl"
ENCODER_PATH = "skin_condition_encoder.pkl"

print("Loading ML model...")
model = joblib.load(MODEL_PATH)
condition_map = joblib.load(ENCODER_PATH)
print("ML model loaded successfully.")


@app.route("/")
def home():
    return jsonify({
        "message": "AI Skin Health Flask API is running"
    })


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        skin_condition = data.get("skinConditionType", "").lower().strip()

        if skin_condition not in condition_map:
            return jsonify({
                "error": "Invalid skinConditionType",
                "allowedValues": list(condition_map.keys())
            }), 400

        input_data = [[
            condition_map[skin_condition],
            float(data.get("sleepHours")),
            int(data.get("stressLevel")),
            float(data.get("waterIntakeLitres")),
            int(data.get("dietQuality")),
            int(data.get("symptomSeverity")),
            float(data.get("temperature")),
            float(data.get("humidity")),
        ]]

        prediction = model.predict(input_data)[0]
        probabilities = model.predict_proba(input_data)[0]

        probability_dict = {}

        for label, probability in zip(model.classes_, probabilities):
            probability_dict[label] = round(float(probability), 4)

        confidence = probability_dict[prediction]

        return jsonify({
            "riskLevel": prediction,
            "confidence": confidence,
            "probabilities": probability_dict
        })

    except Exception as error:
        return jsonify({
            "error": str(error)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)