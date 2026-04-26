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

    with open(DATA_PATH, "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            condition = row["skinConditionType"].lower().strip()

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

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    print("Training fast Random Forest model...")

    model = RandomForestClassifier(
        n_estimators=5,
        max_depth=5,
        random_state=42,
        n_jobs=1,
    )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    print("\nTraining complete.")
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    joblib.dump(model, MODEL_PATH)
    joblib.dump(CONDITION_MAP, ENCODER_PATH)

    print(f"\nModel saved to: {MODEL_PATH}")
    print(f"Encoder saved to: {ENCODER_PATH}")


if __name__ == "__main__":
    main()