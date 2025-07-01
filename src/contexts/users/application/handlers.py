from typing import Optional, List
from src.shared.application.command import CommandHandler
from src.shared.application.query import QueryHandler
from src.shared.application.event_bus import EventBus
from src.shared.domain.exceptions import NotFoundError, AlreadyExistsError
from src.contexts.users.domain.entities import User
from src.contexts.users.domain.repositories import UserRepository
from src.contexts.users.domain.services import PasswordService
from src.contexts.users.application.commands import (
    CreateUserCommand, UpdateUserCommand, DeactivateUserCommand, ActivateUserCommand
)
from src.contexts.users.application.queries import (
    GetUserByIdQuery, GetUserByEmailQuery, GetUserByUsernameQuery, GetUsersQuery
)
from src.contexts.users.application.dtos import UserDto, UserListDto


def user_to_dto(user: User) -> UserDto:
    """Convert User entity to DTO."""
    return UserDto(
        id=user.id,
        email=user.email.value,
        username=user.username.value,
        first_name=user.full_name.first_name,
        last_name=user.full_name.last_name,
        full_name=user.full_name.full_name,
        is_active=user.is_active,
        created_at=user.created_at,
        updated_at=user.updated_at
    )


class CreateUserCommandHandler(CommandHandler[CreateUserCommand]):
    """Handler for creating a user."""
    
    def __init__(self, user_repository: UserRepository, password_service: PasswordService, event_bus: EventBus):
        self.user_repository = user_repository
        self.password_service = password_service
        self.event_bus = event_bus
    
    async def handle(self, command: CreateUserCommand) -> UserDto:
        """Handle the create user command."""
        # Check if user already exists
        if await self.user_repository.exists_by_email(command.email):
            raise AlreadyExistsError(f"User with email {command.email} already exists")
        
        if await self.user_repository.exists_by_username(command.username):
            raise AlreadyExistsError(f"User with username {command.username} already exists")
        
        # Hash password
        hashed_password = self.password_service.hash_password(command.password)
        
        # Create user
        user = User.create(
            email=command.email,
            username=command.username,
            first_name=command.first_name,
            last_name=command.last_name,
            hashed_password=hashed_password
        )
        
        # Save user
        saved_user = await self.user_repository.save(user)
        
        # Publish domain events
        events = saved_user.get_domain_events()
        if events:
            await self.event_bus.publish(events)
            saved_user.clear_domain_events()
        
        return user_to_dto(saved_user)


class UpdateUserCommandHandler(CommandHandler[UpdateUserCommand]):
    """Handler for updating a user."""
    
    def __init__(self, user_repository: UserRepository, event_bus: EventBus):
        self.user_repository = user_repository
        self.event_bus = event_bus
    
    async def handle(self, command: UpdateUserCommand) -> UserDto:
        """Handle the update user command."""
        user = await self.user_repository.find_by_id(command.user_id)
        if not user:
            raise NotFoundError(f"User with ID {command.user_id} not found")
        
        user.update_profile(
            first_name=command.first_name,
            last_name=command.last_name
        )
        
        saved_user = await self.user_repository.save(user)
        
        # Publish domain events
        events = saved_user.get_domain_events()
        if events:
            await self.event_bus.publish(events)
            saved_user.clear_domain_events()
        
        return user_to_dto(saved_user)


class GetUserByIdQueryHandler(QueryHandler[GetUserByIdQuery, Optional[UserDto]]):
    """Handler for getting a user by ID."""
    
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    async def handle(self, query: GetUserByIdQuery) -> Optional[UserDto]:
        """Handle the get user by ID query."""
        user = await self.user_repository.find_by_id(query.user_id)
        if not user:
            return None
        
        return user_to_dto(user)


class GetUsersQueryHandler(QueryHandler[GetUsersQuery, UserListDto]):
    """Handler for getting all users."""
    
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    async def handle(self, query: GetUsersQuery) -> UserListDto:
        """Handle the get users query."""
        users = await self.user_repository.find_all(limit=query.limit, offset=query.offset)
        
        user_dtos = [user_to_dto(user) for user in users]
        
        return UserListDto(
            users=user_dtos,
            total=len(user_dtos),
            limit=query.limit,
            offset=query.offset
        ) 