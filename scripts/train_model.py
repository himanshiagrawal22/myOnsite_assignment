import pandas as pd
import numpy as np
import joblib

from pathlib import Path

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# --------------------------------------------------
# 1. Paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

NIGHTLIGHT_PATH = BASE_DIR / "data" / "Indian_City_NightLights.csv"
MODEL_PATH = BASE_DIR / "models" / "population_model.pkl"
METRICS_PATH = BASE_DIR / "models" / "model_metrics.json"


# --------------------------------------------------
# 2. Load dataset
# --------------------------------------------------

print("Loading dataset...")

df = pd.read_csv(NIGHTLIGHT_PATH)

print(f"Dataset shape: {df.shape}")


# --------------------------------------------------
# 3. Create derived features
# --------------------------------------------------

df["Brightness_Range"] = (
    df["average_masked_max"] -
    df["average_masked_min"]
)

df["Brightness_Ratio"] = (
    df["average_masked_max"] /
    (df["average_masked_mean"] + 1e-6)
)

df["Brightness_Product"] = (
    df["average_masked_mean"] *
    df["average_masked_max"]
)


# --------------------------------------------------
# 4. Select features
# --------------------------------------------------

FEATURES = [
    "average_masked_mean",
    "average_masked_max",
    "average_masked_min",
    "average_masked_stdDev",
    "Brightness_Range",
    "Brightness_Ratio",
    "Brightness_Product"
]


TARGET = "Population"


# --------------------------------------------------
# 5. Remove missing values
# --------------------------------------------------

df = df.dropna(
    subset=FEATURES + [TARGET]
)


X = df[FEATURES]
y = df[TARGET]


print(f"Training samples: {len(df)}")
print(f"Features: {FEATURES}")


# --------------------------------------------------
# 6. Split data
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# --------------------------------------------------
# 7. Train Random Forest
# --------------------------------------------------

print("Training Random Forest model...")

model = RandomForestRegressor(
    n_estimators=200,
    random_state=42,
    max_depth=None
)

model.fit(
    X_train,
    y_train
)


# --------------------------------------------------
# 8. Evaluate model
# --------------------------------------------------

predictions = model.predict(X_test)

mae = mean_absolute_error(
    y_test,
    predictions
)

rmse = np.sqrt(
    mean_squared_error(
        y_test,
        predictions
    )
)

r2 = r2_score(
    y_test,
    predictions
)


print("\nModel Performance")
print("-------------------------")
print(f"MAE  : {mae:.2f}")
print(f"RMSE : {rmse:.2f}")
print(f"R²   : {r2:.4f}")


# --------------------------------------------------
# 9. Save model
# --------------------------------------------------

MODEL_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)

joblib.dump(
    model,
    MODEL_PATH
)


# --------------------------------------------------
# 10. Save metrics
# --------------------------------------------------

import json

metrics = {
    "MAE": float(mae),
    "RMSE": float(rmse),
    "R2": float(r2),
    "training_samples": int(len(df)),
    "features": FEATURES
}

with open(
    METRICS_PATH,
    "w"
) as file:

    json.dump(
        metrics,
        file,
        indent=4
    )


print("\nModel saved successfully!")
print(f"Model: {MODEL_PATH}")
print(f"Metrics: {METRICS_PATH}")