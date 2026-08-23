import os
from functools import lru_cache

from fastapi import Depends
from sqlalchemy.orm import Session

from application.inventory_service_facade import InventoryServiceFacade
from application.use_cases.calculate_reorder_point import (
    CalculateReorderPointUseCase,       
)
from application.use_cases.create_alert import CreateAlertUseCase
from application.use_cases.generate_forecast import GenerateForecastUseCase
from application.use_cases.get_dashboard_data import GetDashboardDataUseCase
from application.use_cases.get_forecast_history import GetForecastHistoryUseCase
from infrastructure.db.session import get_session
from infrastructure.ml.xgboost_strategy import XGBoostStrategy
from infrastructure.notifiers.dashboard_notifier import DashboardNotifier    
from infrastructure.notifiers.email_notifier import EmailNotifier
from infrastructure.notifiers.log_notifier import LogNotifier
from infrastructure.repositories.sqlalchemy_alert_repository import (
    SQLAlchemyAlertRepository,  
)
from infrastructure.repositories.sqlalchemy_forecast_repository import (
    SQLAlchemyForecastRepository,
)
from infrastructure.repositories.sqlalchemy_inventory_repository import (
    SQLAlchemyInventoryRepository,
)
from infrastructure.repositories.sqlalchemy_product_repository import (
    SQLAlchemyProductRepository,
)
from infrastructure.repositories.sqlalchemy_reorder_repository import (
    SQLAlchemyReorderRepository,      
)
from infrastructure.repositories.sqlalchemy_transaction_repository import (
    SQLAlchemyTransactionRepository,
)

XGBOOST_MODEL_PATH = os.getenv(
    "XGBOOST_MODEL_PATH", "infrastructure/ml/model_registry/xgboost-v1.json"
)
XGBOOST_METADATA_PATH = os.getenv(
    "XGBOOST_METADATA_PATH",
    "infrastructure/ml/model_registry/xgboost-v1_metadata.json",
)
ALERT_EMAIL_RECIPIENT = os.getenv("ALERT_EMAIL_RECIPIENT", "inventory-team@example.com")

@lru_cache(maxsize=1)
def get_forecast_strategy() -> XGBoostStrategy:
    return XGBoostStrategy(
        model_path=XGBOOST_MODEL_PATH, metadata_path=XGBOOST_METADATA_PATH
    )

def get_forecast_use_case(
    session: Session = Depends(get_session),
    strategy: XGBoostStrategy = Depends(get_forecast_strategy),
) -> GenerateForecastUseCase:
    return GenerateForecastUseCase(
        strategy=strategy,
        transaction_repo=SQLAlchemyTransactionRepository(session),
        forecast_repo=SQLAlchemyForecastRepository(session),
    )

def get_reorder_use_case(
    session: Session = Depends(get_session),
) -> CalculateReorderPointUseCase:
    return CalculateReorderPointUseCase(
        product_repo=SQLAlchemyProductRepository(session),
        inventory_repo=SQLAlchemyInventoryRepository(session),
        reorder_repo=SQLAlchemyReorderRepository(session),
    )

def get_alert_use_case(
    session: Session = Depends(get_session),
) -> CreateAlertUseCase:
    return CreateAlertUseCase(
        notifiers=[
            EmailNotifier(recipient=ALERT_EMAIL_RECIPIENT),
            LogNotifier(),
            DashboardNotifier(alert_repo=SQLAlchemyAlertRepository(session)),
        ]    
    )

def get_dashboard_use_case(
    session: Session = Depends(get_session),
) -> GetDashboardDataUseCase:
    return GetDashboardDataUseCase(
        product_repo=SQLAlchemyProductRepository(session),
        inventory_repo=SQLAlchemyInventoryRepository(session),
        reorder_repo=SQLAlchemyReorderRepository(session),
        alert_repo=SQLAlchemyAlertRepository(session),
    )

def get_forecast_history_use_case(
    session: Session = Depends(get_session),
) -> GetForecastHistoryUseCase:
    return GetForecastHistoryUseCase(
        product_repo=SQLAlchemyProductRepository(session),
        forecast_repo=SQLAlchemyForecastRepository(session),
    )

def get_facade(
    forecast_use_case: GenerateForecastUseCase = Depends(get_forecast_use_case),
    reorder_use_case: CalculateReorderPointUseCase = Depends(get_reorder_use_case),
    alert_use_case: CreateAlertUseCase = Depends(get_alert_use_case),
) -> InventoryServiceFacade:
    return InventoryServiceFacade(
        forecast_use_case=forecast_use_case,
        reorder_use_case=reorder_use_case,
        alert_use_case=alert_use_case,
    )
