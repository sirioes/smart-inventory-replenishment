import logging

from domain.entities.alert import Alert
from infrastructure.notifiers.email_notifier import EmailNotifier

def test_email_notifier_logs_simulated_email_to_recipient(caplog):
    alert = Alert(recommendation_id="rec-2", status="open")
    notifier = EmailNotifier(recipient="ops@example.com")

    with caplog.at_level(logging.INFO, logger="inventory.alerts.email"):
        notifier.notify(alert)

    assert len(caplog.records) == 1
    assert "ops@example.com" in caplog.text
    assert "rec-2" in caplog.text
