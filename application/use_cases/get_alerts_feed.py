from typing import Any, Dict, List

from domain.interfaces.alert_repository import AlertRepository


class GetAlertsFeedUseCase:
    def __init__(self, alert_repo: AlertRepository) -> None:
        self.alert_repo = alert_repo

    def execute(self, limit: int = 50) -> List[Dict[str, Any]]:
        return self.alert_repo.list_recent(limit=limit)
