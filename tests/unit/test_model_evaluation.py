from infrastructure.ml.model_evaluation import calculate_mae, calculate_mape, calculate_wape


def test_calculate_mae_simple_case():
    y_true = [10, 20, 30]
    y_pred = [12, 18, 33]
    assert calculate_mae(y_true, y_pred) == 7 / 3


def test_calculate_mae_perfect_prediction_is_zero():
    y_true = [5, 10, 15]
    y_pred = [5, 10, 15]
    assert calculate_mae(y_true, y_pred) == 0.0


def test_calculate_mape_simple_case():
    y_true = [100, 200]
    y_pred = [110, 180]
    assert calculate_mape(y_true, y_pred) == 10.0


def test_calculate_mape_ignores_zero_actual():
    y_true = [0, 100]
    y_pred = [50, 110]
    assert calculate_mape(y_true, y_pred) == 10.0


def test_calculate_wape_less_sensitive_to_small_values():
    y_true = [2, 500]
    y_pred = [20, 510]
    mape_result = calculate_mape(y_true, y_pred)
    wape_result = calculate_wape(y_true, y_pred)
    assert wape_result < mape_result


def test_calculate_wape_simple_case():
    y_true = [100, 200]
    y_pred = [110, 180]
    assert calculate_wape(y_true, y_pred) == 10.0
