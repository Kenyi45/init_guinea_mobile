from abc import ABC, abstractmethod
from typing import List
from src.shared.domain.base_entity import DomainEvent


class EventBus(ABC):
    """Interface for event bus."""
    
    @abstractmethod
    async def publish(self, events: List[DomainEvent]) -> None:
        """Publish domain events."""
        pass


class EventHandler(ABC):
    """Base class for event handlers."""
    
    @abstractmethod
    def can_handle(self, event: DomainEvent) -> bool:
        """Check if this handler can handle the event."""
        pass
    
    @abstractmethod
    async def handle(self, event: DomainEvent) -> None:
        """Handle the domain event."""
        pass 