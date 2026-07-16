import json

import numpy as np
import pandas as pd
import xgboost as xgb

from domain.entities.forecast_result import ForecastResult
from domain.interfaces.forecast_strategy import ForecastStrategy
from infrastructure.ml.feature_engineering import build_feature_pipeline


class XGBoostStrategy(ForecastStrategy):

    def __init__(self, model_path: str, metadata_path: str):
        self.model = xgb.Booster()
        self.model.load_model(model_path)

        with open(metadata_path) as f:
            metadata = json.load(f)
        self.feature_columns = metadata["feature_columns"]
        self.model_version = metadata["model_version"]

    def predict(self, product_id: str, historical_data: list[dict]) -> ForecastResult:
        df = pd.DataFrame(historical_data)
        df["transaction_date"] = pd.to_datetime(df["transaction_date"])
        df["product_id"] = product_id
        if "is_promo" not in df.columns:
            df["is_promo"] = 0

        last_date = df["transaction_date"].max()
        next_date = last_date + pd.Timedelta(days=1)
        placeholder = pd.DataFrame([{
            "transaction_date": next_date,
            "product_id": product_id,
            "quantity_sold": np.nan,
            "is_promo": 0,
        }])
        df_with_placeholder = pd.concat([df, placeholder], ignore_index=True)

        featured = build_feature_pipeline(df_with_placeholder)
        latest_row = featured.iloc[[-1]]

        X = latest_row[self.feature_columns]
        dmatrix = xgb.DMatrix(X)
        prediction = float(self.model.predict(dmatrix)[0])
        prediction = max(0.0, prediction)  

        return ForecastResult(
            product_id=product_id,
            predicted_demand=prediction,
            model_version=self.model_version,
            forecast_date=next_date.date(),
        )
