from uuid import uuid4
import click


from messages.transcription_data import TranscriptionData
from services.rabbitmq_queue_service import get_queue_service
from services.log_service import get_logger

from messages.queue_message import QueueMessage

from processors.analysis_processor import AnalysisProcessor
from processors.processor_base import ProcessorBase
from processors.transcription_processor import TranscriptionProcessor

from agents.transcript_generation_agent import TranscriptGenerationAgent
from agents.agent_base import AgentBase


logger = get_logger(__name__)


def processing_deletage(msg: str) -> None:
    message: QueueMessage = QueueMessage.from_json(msg)
    processor_classes = {
        "analysisagent": AnalysisProcessor,
        "transcriptionagent": TranscriptionProcessor,
    }
    processor_class = processor_classes.get(message.type)
    if processor_class:
        processor: ProcessorBase = processor_class()
        processor.process_message(message)
    else:
        logger.info(f"Unknown message type: {message.type}")


DEFAULT_QUEUE = "in_queue"
queue_service = get_queue_service()


@click.group(help="sDIPs - Command Line Interface")
def cli():
    pass


@cli.command(help="Count messages in the queue")
@click.option("--name", default=DEFAULT_QUEUE, help="Queue name")
def count(name: str) -> None:
    count = queue_service.count_messages(name)
    logger.info(f"Message count in queue '{name}': {count}")
    queue_service.close()


@cli.command(help="Clear the queue")
@click.option("--name", default=DEFAULT_QUEUE, help="Queue name")
def clear(name: str):
    try:
        logger.info(f"Clearing queue '{name}'")
        queue_service.clear_queue(name)
        logger.info("Queue 'default' cleared.")
        queue_service.close()
    except Exception as e:
        logger.exception(f"Error clearing queue 'default': {e}")


@cli.command(help="Generate messages in the queue")
@click.option("--count", default=1, help="Number of messages to generate.")
@click.option("--name", default=DEFAULT_QUEUE, help="Queue name")
def generate(count: int, name: str) -> None:
    logger.info(f"Generating {count} messages in queue '{name}'")
    for _ in range(count):
        analysis_data = TranscriptionData(
            content="Generate a transcription between Jane and John about an incident with Azure App Service. Finish by the conversation by suggesting that a survey should be started."
        )
        msg = QueueMessage(
            data=analysis_data, cid=str(uuid4()), type="transcriptionagent"
        )
        logger.info(f"Generated message: {msg.to_json()}")
        queue_service.push_message(name, msg.to_json())
    queue_service.close()


@cli.command(help="Process messages in the queue")
@click.option("--name", default=DEFAULT_QUEUE, help="Queue name")
def process(name: str) -> None:
    logger.info(f"Processing messages in queue '{name}'")
    queue_service.process_messages(name, processing_deletage, auto_ack=False)
    queue_service.close()


@cli.command(help="Generate a mock transcript")
def mock_transcript() -> None:
    logger.info("Generating mock transcript")
    agent: AgentBase = TranscriptGenerationAgent()
    mock_transcript = agent.completion(
        messages=[
            {
                "role": "user",
                "content": "Generate a transcription between Jane and John about an incident with Azure App Service. Finish by the conversation by suggesting that a survey should be started.",
            },
        ],
        temperature=0.1,
    )
    logger.info(f"Mock transcript completed:\n{mock_transcript}")


if __name__ == "__main__":
    cli()
