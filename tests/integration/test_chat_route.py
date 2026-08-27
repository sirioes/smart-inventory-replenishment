from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from api.dependencies import get_answer_inventory_query_use_case
from api.main import app
from domain.interfaces.llm_provider import LLMProviderError


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)

@pytest.fixture(autouse=True)
def _clear_overrides():
    yield
    app.dependency_overrides.clear()

def test_chat_returns_grounded_answer(client: TestClient) -> None:
    fake_use_case = MagicMock()
    fake_use_case.execute.return_value = "SKU-1 perlu direstock 20 unit."
    app.dependency_overrides[get_answer_inventory_query_use_case] = lambda: fake_use_case

    response = client.post("/chat", json={"question": "Produk apa yang perlu direstock?"})

    assert response.status_code == 200
    assert response.json()["answer"] == "SKU-1 perlu direstock 20 unit."
    fake_use_case.execute.assert_called_once_with(question="Produk apa yang perlu direstock?")

def test_chat_rejects_empty_question(client: TestClient) -> None:
    response = client.post("/chat", json={"question": ""})

    assert response.status_code == 422

def test_chat_returns_503_when_llm_provider_is_unavailable(client: TestClient) -> None:
    fake_use_case = MagicMock()
    fake_use_case.execute.side_effect = LLMProviderError("connection failed")
    app.dependency_overrides[get_answer_inventory_query_use_case] = lambda: fake_use_case

    response = client.post("/chat", json={"question": "Halo?"})

    assert response.status_code == 503
