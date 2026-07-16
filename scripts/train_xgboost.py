import json
import os
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import xgboost as xgb

from infrastructure.ml.feature_engineering import build_feature_pipeline
from infrastructure.ml.model_evaluation import calculate_mae, calculate_mape, calculate_wape

FEATURE_COLUMNS = [
    "lag_1", "lag_7", "lag_14",
    "rolling_mean_7", "rolling_mean_30",
    "day_of_week", "is_weekend", "month",
    "day_of_week_sin", "day_of_week_cos",
    "month_sin", "month_cos",
    "is_promo",
]
TARGET_COLUMN = "quantity_sold"
VALIDATION_DAYS = 60  
MODEL_VERSION = "xgboost-v1"


def load_and_prepare_data() -> pd.DataFrame:
    df = pd.read_csv("data/raw/train.csv")
    df["transaction_date"] = pd.to_datetime(df["transaction_date"])
    df = build_feature_pipeline(df)
    df = df.dropna(subset=FEATURE_COLUMNS)
    return df


def time_based_split(df: pd.DataFrame):
    df = df.sort_values("transaction_date")
    cutoff_date = df["transaction_date"].max() - pd.Timedelta(days=VALIDATION_DAYS)
    train_df = df[df["transaction_date"] <= cutoff_date]
    val_df = df[df["transaction_date"] > cutoff_date]
    return train_df, val_df


def train_model(train_df: pd.DataFrame) -> xgb.Booster:
    dtrain = xgb.DMatrix(train_df[FEATURE_COLUMNS], label=train_df[TARGET_COLUMN])

    params = {
        "objective": "reg:squarederror",
        "max_depth": 5,
        "eta": 0.05,
        "subsample": 0.8,
        "colsample_bytree": 0.8,
    }
    model = xgb.train(params, dtrain, num_boost_round=200)
    return model


def evaluate(model: xgb.Booster, val_df: pd.DataFrame) -> dict:
    dval = xgb.DMatrix(val_df[FEATURE_COLUMNS])
    predictions = model.predict(dval)
    predictions = predictions.clip(min=0)  

    mae = calculate_mae(val_df[TARGET_COLUMN], predictions)
    mape = calculate_mape(val_df[TARGET_COLUMN], predictions)
    wape = calculate_wape(val_df[TARGET_COLUMN], predictions)

    baseline_pred = val_df["lag_7"]
    baseline_mae = calculate_mae(val_df[TARGET_COLUMN], baseline_pred)
    baseline_mape = calculate_mape(val_df[TARGET_COLUMN], baseline_pred)
    baseline_wape = calculate_wape(val_df[TARGET_COLUMN], baseline_pred)

    return {
        "xgboost_mae": round(mae, 3),
        "xgboost_mape": round(mape, 3),
        "xgboost_wape": round(wape, 3),
        "baseline_mae": round(baseline_mae, 3),
        "baseline_mape": round(baseline_mape, 3),
        "baseline_wape": round(baseline_wape, 3),
        "improvement_over_baseline_pct": round((1 - mae / baseline_mae) * 100, 2)
    }


def main():
    print("Memuat & menyiapkan data...")
    df = load_and_prepare_data()
    train_df, val_df = time_based_split(df)
    print(f"Data training: {len(train_df)} baris | Data validasi: {len(val_df)} baris")

    print("Training model...")
    model = train_model(train_df)

    print("Evaluasi...")
    metrics = evaluate(model, val_df)
    print(json.dumps(metrics, indent=2))

    # Simpan model + metadata
    import os
    os.makedirs("infrastructure/ml/model_registry", exist_ok=True)
    model_path = f"infrastructure/ml/model_registry/{MODEL_VERSION}.json"
    model.save_model(model_path)

    metadata = {
        "model_version": MODEL_VERSION,
        "trained_on": date.today().isoformat(),
        "feature_columns": FEATURE_COLUMNS,
        "target_column": TARGET_COLUMN,
        "metrics": metrics,
    }
    metadata_path = f"infrastructure/ml/model_registry/{MODEL_VERSION}_metadata.json"
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)

    print(f"\nModel disimpan di: {model_path}")
    print(f"Metadata disimpan di: {metadata_path}")


if __name__ == "__main__":
    main()
