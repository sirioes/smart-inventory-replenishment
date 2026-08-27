from abc import ABC, abstractmethod


class LLMProviderError(Exception):
    pass


class LLMProvider(ABC):
    @abstractmethod
    def ask(self, system_prompt: str, user_message: str) -> str:
        raise NotImplementedError
