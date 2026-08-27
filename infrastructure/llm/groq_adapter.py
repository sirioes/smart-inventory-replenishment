import os
from typing import Optional

from groq import Groq, GroqError

from domain.interfaces.llm_provider import LLMProvider, LLMProviderError

DEFAULT_MODEL = "openai/gpt-oss-20b"


class GroqAdapter(LLMProvider):
    def __init__(
        self,
        client: Optional[Groq] = None,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
    ) -> None:
        self._client = client
        self._api_key = api_key
        self.model = model or os.getenv("GROQ_MODEL", DEFAULT_MODEL)

    @property
    def client(self) -> Groq:
        if self._client is None:
            self._client = Groq(api_key=self._api_key or os.getenv("GROQ_API_KEY"))
        return self._client

    def ask(self, system_prompt: str, user_message: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
            )
        except GroqError as exc:
            raise LLMProviderError(str(exc)) from exc
        return response.choices[0].message.content or ""
