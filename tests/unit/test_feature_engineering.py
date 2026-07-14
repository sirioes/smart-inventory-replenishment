import pandas as pd

from infrastructure.ml.feature_engineering import (
    add_calendar_features,
    add_lag_features,
    add_rolling_features,
    build_feature_pipeline,
)

def make_simple_df():
    dates = pd.date_range("2024-01-01", periods=10, freq="D")
    return pd.DataFrame(
        {
            "transaction_date": dates,
            "product_id": ["P1"] * 10,
            "quantity_sold": [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        }
    )


def test_lag_feature_shifts_correctly():
    df = make_simple_df()
    result = add_lag_features(df, group_col="product_id", target_col="quantity_sold", lags=[1, 7])

    # Hari ke-2 (index 1, quantity_sold=20): lag_1 harus = quantity_sold hari sebelumnya (10)
    assert result.loc[1, "lag_1"] == 10
    # Hari ke-8 (index 7, quantity_sold=80): lag_7 harus = quantity_sold 7 hari sebelumnya (10)
    assert result.loc[7, "lag_7"] == 10
    # Hari pertama (index 0) tidak punya histori, harus NaN
    assert pd.isna(result.loc[0, "lag_1"])


def test_rolling_mean_excludes_current_day():
    df = make_simple_df()
    result = add_rolling_features(df, group_col="product_id", target_col="quantity_sold", windows=[7])

    expected = sum([10, 20, 30, 40, 50, 60, 70]) / 7
    assert result.loc[7, "rolling_mean_7"] == expected


def test_rolling_mean_does_not_leak_current_value():
    df = make_simple_df()
    df_extreme = df.copy()
    df_extreme.loc[7, "quantity_sold"] = 999999  

    result_normal = add_rolling_features(df, "product_id", "quantity_sold", [7])
    result_extreme = add_rolling_features(df_extreme, "product_id", "quantity_sold", [7])

    assert result_normal.loc[7, "rolling_mean_7"] == result_extreme.loc[7, "rolling_mean_7"]


def test_calendar_features_weekend_detection():
    df = make_simple_df()  # 2024-01-01 adalah hari Senin
    result = add_calendar_features(df, date_col="transaction_date")

    # 2024-01-01 = Senin (day_of_week=0), 2024-01-06 = Sabtu (day_of_week=5)
    assert result.loc[0, "day_of_week"] == 0
    assert result.loc[0, "is_weekend"] == 0
    assert result.loc[5, "day_of_week"] == 5
    assert result.loc[5, "is_weekend"] == 1


def test_calendar_features_cyclical_encoding_range():
    df = make_simple_df()
    result = add_calendar_features(df, date_col="transaction_date")

    # Nilai sin/cos harus selalu di rentang [-1, 1]
    assert result["day_of_week_sin"].between(-1, 1).all()
    assert result["day_of_week_cos"].between(-1, 1).all()
    assert result["month_sin"].between(-1, 1).all()
    assert result["month_cos"].between(-1, 1).all()


def test_build_feature_pipeline_produces_all_columns():
    df = make_simple_df()
    result = build_feature_pipeline(df)

    expected_columns = [
        "lag_1", "lag_7", "lag_14",
        "rolling_mean_7", "rolling_mean_30",
        "day_of_week", "is_weekend", "month",
        "day_of_week_sin", "day_of_week_cos",
        "month_sin", "month_cos",
    ]
    for col in expected_columns:
        assert col in result.columns


def test_lag_features_grouped_by_product_no_cross_contamination():
    dates = pd.date_range("2024-01-01", periods=3, freq="D")
    df = pd.DataFrame({
        "transaction_date": list(dates) * 2,
        "product_id": ["P1"] * 3 + ["P2"] * 3,
        "quantity_sold": [10, 20, 30, 999, 888, 777],
    })
    result = add_lag_features(df, "product_id", "quantity_sold", [1])

    p2_first_row = result[result["product_id"] == "P2"].iloc[0]
    assert pd.isna(p2_first_row["lag_1"])
