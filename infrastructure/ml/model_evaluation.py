import numpy as np


def calculate_mae(y_true, y_pred) -> float:
    """Mean Absolute Error - rata-rata selisih absolut antara prediksi dan nilai aktual."""
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    return float(np.mean(np.abs(y_true - y_pred)))


def calculate_mape(y_true, y_pred) -> float:
    """Mean Absolute Percentage Error - rata-rata persentase kesalahan."""
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    mask = y_true != 0
    if mask.sum() == 0:
        return float("nan")
    return float(np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100)


def calculate_wape(y_true, y_pred) -> float:
    """Weighted Absolute Percentage Error - alternatif MAPE yang lebih tahan terhadap nilai aktual mendekati nol."""
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    total_actual = np.sum(np.abs(y_true))
    if total_actual == 0:
        return float("nan")
    return float(np.sum(np.abs(y_true - y_pred)) / total_actual * 100)
