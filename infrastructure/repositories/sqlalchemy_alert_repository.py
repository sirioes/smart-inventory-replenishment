from sqlalchemy.orm import Session

from domain.entities.alert import Alert
from domain.interfaces.alert_repository import AlertRepository
from infrastructure.db.models import AlertModel, ReorderRecommendationModel

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

    def count_open_for_product(self, product_id: str) -> int:
        return (
            self.session.query(AlertModel)
            .join(
                ReorderRecommendationModel,
                AlertModel.recommendation_id == ReorderRecommendationModel.id,
            )
            .filter(
                ReorderRecommendationModel.product_id == product_id,
                AlertModel.status == "open",
            )
            .count()
        )
