from sqlalchemy.orm import Session

from domain.entities.alert import Alert
from domain.interfaces.alert_repository import AlertRepository
from infrastructure.db.models import AlertModel, ProductModel, ReorderRecommendationModel

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

    def list_recent(self, limit: int = 50):
        rows = (
            self.session.query(AlertModel, ReorderRecommendationModel, ProductModel)
            .join(
                ReorderRecommendationModel,
                AlertModel.recommendation_id == ReorderRecommendationModel.id,
            )
            .join(ProductModel, ReorderRecommendationModel.product_id == ProductModel.id)
            .order_by(AlertModel.created_at.desc())
            .limit(limit)
            .all()
        )
        return [
            {
                "alert_id": alert.id,
                "product_id": product.id,
                "sku": product.sku,
                "name": product.name,
                "status": alert.status,
                "channel": alert.channel,
                "created_at": alert.created_at.isoformat(),
                "recommended_qty": recommendation.recommended_qty,
            }
            for alert, recommendation, product in rows
        ]
