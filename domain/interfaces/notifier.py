from abc import ABC, abstractmethod

from domain.entities.alert import Alert


class Notifier(ABC):

    @abstractmethod
    def notify(self, alert: Alert) -> None:
        raise NotImplementedError
