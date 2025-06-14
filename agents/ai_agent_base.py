from abc import ABC, abstractmethod
from typing import Optional

from services.azure_openai_service import AzureOpenAIService


class AIAgentBase(ABC):
    def __init__(
        self,
        name: str = "BaseAgent",
        llm: AzureOpenAIService = None,
        system_prompt: str = "You are a helpful assistant.",
    ):
        self.name = name
        self.llm = llm or AzureOpenAIService()
        self.system_prompt = system_prompt

    def update_messages(
        self, messages: list[dict[str, str]] = [], max: int = 10
    ) -> list[dict[str, str]]:
        if len(messages) == 0:
            return []
        if messages[0]["role"] != "system":
            messages.insert(0, {"role": "system", "content": self.system_prompt})
        elif messages[0]["role"] == "system":
            messages[0]["content"] = self.system_prompt
        # keep the first message and the last max messages
        if len(messages) > max:
            messages = messages[:1] + messages[-max:]
        return messages

    def completion(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.1,
        max_tokens: Optional[int] = None,
        **kwargs,
    ) -> str:
        messages = self.update_messages(messages)
        return self.llm.get_chat_completion(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs,
        )
