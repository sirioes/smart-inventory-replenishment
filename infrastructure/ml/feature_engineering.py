import numpy as np
import pandas as pd


def add_lag_features(
    df: pd.DataFrame, group_col: str, target_col: str, lags: list[int]
) -> pd.DataFrame:
    
    df = df.sort_values([group_col, "transaction_date"]).copy()
    for lag in lags:
        df[f"lag_{lag}"] = df.groupby(group_col)[target_col].shift(lag)
    return df


def add_rolling_features(
    df: pd.DataFrame, group_col: str, target_col: str, windows: list[int]
) -> pd.DataFrame:
    
    df = df.sort_values([group_col, "transaction_date"]).copy()
    for window in windows:
        df[f"rolling_mean_{window}"] = df.groupby(group_col)[target_col].transform(
            lambda s: s.shift(1).rolling(window=window, min_periods=1).mean()
        )
    return df


def add_calendar_features(df: pd.DataFrame, date_col: str) -> pd.DataFrame:
    df = df.copy()
    dt = pd.to_datetime(df[date_col])

    df["day_of_week"] = dt.dt.dayofweek
    df["is_weekend"] = (df["day_of_week"] >= 5).astype(int)
    df["month"] = dt.dt.month

    df["day_of_week_sin"] = np.sin(2 * np.pi * df["day_of_week"] / 7)
    df["day_of_week_cos"] = np.cos(2 * np.pi * df["day_of_week"] / 7)
    df["month_sin"] = np.sin(2 * np.pi * df["month"] / 12)
    df["month_cos"] = np.cos(2 * np.pi * df["month"] / 12)

    return df


def build_feature_pipeline(
    df: pd.DataFrame,
    group_col: str = "product_id",
    target_col: str = "quantity_sold",
    date_col: str = "transaction_date",
    lags: list[int] = [1, 7, 14],
    rolling_windows: list[int] = [7, 30],
) -> pd.DataFrame:
    df = df.sort_values([group_col, date_col]).reset_index(drop=True)
    df = add_lag_features(df, group_col, target_col, lags)
    df = add_rolling_features(df, group_col, target_col, rolling_windows)
    df = add_calendar_features(df, date_col)
    return df
