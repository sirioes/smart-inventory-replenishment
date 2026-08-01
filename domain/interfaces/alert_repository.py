from abc import ABC, abstractmethod

from domain.entities.alert import Alert

class AlertRepository(ABC):

    @abstractmethod
    def save(self, alert: Alert) -> None:
        raise NotImplementedError
