from abc import ABC, abstractmethod

from messagetypes.messages import Message
from services.azureopenaiservice import AzureOpenAIService


class ProcessorBase(ABC):
    def __init__(self, llm: AzureOpenAIService = None):
        self.llm = llm or AzureOpenAIService()
        self.messagage: Message = None

    @abstractmethod
    def process_message(self, message: Message) -> None:
        pass
