from agents.transcript_generation_agent import TranscriptGenerationAgent
from agents.agent_base import (
    AgentBase,
)
from processors.processor_base import ProcessorBase
from messages.queue_message import QueueMessage
from services.file_service import FileService
from services.azure_openai_service import AzureOpenAIService
from services.log_service import get_logger

logger = get_logger(__name__)


class TranscriptionProcessor(ProcessorBase):
    def process_message(self, message: QueueMessage) -> None:
        logger.info(f"Processing generation message: {message}")
        FileService.append_to_file(str(message))
        self.messagage = message
        agent: AgentBase = TranscriptGenerationAgent()
        mock_transcript = agent.completion(
            messages=[
                {"role": "user", "content": message.data.content},
            ],
            temperature=0.1,
        )
        FileService.append_to_file(mock_transcript)
        # self.llm.get_chat_completion(messages=[])
