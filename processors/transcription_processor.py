from agents.chinese_translation_agent import ChineseTranslationAgent
from agents.transcript_generation_agent import TranscriptGenerationAgent
from agents.agent_base import (
    AgentBase,
)
from processors.processor_base import ProcessorBase
from messages.queue_message import QueueMessage
from services.file_service import FileService

from services.log_service import get_logger

logger = get_logger(__name__)


class TranscriptionProcessor(ProcessorBase):
    def process_message(self, message: QueueMessage) -> None:
        logger.info(f"Processing generation message: {message}")
        FileService.append_to_file(str(message))
        self.messagage = message

        logger.info(f"Generating mock transcript")
        agent: AgentBase = TranscriptGenerationAgent()
        mock_transcript = agent.completion(
            messages=[
                {"role": "user", "content": message.data.content},
            ],
            temperature=0.1,
        )

        logger.info("Translating mock transcript to Chinese")
        agent = ChineseTranslationAgent()
        translation = agent.completion(
            messages=[
                {"role": "user", "content": mock_transcript},
            ],
            temperature=0.1,
        )
        # logger.info(f"Translation: {translation}")
        FileService.append_to_file(
            f"Mock transcript:\n{mock_transcript}\n\nTranslation:\n{translation}"
        )

        logger.info("Mock transcript and translation saved to file.")
