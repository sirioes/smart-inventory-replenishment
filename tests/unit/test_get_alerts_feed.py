from unittest.mock import MagicMock

from application.use_cases.get_alerts_feed import GetAlertsFeedUseCase


def test_get_alerts_feed_returns_items_from_repo():
    alert_repo = MagicMock()
    alert_repo.list_recent.return_value = [
        {
            "alert_id": "A1",
            "product_id": "P1",
            "sku": "SKU-1",
            "name": "Widget",
            "status": "open",
            "channel": "log",
            "created_at": "2026-08-01T10:00:00",
            "recommended_qty": 20,
        }
    ]

    use_case = GetAlertsFeedUseCase(alert_repo=alert_repo)

    result = use_case.execute(limit=10)

    assert len(result) == 1
    assert result[0]["status"] == "open"
    alert_repo.list_recent.assert_called_once_with(limit=10)
