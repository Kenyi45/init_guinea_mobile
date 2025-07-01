from abc import ABC, abstractmethod
from typing import Any, TypeVar, Generic
from pydantic import BaseModel


class Query(BaseModel, ABC):
    """Base class for queries in CQRS pattern."""
    pass


T = TypeVar('T')
R = TypeVar('R')


class QueryHandler(Generic[T, R], ABC):
    """Base class for query handlers."""
    
    @abstractmethod
    async def handle(self, query: T) -> R:
        """Handle the query and return result."""
        pass 