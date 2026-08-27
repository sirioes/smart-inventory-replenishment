from unittest.mock import MagicMock

import pytest
from groq import GroqError

from domain.interfaces.llm_provider import LLMProviderError
from infrastructure.llm.groq_adapter import GroqAdapter


def _mock_client(reply_text: str) -> MagicMock:
    client = MagicMock()
    completion = MagicMock()
    completion.choices = [MagicMock(message=MagicMock(content=reply_text))]
    client.chat.completions.create.return_value = completion
    return client


def test_ask_returns_the_model_reply_text():
    client = _mock_client("Produk A perlu direstock 20 unit.")

    adapter = GroqAdapter(client=client, model="test-model")
    result = adapter.ask(system_prompt="Kamu asisten inventory.", user_message="Produk apa yang perlu direstock?")

    assert result == "Produk A perlu direstock 20 unit."


def test_ask_sends_system_and_user_messages_to_the_client():
    client = _mock_client("ok")

    adapter = GroqAdapter(client=client, model="test-model")
    adapter.ask(system_prompt="SYSTEM", user_message="USER")

    _, kwargs = client.chat.completions.create.call_args
    assert kwargs["model"] == "test-model"
    assert kwargs["messages"] == [
        {"role": "system", "content": "SYSTEM"},
        {"role": "user", "content": "USER"},
    ]


def test_ask_falls_back_to_empty_string_when_content_is_none():
    client = _mock_client(None)

    adapter = GroqAdapter(client=client, model="test-model")
    result = adapter.ask(system_prompt="SYSTEM", user_message="USER")

    assert result == ""


def test_model_defaults_to_current_supported_model_when_unset(monkeypatch):
    monkeypatch.delenv("GROQ_MODEL", raising=False)
    client = _mock_client("ok")

    adapter = GroqAdapter(client=client)

    assert adapter.model == "openai/gpt-oss-20b"


def test_model_reads_from_env_when_set(monkeypatch):
    monkeypatch.setenv("GROQ_MODEL", "openai/gpt-oss-120b")
    client = _mock_client("ok")

    adapter = GroqAdapter(client=client)

    assert adapter.model == "openai/gpt-oss-120b"


def test_ask_translates_groq_error_into_domain_error():
    client = MagicMock()
    client.chat.completions.create.side_effect = GroqError("rate limited")

    adapter = GroqAdapter(client=client, model="test-model")

    with pytest.raises(LLMProviderError):
        adapter.ask(system_prompt="SYSTEM", user_message="USER")
