import pika
import json
import os
from typing import Callable, Any
from abc import ABC, abstractmethod
import logging


logger = logging.getLogger(__name__)


class MessageBroker(ABC):
    """Abstract message broker interface."""
    
    @abstractmethod
    async def publish(self, queue_name: str, message: dict) -> None:
        """Publish a message to a queue."""
        pass
    
    @abstractmethod
    async def consume(self, queue_name: str, callback: Callable[[dict], None]) -> None:
        """Consume messages from a queue."""
        pass


class RabbitMQBroker(MessageBroker):
    """RabbitMQ implementation of message broker."""
    
    def __init__(self):
        self.connection_url = os.getenv("RABBITMQ_URL")
        self.connection = None
        self.channel = None
        self._connect()
    
    def _connect(self):
        """Establish connection to RabbitMQ."""
        try:
            parameters = pika.URLParameters(self.connection_url)
            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()
            logger.info("Connected to RabbitMQ")
        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}")
            raise
    
    async def publish(self, queue_name: str, message: dict) -> None:
        """Publish a message to a queue."""
        try:
            if not self.channel:
                self._connect()
            
            self.channel.queue_declare(queue=queue_name, durable=True)
            
            self.channel.basic_publish(
                exchange='',
                routing_key=queue_name,
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # Make message persistent
                )
            )
            logger.info(f"Published message to {queue_name}: {message}")
        except Exception as e:
            logger.error(f"Failed to publish message: {e}")
            raise
    
    async def consume(self, queue_name: str, callback: Callable[[dict], None]) -> None:
        """Consume messages from a queue."""
        try:
            if not self.channel:
                self._connect()
            
            self.channel.queue_declare(queue=queue_name, durable=True)
            
            def wrapper(ch, method, properties, body):
                try:
                    message = json.loads(body)
                    callback(message)
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                except Exception as e:
                    logger.error(f"Error processing message: {e}")
                    ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            
            self.channel.basic_qos(prefetch_count=1)
            self.channel.basic_consume(queue=queue_name, on_message_callback=wrapper)
            
            logger.info(f"Started consuming from {queue_name}")
            self.channel.start_consuming()
        except Exception as e:
            logger.error(f"Failed to consume messages: {e}")
            raise
    
    def close(self):
        """Close connection."""
        if self.connection and not self.connection.is_closed:
            self.connection.close()
            logger.info("Closed RabbitMQ connection") 