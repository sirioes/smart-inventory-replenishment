from unittest.mock import MagicMock

from domain.entities.alert import Alert
from infrastructure.notifiers.dashboard_notifier import DashboardNotifier

def test_dashboard_notifier_sets_channel_and_saves_via_repository():
    alert = Alert(recommendation_id="rec-3", status="open", channel="log")
    fake_repo = MagicMock()
    notifier = DashboardNotifier(alert_repo=fake_repo)

    notifier.notify(alert)

    assert alert.channel == "dashboard"
    fake_repo.save.assert_called_once_with(alert)
