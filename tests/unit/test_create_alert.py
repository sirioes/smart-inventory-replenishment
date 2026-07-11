from unittest.mock import MagicMock

from application.use_cases.create_alert import CreateAlertUseCase
from domain.entities.reorder_recommendation import ReorderRecommendation


def test_create_alert_notifies_all_registered_notifiers():
    fake_notifier_1 = MagicMock()
    fake_notifier_2 = MagicMock()

    use_case = CreateAlertUseCase(notifiers=[fake_notifier_1, fake_notifier_2])

    recommendation = ReorderRecommendation(
        product_id="B1", reorder_point=20.0, recommended_qty=15, needs_restock=True
    )

    alert = use_case.execute(recommendation)

    fake_notifier_1.notify.assert_called_once_with(alert)
    fake_notifier_2.notify.assert_called_once_with(alert)
