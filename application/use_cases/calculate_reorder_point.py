import math

from domain.entities.forecast_result import ForecastResult
from domain.entities.reorder_recommendation import ReorderRecommendation
from domain.interfaces.inventory_repository import InventoryRepository
from domain.interfaces.product_repository import ProductRepository
from domain.interfaces.reorder_repository import ReorderRepository

DEFAULT_SERVICE_LEVEL_Z = 1.65  # setara kurang lebih 95% service level


class CalculateReorderPointUseCase:

    def __init__(
        self,
        product_repo: ProductRepository,
        inventory_repo: InventoryRepository,
        reorder_repo: ReorderRepository,
        demand_std_dev: float = 0.0,
        service_level_z: float = DEFAULT_SERVICE_LEVEL_Z,
    ) -> None:
        self.product_repo = product_repo
        self.inventory_repo = inventory_repo
        self.reorder_repo = reorder_repo
        self.demand_std_dev = demand_std_dev
        self.service_level_z = service_level_z

    def execute(self, product_id: str, forecast: ForecastResult) -> ReorderRecommendation:
        product = self.product_repo.get_by_id(product_id)
        inventory = self.inventory_repo.get_by_product_id(product_id)

        safety_stock = self.service_level_z * self.demand_std_dev * math.sqrt(
            product.lead_time_days
        )
        reorder_point = (forecast.predicted_demand * product.lead_time_days) + safety_stock

        needs_restock = inventory.current_stock <= reorder_point
        recommended_qty = max(0, round(reorder_point - inventory.current_stock))

        recommendation = ReorderRecommendation(
            product_id=product_id,
            reorder_point=reorder_point,
            recommended_qty=recommended_qty,
            needs_restock=needs_restock,
        )
        self.reorder_repo.save(recommendation)
        return recommendation
