from abc import ABC, abstractmethod


class LLMProvider(ABC):
    @abstractmethod
    def ask(self, system_prompt: str, user_message: str) -> str:
        raise NotImplementedError
