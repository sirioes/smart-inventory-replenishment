from sqlalchemy.orm import Session

from domain.entities.reorder_recommendation import ReorderRecommendation
from domain.interfaces.reorder_repository import ReorderRepository
from infrastructure.db.models import ReorderRecommendationModel


class SQLAlchemyReorderRepository(ReorderRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, recommendation: ReorderRecommendation) -> None:
        row = ReorderRecommendationModel(
            product_id=recommendation.product_id,
            reorder_point=recommendation.reorder_point,
            recommended_qty=recommendation.recommended_qty,
            needs_restock=recommendation.needs_restock,
        )
        self.session.add(row)
        self.session.commit()
