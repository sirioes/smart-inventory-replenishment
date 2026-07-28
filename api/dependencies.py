import os
from functools import lru_cache
from fastapi import Depends
from sqlalchemy.orm import Session
from application.inventory_service_facade import InventoryServiceFacade
from application.use_cases.generate_forecast import GenerateForecastUseCase
from infrastructure.db.session import get_session
from infrastructure.ml.xgboost_strategy import XGBoostStrategy
from infrastructure.repositories.sqlalchemy_forecast_repository import (
    SQLAlchemyForecastRepository,
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

def get_facade() -> InventoryServiceFacade:
    raise NotImplementedError(
        "Wire InventoryServiceFacade with CalculateReorderPointUseCase and "
        "CreateAlertUseCase here as part of Issue #20 (Implement Inventory "
        "Service Facade)."
    )
