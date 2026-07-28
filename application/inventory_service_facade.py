from application.use_cases.calculate_reorder_point import (
    CalculateReorderPointUseCase,
)
from application.use_cases.create_alert import CreateAlertUseCase
from application.use_cases.generate_forecast import GenerateForecastUseCase
from domain.entities.reorder_recommendation import ReorderRecommendation


class InventoryServiceFacade:
    def __init__(
        self,
        forecast_use_case: GenerateForecastUseCase,
        reorder_use_case: CalculateReorderPointUseCase,
        alert_use_case: CreateAlertUseCase,
    ) -> None:
        self.forecast_use_case = forecast_use_case
        self.reorder_use_case = reorder_use_case
        self.alert_use_case = alert_use_case

    def process_product(self, product_id: str) -> ReorderRecommendation:
        raise NotImplementedError(
            "InventoryServiceFacade.process_product is implemented in "
            "Issue #20 (Implement Inventory Service Facade)."
        )
