import logging

from domain.entities.alert import Alert
from infrastructure.notifiers.log_notifier import LogNotifier

def test_log_notifier_logs_warning_with_alert_details(caplog):
    alert = Alert(recommendation_id="rec-1", status="open")

    with caplog.at_level(logging.WARNING, logger="inventory.alerts"):
        LogNotifier().notify(alert)

    assert len(caplog.records) == 1
    assert "rec-1" in caplog.text
    assert "open" in caplog.text
