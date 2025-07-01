import json
import logging
from typing import List
from src.shared.application.event_bus import EventBus
from src.shared.domain.base_entity import DomainEvent
from src.shared.infrastructure.message_broker import RabbitMQBroker


logger = logging.getLogger(__name__)


class RabbitMQEventBus(EventBus):
    """RabbitMQ implementation of EventBus."""
    
    def __init__(self):
        self.broker = RabbitMQBroker()
    
    async def publish(self, events: List[DomainEvent]) -> None:
        """Publish domain events to RabbitMQ."""
        for event in events:
            try:
                message = {
                    "event_id": event.event_id,
                    "event_type": event.event_type,
                    "data": event.data,
                    "occurred_at": event.occurred_at.isoformat()
                }
                
                # Route events to appropriate queues based on event type
                queue_name = self._get_queue_name(event.event_type)
                await self.broker.publish(queue_name, message)
                
                logger.info(f"Published event {event.event_type} to queue {queue_name}")
                
            except Exception as e:
                logger.error(f"Failed to publish event {event.event_type}: {e}")
                raise
    
    def _get_queue_name(self, event_type: str) -> str:
        """Get queue name based on event type."""
        # Route different event types to different queues
        queue_mapping = {
            "user_created": "user_events",
            "user_updated": "user_events",
            "user_deleted": "user_events",
        }
        
        return queue_mapping.get(event_type, "domain_events") 