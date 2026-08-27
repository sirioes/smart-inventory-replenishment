import os
from typing import Optional

from groq import Groq

from domain.interfaces.llm_provider import LLMProvider

DEFAULT_MODEL = "openai/gpt-oss-20b"


class GroqAdapter(LLMProvider):
    def __init__(
        self,
        client: Optional[Groq] = None,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
    ) -> None:
        self.client = client or Groq(api_key=api_key or os.getenv("GROQ_API_KEY"))
        self.model = model or os.getenv("GROQ_MODEL", DEFAULT_MODEL)

    def ask(self, system_prompt: str, user_message: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
        )
        return response.choices[0].message.content or ""
