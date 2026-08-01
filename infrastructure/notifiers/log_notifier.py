import logging

from domain.entities.alert import Alert
from domain.interfaces.notifier import Notifier

logger = logging.getLogger("inventory.alerts")

class LogNotifier(Notifier):
    def notify(self, alert: Alert) -> None:
        logger.warning(
            "Restock alert triggered: recommendation_id=%s status=%s",
            alert.recommendation_id,
            alert.status,
        )
