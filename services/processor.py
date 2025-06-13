import asyncio
import logging
from typing import Any, Callable, Optional, Awaitable
from .queueservice import get_queue_service


# Set up logging
logger = logging.getLogger(__name__)


class MessageProcessor:
    def __init__(
        self, message_handler: Optional[Callable[[Any], Awaitable[None]]] = None
    ):
        """
        Initialize the message processor.

        Args:
            message_handler: Optional async function to handle messages.
                           If not provided, uses default_message_handler.
        """
        self.queue_service = get_queue_service()
        self.message_handler = message_handler or self.default_message_handler
        self._running = False
        self._task = None

    async def default_message_handler(self, message: Any) -> None:
        """Default message handler that just logs the message."""
        logger.info(f"Processing message: {message}")
        # Add your custom message processing logic here
        await asyncio.sleep(0.1)  # Simulate some processing time

    async def process_single_message(self) -> bool:
        """
        Process a single message from the queue.

        Returns:
            bool: True if a message was processed, False if queue was empty
        """
        message = self.queue_service.pop_nowait()
        if message is not None:
            try:
                await self.message_handler(message)
                logger.debug(f"Successfully processed message: {message}")
                return True
            except Exception as e:
                logger.error(f"Error processing message {message}: {e}")
                # You might want to put failed messages back in queue or dead letter queue
                return True  # Still counts as processing attempt
        return False

    async def process_messages_continuously(self, poll_interval: float = 0.1) -> None:
        """
        Continuously process messages from the queue.

        Args:
            poll_interval: Time to wait between queue checks when empty (seconds)
        """
        logger.info("Starting continuous message processing")
        self._running = True

        try:
            while self._running:
                processed = await self.process_single_message()
                if not processed:
                    # No message to process, wait before checking again
                    await asyncio.sleep(poll_interval)
        except asyncio.CancelledError:
            logger.info("Message processing cancelled")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in message processing: {e}")
            raise
        finally:
            self._running = False
            logger.info("Message processing stopped")

    async def process_batch(self, batch_size: int = 10, timeout: float = 5.0) -> int:
        """
        Process a batch of messages from the queue.

        Args:
            batch_size: Maximum number of messages to process
            timeout: Maximum time to spend processing the batch

        Returns:
            int: Number of messages processed
        """
        logger.info(f"Processing batch of up to {batch_size} messages")
        processed_count = 0
        start_time = asyncio.get_event_loop().time()

        for _ in range(batch_size):
            # Check timeout
            if asyncio.get_event_loop().time() - start_time >= timeout:
                logger.warning(
                    f"Batch processing timeout reached after {processed_count} messages"
                )
                break

            processed = await self.process_single_message()
            if processed:
                processed_count += 1
            else:
                # No more messages in queue
                break

        logger.info(f"Batch processing completed: {processed_count} messages processed")
        return processed_count

    def start_background_processing(self, poll_interval: float = 0.1) -> None:
        """
        Start processing messages in the background.

        Args:
            poll_interval: Time to wait between queue checks when empty (seconds)
        """
        if self._task and not self._task.done():
            logger.warning("Background processing already running")
            return

        self._task = asyncio.create_task(
            self.process_messages_continuously(poll_interval)
        )
        logger.info("Background message processing started")

    def stop_background_processing(self) -> None:
        """Stop background message processing."""
        self._running = False
        if self._task and not self._task.done():
            self._task.cancel()
            logger.info("Background message processing stopped")

    async def wait_for_completion(self) -> None:
        """Wait for background processing to complete."""
        if self._task:
            try:
                await self._task
            except asyncio.CancelledError:
                pass

    def get_queue_status(self) -> dict:
        """Get current queue status."""
        return {
            "queue_size": self.queue_service.size(),
            "is_empty": self.queue_service.is_empty(),
            "processor_running": self._running,
            "background_task_active": (
                self._task and not self._task.done() if self._task else False
            ),
        }


# Convenience functions
async def process_message_async(
    message: Any, handler: Optional[Callable[[Any], Awaitable[None]]] = None
) -> None:
    """
    Process a single message asynchronously.

    Args:
        message: The message to process
        handler: Optional custom handler function
    """
    processor = MessageProcessor(handler)
    await processor.message_handler(message)


async def process_all_messages(
    handler: Optional[Callable[[Any], Awaitable[None]]] = None, batch_size: int = 100
) -> int:
    """
    Process all messages currently in the queue.

    Args:
        handler: Optional custom handler function
        batch_size: Maximum number of messages to process in one batch

    Returns:
        int: Number of messages processed
    """
    processor = MessageProcessor(handler)
    return await processor.process_batch(batch_size, timeout=float("inf"))


# Example usage
async def example_message_handler(message: Any) -> None:
    """Example custom message handler."""
    print(f"Custom handler processing: {message}")
    # Add your custom logic here
    await asyncio.sleep(0.05)  # Simulate processing time


# For backwards compatibility and easy testing
async def process_queue_async(poll_interval: float = 0.1) -> None:
    """
    Simple async function to process all messages in the queue.
    This is a convenience function for basic usage.
    """
    processor = MessageProcessor()
    await processor.process_messages_continuously(poll_interval)
