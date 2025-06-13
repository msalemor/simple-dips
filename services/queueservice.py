import pika
from services.logservice import get_logger

logger = get_logger(__name__)


class RabbitMQQueueService:
    def __init__(
        self,
        host="localhost",
        port=5672,
        username="admin",
        password="admin",
        virtual_host="/",
    ):
        credentials = pika.PlainCredentials(username, password)
        self.connection_params = pika.ConnectionParameters(
            host=host, port=port, virtual_host=virtual_host, credentials=credentials
        )
        self.connection = pika.BlockingConnection(self.connection_params)
        self.channel = self.connection.channel()

    def create_queue(self, queue_name, durable=True):
        logger.info(f"Creating queue: {queue_name}, durable={durable}")
        self.channel.queue_declare(queue=queue_name, durable=durable)

    def push_message(self, queue_name, message):
        logger.info(f"Pushing message to queue: {queue_name}")
        self.channel.basic_publish(
            exchange="",
            routing_key=queue_name,
            body=message,
            properties=pika.BasicProperties(delivery_mode=2),  # make message persistent
        )

    def pop_message(self, queue_name, auto_ack=True):
        logger.info(f"Popping message from queue: {queue_name}, auto_ack={auto_ack}")
        method_frame, header_frame, body = self.channel.basic_get(
            queue=queue_name, auto_ack=auto_ack
        )
        if method_frame:
            return body.decode()
        return None

    def count_messages(self, queue_name):
        logger.info(f"Counting messages in queue: {queue_name}")
        queue = self.channel.queue_declare(queue=queue_name, passive=True)
        return queue.method.message_count

    def clear_queue(self, queue_name):
        logger.info(f"Clearing queue: {queue_name}")
        self.channel.queue_purge(queue=queue_name)

    def close(self):
        logger.info("Closing RabbitMQ connection")
        self.connection.close()

    def process_messages(self, queue_name: str, delegate, auto_ack=False) -> None:
        logger.info(
            f"Processing messages from queue: {queue_name}, auto_ack={auto_ack}"
        )
        for method_frame, properties, body in self.channel.consume(
            queue=queue_name, auto_ack=auto_ack
        ):
            try:
                delegate(body.decode())
                if not auto_ack:
                    self.channel.basic_ack(method_frame.delivery_tag)
            except Exception as e:
                print(f"Error processing message: {e}")
                if not auto_ack:
                    self.channel.basic_nack(method_frame.delivery_tag, requeue=True)
                break


instance = None


def get_queue_service():
    global instance
    if instance is None:
        instance = RabbitMQQueueService()
    return instance
