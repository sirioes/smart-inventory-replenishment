from domain.entities.alert import Alert
from domain.interfaces.alert_repository import AlertRepository
from domain.interfaces.notifier import Notifier

class DashboardNotifier(Notifier):
    def __init__(self, alert_repo: AlertRepository) -> None:
        self.alert_repo = alert_repo

    def notify(self, alert: Alert) -> None:
        alert.channel = "dashboard"
        self.alert_repo.save(alert)
