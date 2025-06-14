from abc import ABC, abstractmethod

from messages.queue_message import QueueMessage
from services.azure_openai_service import AzureOpenAIService


class ProcessorBase(ABC):
    def __init__(self, llm: AzureOpenAIService = None):
        self.llm = llm or AzureOpenAIService()
        self.messagage: QueueMessage = None

    @abstractmethod
    def process_message(self, message: QueueMessage) -> None:
        pass
