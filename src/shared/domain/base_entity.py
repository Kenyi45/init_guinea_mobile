from abc import ABC
from typing import Any, Dict, List
from datetime import datetime
import uuid


class DomainEvent:
    """Base class for domain events."""
    
    def __init__(self, event_type: str, data: Dict[str, Any]):
        self.event_type = event_type
        self.data = data
        self.occurred_at = datetime.utcnow()
        self.event_id = str(uuid.uuid4())


class BaseEntity(ABC):
    """Base entity class following DDD principles."""
    
    def __init__(self, entity_id: str = None):
        self._id = entity_id or str(uuid.uuid4())
        self._domain_events: List[DomainEvent] = []
        self._created_at = datetime.utcnow()
        self._updated_at = datetime.utcnow()
    
    @property
    def id(self) -> str:
        return self._id
    
    @property
    def created_at(self) -> datetime:
        return self._created_at
    
    @property
    def updated_at(self) -> datetime:
        return self._updated_at
    
    def mark_updated(self) -> None:
        """Mark entity as updated."""
        self._updated_at = datetime.utcnow()
    
    def add_domain_event(self, event: DomainEvent) -> None:
        """Add a domain event to be published."""
        self._domain_events.append(event)
    
    def clear_domain_events(self) -> None:
        """Clear all domain events."""
        self._domain_events.clear()
    
    def get_domain_events(self) -> List[DomainEvent]:
        """Get all domain events."""
        return self._domain_events.copy()
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, BaseEntity):
            return False
        return self._id == other._id
    
    def __hash__(self) -> int:
        return hash(self._id) 