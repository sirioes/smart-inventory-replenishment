from typing import List

from sqlalchemy.orm import Session

from domain.entities.forecast_result import ForecastResult
from domain.interfaces.forecast_repository import ForecastRepository
from infrastructure.db.models import ForecastResultModel


class SQLAlchemyForecastRepository(ForecastRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, forecast: ForecastResult) -> None:
        row = ForecastResultModel(
            product_id=forecast.product_id,
            forecast_date=forecast.forecast_date,
            predicted_demand=forecast.predicted_demand,
            model_version=forecast.model_version,
        )
        self.session.add(row)
        self.session.commit()

    def list_by_product_id(self, product_id: str) -> List[ForecastResult]:
        rows = (
            self.session.query(ForecastResultModel)
            .filter(ForecastResultModel.product_id == product_id)
            .order_by(
                ForecastResultModel.forecast_date.asc(),
                ForecastResultModel.generated_at.asc(),
            )
            .all()
        )
        return [
            ForecastResult(
                product_id=row.product_id,
                predicted_demand=row.predicted_demand,
                model_version=row.model_version,
                forecast_date=row.forecast_date,
            )
            for row in rows
        ]
