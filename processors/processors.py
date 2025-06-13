from aiagents.ChineseTranslationAgent import ChineseTranslationAgent
from aiagents.TranscriptGenerationAgent import TranscriptGenerationAgent
from aiagents.AIAgentBase import (
    AIAgentBase,
)
from processors.processorbase import ProcessorBase
from messagetypes.messages import Message
from services.fileservice import FileService
from services.logservice import get_logger
from services.azureopenaiservice import AzureOpenAIService

logger = get_logger(__name__)


class AnalysisProcessor(ProcessorBase):
    def process_message(self, message: Message) -> None:
        logger.info(f"Processing generation message: {message}")
        FileService.append_to_file(str(message))
        self.messagage = message

        logger.info(f"Generating mock transcript")
        agent: AIAgentBase = TranscriptGenerationAgent()
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
        # self.llm.get_chat_completion(messages=[])


def transcription_agent(
    message: Message = None, llm: AzureOpenAIService = None
) -> None:
    system_promt = "You are a transcription agent. Process the message and return the transcription."
    llm.get_chat_completion(messages=[])


class TranscriptionProcessor(ProcessorBase):
    def process_message(self, message: Message) -> None:
        logger.info(f"Processing generation message: {message}")
        FileService.append_to_file(str(message))
        self.messagage = message
        agent: AIAgentBase = TranscriptGenerationAgent()
        mock_transcript = agent.completion(
            messages=[
                {"role": "user", "content": message.data.content},
            ],
            temperature=0.1,
        )
        FileService.append_to_file(mock_transcript)
        # self.llm.get_chat_completion(messages=[])
