import logging

from domain.entities.alert import Alert
from domain.interfaces.notifier import Notifier

logger = logging.getLogger("inventory.alerts.email")

class EmailNotifier(Notifier):
    def __init__(self, recipient: str) -> None:
        self.recipient = recipient

    def notify(self, alert: Alert) -> None:
        logger.info(
            "Simulated email to %s: restock alert for recommendation_id=%s",
            self.recipient,
            alert.recommendation_id,
        )
