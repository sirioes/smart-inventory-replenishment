from dataclasses import dataclass
from typing import List, Optional

from domain.interfaces.alert_repository import AlertRepository
from domain.interfaces.inventory_repository import InventoryRepository
from domain.interfaces.product_repository import ProductRepository
from domain.interfaces.reorder_repository import ReorderRepository


@dataclass
class ProductDashboardData:
    """Read-model for one row of the dashboard. Not a domain entity —
    it exists purely to carry this use case's aggregated output."""

    product_id: str
    sku: str
    name: str
    current_stock: int
    safety_stock: int
    reorder_point: Optional[float]
    recommended_qty: Optional[int]
    needs_restock: bool
    open_alert_count: int


class GetDashboardDataUseCase:

    def __init__(
        self,
        product_repo: ProductRepository,
        inventory_repo: InventoryRepository,
        reorder_repo: ReorderRepository,
        alert_repo: AlertRepository,
    ) -> None:
        self.product_repo = product_repo
        self.inventory_repo = inventory_repo
        self.reorder_repo = reorder_repo
        self.alert_repo = alert_repo

    def execute(self) -> List[ProductDashboardData]:
        products = self.product_repo.list_active_products()
        inventory_by_product = {
            item.product_id: item for item in self.inventory_repo.list_all()
        }

        dashboard_rows: List[ProductDashboardData] = []
        for product in products:
            inventory = inventory_by_product.get(product.id)
            recommendation = self.reorder_repo.get_latest_by_product_id(product.id)

            dashboard_rows.append(
                ProductDashboardData(
                    product_id=product.id,
                    sku=product.sku,
                    name=product.name,
                    current_stock=inventory.current_stock if inventory else 0,
                    safety_stock=inventory.safety_stock if inventory else 0,
                    reorder_point=recommendation.reorder_point if recommendation else None,
                    recommended_qty=recommendation.recommended_qty if recommendation else None,
                    needs_restock=recommendation.needs_restock if recommendation else False,
                    open_alert_count=self.alert_repo.count_open_for_product(product.id),
                )
            )
        return dashboard_rows
