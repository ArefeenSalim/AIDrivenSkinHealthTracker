import joblib

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allows the mobile app to send requests to this Flask backend

MODEL_PATH = "flare_risk_model.pkl"
ENCODER_PATH = "skin_condition_encoder.pkl"

print("Loading ML model...")
model = joblib.load(MODEL_PATH)  # loads the trained Random Forest model
condition_map = joblib.load(ENCODER_PATH)  # loads the encoded skin condition values
print("ML model loaded successfully.")


@app.route("/")
def home():
    # simple test route to check that the backend is running
    return jsonify({
        "message": "AI Skin Health Flask API is running"
    })


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()  # gets the daily log data sent from the mobile app

        skin_condition = data.get("skinConditionType", "").lower().strip()

        # checks that the selected skin condition is one the model understands
        if skin_condition not in condition_map:
            return jsonify({
                "error": "Invalid skinConditionType",
                "allowedValues": list(condition_map.keys())
            }), 400

        # formats the app input into the same feature order used during model training
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

        prediction = model.predict(input_data)[0]  # predicts Low, Medium or High risk
        probabilities = model.predict_proba(input_data)[0]  # gets confidence scores for each risk level

        probability_dict = {}

        # converts model probabilities into a readable JSON format for the app
        for label, probability in zip(model.classes_, probabilities):
            probability_dict[label] = round(float(probability), 4)

        confidence = probability_dict[prediction]  # confidence for the predicted risk level

        return jsonify({
            "riskLevel": prediction,
            "confidence": confidence,
            "probabilities": probability_dict
        })

    except Exception as error:
        # returns an error response if something goes wrong during prediction
        return jsonify({
            "error": str(error)
        }), 500


if __name__ == "__main__":
    # runs the Flask API locally on port 5001
    app.run(host="0.0.0.0", port=5001, debug=True)