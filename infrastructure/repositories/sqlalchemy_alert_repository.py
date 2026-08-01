from sqlalchemy.orm import Session

from domain.entities.alert import Alert
from domain.interfaces.alert_repository import AlertRepository
from infrastructure.db.models import AlertModel

class SQLAlchemyAlertRepository(AlertRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, alert: Alert) -> None:
        row = AlertModel(
            recommendation_id=alert.recommendation_id,
            status=alert.status,
            channel=alert.channel,
        )
        self.session.add(row)
        self.session.commit()
