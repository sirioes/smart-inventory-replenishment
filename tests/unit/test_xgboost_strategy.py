import json
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
import xgboost as xgb

from infrastructure.ml.feature_engineering import build_feature_pipeline
from infrastructure.ml.xgboost_strategy import XGBoostStrategy

FEATURE_COLUMNS = [
    "lag_1", "lag_7", "lag_14",
    "rolling_mean_7", "rolling_mean_30",
    "day_of_week", "is_weekend", "month",
    "day_of_week_sin", "day_of_week_cos",
    "month_sin", "month_cos",
    "is_promo",
]


def _train_tiny_model_and_save(tmp_path: Path):
    dates = pd.date_range("2024-01-01", periods=60, freq="D")
    df = pd.DataFrame({
        "transaction_date": dates,
        "product_id": ["P1"] * 60,
        "quantity_sold": np.random.randint(10, 100, size=60),
        "is_promo": 0,
    })
    featured = build_feature_pipeline(df).dropna(subset=FEATURE_COLUMNS)

    dtrain = xgb.DMatrix(featured[FEATURE_COLUMNS], label=featured["quantity_sold"])
    model = xgb.train({"objective": "reg:squarederror", "max_depth": 2}, dtrain, num_boost_round=10)

    model_path = tmp_path / "test_model.json"
    metadata_path = tmp_path / "test_model_metadata.json"
    model.save_model(str(model_path))
    with open(metadata_path, "w") as f:
        json.dump({"model_version": "test-v0", "feature_columns": FEATURE_COLUMNS}, f)

    return str(model_path), str(metadata_path)


def test_predict_returns_forecast_result_with_valid_structure():
    with tempfile.TemporaryDirectory() as tmp_dir:
        model_path, metadata_path = _train_tiny_model_and_save(Path(tmp_dir))
        strategy = XGBoostStrategy(model_path=model_path, metadata_path=metadata_path)

        historical_data = [
            {"transaction_date": (pd.Timestamp("2024-01-01") + pd.Timedelta(days=i)).strftime("%Y-%m-%d"),
             "quantity_sold": 50, "is_promo": 0}
            for i in range(30)
        ]

        result = strategy.predict(product_id="P1", historical_data=historical_data)

        assert result.product_id == "P1"
        assert result.model_version == "test-v0"
        assert isinstance(result.predicted_demand, float)


def test_predict_never_returns_negative_demand():
    with tempfile.TemporaryDirectory() as tmp_dir:
        model_path, metadata_path = _train_tiny_model_and_save(Path(tmp_dir))
        strategy = XGBoostStrategy(model_path=model_path, metadata_path=metadata_path)

        historical_data = [
            {"transaction_date": (pd.Timestamp("2024-01-01") + pd.Timedelta(days=i)).strftime("%Y-%m-%d"),
             "quantity_sold": 0, "is_promo": 0}
            for i in range(30)
        ]

        result = strategy.predict(product_id="P1", historical_data=historical_data)
        assert result.predicted_demand >= 0.0


def test_predict_forecast_date_is_one_day_after_last_history():
    with tempfile.TemporaryDirectory() as tmp_dir:
        model_path, metadata_path = _train_tiny_model_and_save(Path(tmp_dir))
        strategy = XGBoostStrategy(model_path=model_path, metadata_path=metadata_path)

        historical_data = [
            {"transaction_date": (pd.Timestamp("2024-01-01") + pd.Timedelta(days=i)).strftime("%Y-%m-%d"),
             "quantity_sold": 50, "is_promo": 0}
            for i in range(10)
        ]
        result = strategy.predict(product_id="P1", historical_data=historical_data)
        assert result.forecast_date == pd.Timestamp("2024-01-11").date()
