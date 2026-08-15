import joblib
from pathlib import Path
import pandas as pd


# --------------------------------------------------
# Model path
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "population_model.pkl"


# --------------------------------------------------
# Load model
# --------------------------------------------------

def load_population_model():

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model file not found: {MODEL_PATH}"
        )

    return joblib.load(MODEL_PATH)


# --------------------------------------------------
# Predict population
# --------------------------------------------------

def predict_population(features: dict):

    model = load_population_model()

    # Keep the feature order exactly the same
    # as the training model

    feature_names = [
        "average_masked_mean",
        "average_masked_max",
        "average_masked_min",
        "average_masked_stdDev",
        "Brightness_Range",
        "Brightness_Ratio",
        "Brightness_Product"
    ]

    # Convert input dictionary into DataFrame
    input_data = pd.DataFrame(
        [[features[name] for name in feature_names]],
        columns=feature_names
    )

    # Make prediction
    prediction = model.predict(input_data)[0]

    return {
        "estimated_population": round(float(prediction)),
        "features_used": feature_names
    }