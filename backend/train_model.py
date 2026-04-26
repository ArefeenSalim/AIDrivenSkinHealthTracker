import csv
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

DATA_PATH = "skin_data.csv"
MODEL_PATH = "flare_risk_model.pkl"
ENCODER_PATH = "skin_condition_encoder.pkl"

CONDITION_MAP = {
    "acne": 0,
    "eczema": 1,
    "psoriasis": 2,
    "rosacea": 3,
}

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


def load_dataset():
    X = []
    y = []

    # reads the generated CSV dataset and separates inputs from the target risk label
    with open(DATA_PATH, "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            condition = row["skinConditionType"].lower().strip()

            # converts each row into the exact feature order expected by the model
            X.append([
                CONDITION_MAP[condition],
                float(row["sleepHours"]),
                int(row["stressLevel"]),
                float(row["waterIntakeLitres"]),
                int(row["dietQuality"]),
                int(row["symptomSeverity"]),
                float(row["temperature"]),
                float(row["humidity"]),
            ])

            y.append(row["riskLevel"])

    return X, y


def main():
    print("Loading dataset...")
    X, y = load_dataset()

    print(f"Rows loaded: {len(X)}")

    # splits the dataset so the model can be trained and tested separately
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    print("Training fast Random Forest model...")

    # Random Forest is used because it works well with mixed lifestyle and weather features
    model = RandomForestClassifier(
        n_estimators=5,
        max_depth=5,
        random_state=42,
        n_jobs=1,
    )

    model.fit(X_train, y_train)  # trains the model using the training data

    y_pred = model.predict(X_test)  # tests the model on unseen test data

    print("\nTraining complete.")
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    # saves the trained model and the skin condition encoding map for the Flask API
    joblib.dump(model, MODEL_PATH)
    joblib.dump(CONDITION_MAP, ENCODER_PATH)

    print(f"\nModel saved to: {MODEL_PATH}")
    print(f"Encoder saved to: {ENCODER_PATH}")


if __name__ == "__main__":
    main()