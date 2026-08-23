from typing import Optional

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

    def get_latest_by_product_id(self, product_id: str) -> Optional[ReorderRecommendation]:
        row = (
            self.session.query(ReorderRecommendationModel)
            .filter(ReorderRecommendationModel.product_id == product_id)
            .order_by(ReorderRecommendationModel.created_at.desc())
            .first()
        )
        if row is None:
            return None
        return ReorderRecommendation(
            product_id=row.product_id,
            reorder_point=row.reorder_point,
            recommended_qty=row.recommended_qty,
            needs_restock=row.needs_restock,
        )
