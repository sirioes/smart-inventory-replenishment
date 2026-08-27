from unittest.mock import MagicMock

from application.use_cases.answer_inventory_query import AnswerInventoryQueryUseCase
from application.use_cases.get_dashboard_data import ProductDashboardData


def test_execute_grounds_the_prompt_in_real_dashboard_data():
    llm_provider = MagicMock()
    llm_provider.ask.return_value = "Produk SKU-1 perlu direstock."

    dashboard_use_case = MagicMock()
    dashboard_use_case.execute.return_value = [
        ProductDashboardData(
            product_id="P1",
            sku="SKU-1",
            name="Widget",
            current_stock=5,
            safety_stock=10,
            reorder_point=8.0,
            recommended_qty=20,
            needs_restock=True,
            open_alert_count=1,
        )
    ]

    use_case = AnswerInventoryQueryUseCase(
        llm_provider=llm_provider, dashboard_use_case=dashboard_use_case
    )

    result = use_case.execute(question="Produk apa yang perlu direstock?")

    assert result == "Produk SKU-1 perlu direstock."
    _, kwargs = llm_provider.ask.call_args
    assert "SKU-1" in kwargs["system_prompt"]
    assert "PERLU RESTOCK" in kwargs["system_prompt"]
    assert kwargs["user_message"] == "Produk apa yang perlu direstock?"


def test_execute_tells_the_model_when_there_is_no_data_yet():
    llm_provider = MagicMock()
    dashboard_use_case = MagicMock()
    dashboard_use_case.execute.return_value = []

    use_case = AnswerInventoryQueryUseCase(
        llm_provider=llm_provider, dashboard_use_case=dashboard_use_case
    )

    use_case.execute(question="Ada produk apa aja?")

    _, kwargs = llm_provider.ask.call_args
    assert "Belum ada produk" in kwargs["system_prompt"]
