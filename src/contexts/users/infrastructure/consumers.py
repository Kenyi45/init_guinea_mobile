import asyncio
import json
import logging
from typing import Dict, Any
from src.shared.infrastructure.message_broker import RabbitMQBroker
from src.contexts.users.application.commands import CreateUserCommand
from src.contexts.users.application.handlers import CreateUserCommandHandler
from src.contexts.users.infrastructure.repositories import SQLAlchemyUserRepository
from src.contexts.users.domain.services import PasswordService
from src.shared.infrastructure.database import SessionLocal
from src.shared.application.event_bus import EventBus
from src.shared.infrastructure.metrics import record_message_consumed


logger = logging.getLogger(__name__)


class UserCommandConsumer:
    """Consumer for user commands from RabbitMQ."""
    
    def __init__(self):
        self.broker = RabbitMQBroker()
        self.password_service = PasswordService()
    
    async def start_consuming(self):
        """Start consuming messages from the user command queue."""
        await self.broker.consume("user_commands", self.handle_user_command)
    
    async def handle_user_command(self, message: Dict[str, Any]):
        """Handle user command messages."""
        queue_name = "user_commands"
        try:
            command_type = message.get("command_type")
            command_data = message.get("data", {})
            
            logger.info(f"Processing user command: {command_type}")
            
            if command_type == "create_user":
                await self._handle_create_user(command_data)
                record_message_consumed(queue_name, "success")
            else:
                logger.warning(f"Unknown command type: {command_type}")
                record_message_consumed(queue_name, "unknown_command")
                
        except Exception as e:
            record_message_consumed(queue_name, "error")
            logger.error(f"Error processing user command: {e}")
            raise
    
    async def _handle_create_user(self, data: Dict[str, Any]):
        """Handle create user command."""
        try:
            # Create database session
            db = SessionLocal()
            
            try:
                # Create repository and event bus
                user_repository = SQLAlchemyUserRepository(db)
                
                # Dummy event bus for now
                class DummyEventBus(EventBus):
                    async def publish(self, events):
                        logger.info(f"Publishing events: {[e.event_type for e in events]}")
                
                event_bus = DummyEventBus()
                
                # Create command
                command = CreateUserCommand(
                    email=data["email"],
                    username=data["username"],
                    first_name=data["first_name"],
                    last_name=data["last_name"],
                    password=data["password"]
                )
                
                # Execute command
                handler = CreateUserCommandHandler(user_repository, self.password_service, event_bus)
                result = await handler.handle(command)
                
                logger.info(f"User created successfully: {result.id}")
                
            finally:
                db.close()
                
        except Exception as e:
            logger.error(f"Failed to create user: {e}")
            raise


async def start_user_consumer():
    """Start the user command consumer."""
    consumer = UserCommandConsumer()
    await consumer.start_consuming()


if __name__ == "__main__":
    asyncio.run(start_user_consumer()) 