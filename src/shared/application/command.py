from abc import ABC, abstractmethod
from typing import Any, TypeVar, Generic
from pydantic import BaseModel


class Command(BaseModel, ABC):
    """Base class for commands in CQRS pattern."""
    pass


T = TypeVar('T')


class CommandHandler(Generic[T], ABC):
    """Base class for command handlers."""
    
    @abstractmethod
    async def handle(self, command: T) -> Any:
        """Handle the command and return result."""
        pass 