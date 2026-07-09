from typing import List

from domain.entities.alert import Alert
from domain.entities.reorder_recommendation import ReorderRecommendation
from domain.interfaces.notifier import Notifier


class CreateAlertUseCase:

    def __init__(self, notifiers: List[Notifier]) -> None:
        self.notifiers = notifiers

    def execute(self, recommendation: ReorderRecommendation) -> Alert:
        alert = Alert(recommendation_id=recommendation.product_id, status="open")
        for notifier in self.notifiers:
            notifier.notify(alert)
        return alert
