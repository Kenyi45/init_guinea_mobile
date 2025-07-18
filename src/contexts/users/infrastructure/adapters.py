from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.shared.infrastructure.database import get_db
from src.shared.domain.exceptions import NotFoundError, AlreadyExistsError, ValidationError
from src.contexts.users.application.dtos import UserDto, CreateUserDto, UpdateUserDto, UserListDto
from src.contexts.users.application.commands import CreateUserCommand, UpdateUserCommand, DeleteUserCommand
from src.contexts.users.application.queries import GetUserByIdQuery, GetUsersQuery
from src.contexts.users.application.handlers import (
    CreateUserCommandHandler, UpdateUserCommandHandler, DeleteUserCommandHandler, GetUserByIdQueryHandler, GetUsersQueryHandler
)
from src.shared.infrastructure.auth_middleware import get_current_user_id
from src.contexts.users.infrastructure.repositories import SQLAlchemyUserRepository
from src.contexts.users.domain.services import PasswordService
from src.shared.infrastructure.message_broker import RabbitMQBroker
from src.shared.application.event_bus import EventBus


router = APIRouter(prefix="/users", tags=["users"])


# Dependency injection helpers
def get_user_repository(db: Session = Depends(get_db)) -> SQLAlchemyUserRepository:
    """Get user repository instance."""
    return SQLAlchemyUserRepository(db)


def get_password_service() -> PasswordService:
    """Get password service instance."""
    return PasswordService()


def get_event_bus() -> EventBus:
    """Get event bus instance."""
    from src.shared.infrastructure.event_bus_impl import RabbitMQEventBus
    return RabbitMQEventBus()


@router.post("/", response_model=UserDto, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: CreateUserDto,
    user_repository: SQLAlchemyUserRepository = Depends(get_user_repository),
    password_service: PasswordService = Depends(get_password_service),
    event_bus: EventBus = Depends(get_event_bus)
):
    """Create a new user."""
    try:
        command = CreateUserCommand(
            email=user_data.email,
            username=user_data.username,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            password=user_data.password
        )
        
        handler = CreateUserCommandHandler(user_repository, password_service, event_bus)
        result = await handler.handle(command)
        
        return result
    except AlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{user_id}", response_model=UserDto)
async def get_user(
    user_id: str,
    user_repository: SQLAlchemyUserRepository = Depends(get_user_repository),
    current_user_id: str = Depends(get_current_user_id)
):
    """Get a user by ID. Requires authentication."""
    try:
        query = GetUserByIdQuery(user_id=user_id)
        handler = GetUserByIdQueryHandler(user_repository)
        result = await handler.handle(query)
        
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/", response_model=UserListDto)
async def get_users(
    limit: int = 100,
    offset: int = 0,
    user_repository: SQLAlchemyUserRepository = Depends(get_user_repository),
    current_user_id: str = Depends(get_current_user_id)
):
    """Get all users with pagination. Requires authentication."""
    try:
        query = GetUsersQuery(limit=limit, offset=offset)
        handler = GetUsersQueryHandler(user_repository)
        result = await handler.handle(query)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.put("/{user_id}", response_model=UserDto)
async def update_user(
    user_id: str,
    user_data: UpdateUserDto,
    user_repository: SQLAlchemyUserRepository = Depends(get_user_repository),
    event_bus: EventBus = Depends(get_event_bus),
    current_user_id: str = Depends(get_current_user_id)
):
    """Update a user. Requires authentication."""
    try:
        command = UpdateUserCommand(
            user_id=user_id,
            first_name=user_data.first_name,
            last_name=user_data.last_name
        )
        
        handler = UpdateUserCommandHandler(user_repository, event_bus)
        result = await handler.handle(command)
        
        return result
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str,
    user_repository: SQLAlchemyUserRepository = Depends(get_user_repository),
    event_bus: EventBus = Depends(get_event_bus),
    current_user_id: str = Depends(get_current_user_id)
):
    """Delete/deactivate a user. Requires authentication."""
    try:
        command = DeleteUserCommand(user_id=user_id)
        
        handler = DeleteUserCommandHandler(user_repository, event_bus)
        await handler.handle(command)
        
        return None  # 204 No Content
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) 