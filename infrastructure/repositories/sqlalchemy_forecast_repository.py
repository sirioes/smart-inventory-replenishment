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
