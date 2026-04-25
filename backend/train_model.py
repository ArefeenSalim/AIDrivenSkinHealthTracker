import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder

DATA_PATH = "skin_data.csv"
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

TARGET_COLUMN = "riskLevel"


def load_data():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(
            f"{DATA_PATH} not found. Run generate_dataset.py first."
        )

    df = pd.read_csv(DATA_PATH)
    return df


def preprocess_data(df):
    encoder = LabelEncoder()

    df["skinConditionType"] = encoder.fit_transform(
        df["skinConditionType"]
    )

    X = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]

    return X, y, encoder


def train_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    model = RandomForestClassifier(
        n_estimators=150,
        random_state=42,
        max_depth=12,
    )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    print("\nTraining complete.")
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")

    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    return model


def main():
    print("Loading dataset...")
    df = load_data()

    print("Preprocessing data...")
    X, y, encoder = preprocess_data(df)

    print(f"Rows available for training: {len(X)}")

    print("Training Random Forest model...")
    model = train_model(X, y)

    print("\nSaving model...")
    joblib.dump(model, MODEL_PATH)
    joblib.dump(encoder, ENCODER_PATH)

    print(f"Model saved to: {MODEL_PATH}")
    print(f"Encoder saved to: {ENCODER_PATH}")


if __name__ == "__main__":
    main()