# Hexagonal Architecture API - Documentation

## Overview
Backend application implementing Hexagonal Architecture, CQRS, and Bundle-contexts using FastAPI.

## Architecture Principles

### 1. Hexagonal Architecture
- Domain layer independent of external frameworks
- Clear separation between business logic and infrastructure
- Dependency inversion principle applied throughout

### 2. CQRS (Command Query Responsibility Segregation)
- Commands: Write operations processed asynchronously via RabbitMQ
- Queries: Read operations executed directly against database
- Separate models optimized for different operations

### 3. Bundle-contexts
- Users Context: Complete user management functionality
- Auth Context: Authentication and authorization
- Shared Context: Common infrastructure and patterns

## Project Structure

```
src/
├── shared/                 # Common infrastructure
│   ├── domain/            # Base entities, value objects, exceptions
│   ├── application/       # Base CQRS patterns, event bus
│   └── infrastructure/    # Database, message broker implementations
└── contexts/
    ├── users/             # User management context
    │   ├── domain/        # User entity, value objects, repositories
    │   ├── application/   # Commands, queries, handlers, DTOs
    │   └── infrastructure/# Models, repositories, API adapters
    └── auth/              # Authentication context
```

## Key Features Implemented

### User Management (CRUD)
- Create user with domain validation
- Retrieve user by ID, email, or username
- Update user profile information
- Activate/deactivate user accounts
- Domain events: UserCreated, UserUpdated

### Authentication
- JWT-based authentication
- Password hashing with bcrypt
- Token verification endpoints

### Domain-Driven Design
- Value Objects: Email, Username, FullName, HashedPassword
- Entity: User with business logic and domain events
- Domain Services: PasswordService, AuthService
- Repository pattern with interfaces

## Technical Implementation

### Technologies Used
- Python 3.11 + FastAPI
- SQLAlchemy + PostgreSQL
- RabbitMQ for async command processing
- JWT for authentication
- pytest for comprehensive testing
- Docker for containerization

### SOLID Principles Applied
- Single Responsibility: Each class has one reason to change
- Open/Closed: Extensible through interfaces
- Liskov Substitution: Proper inheritance hierarchies
- Interface Segregation: Specific, cohesive interfaces
- Dependency Inversion: Depend on abstractions, not concretions

### Design Patterns Used
- Repository Pattern: Data access abstraction
- Command Pattern: Encapsulated requests
- Factory Method: User entity creation
- Observer Pattern: Domain events
- Dependency Injection: Loose coupling

## Testing Strategy

### Domain Layer Coverage (>80%)
- Value Objects: Complete validation testing
- Entities: Business logic and state changes
- Domain Services: Password operations and validation
- Domain Events: Event generation and data

### Test Structure
```
tests/
├── conftest.py              # Pytest configuration and fixtures
├── contexts/
│   └── users/
│       └── domain/
│           ├── test_value_objects.py    # Email, Username, etc.
│           ├── test_entities.py         # User entity
│           └── test_services.py         # PasswordService
```

## API Endpoints

### Users API
- `POST /api/v1/users` - Create new user
- `GET /api/v1/users/{id}` - Get user by ID
- `GET /api/v1/users` - List users (paginated)
- `PUT /api/v1/users/{id}` - Update user profile

### Authentication API
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/verify` - Token verification

### System Endpoints
- `GET /` - API information
- `GET /health` - Health check
- `GET /docs` - Swagger documentation

## Running the Application

### Docker Compose (Recommended)
```bash
docker-compose up --build
```

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run services
docker-compose up db rabbitmq

# Start application
uvicorn src.main:app --reload
```

### Running Tests
```bash
# Run all tests with coverage
python run_tests.py

# Or using pytest directly
pytest --cov=src --cov-report=html
```

## Security Considerations

### Password Security
- bcrypt hashing with automatic salt generation
- Password strength validation (length, complexity)
- No plaintext password storage

### API Security
- JWT tokens with configurable expiration
- Bearer token authentication
- Input validation using Pydantic schemas

### Domain Validation
- Email format validation
- Username format and length constraints
- Name field validation

## Scalability Features

### Horizontal Scalability
- Stateless application design
- Message queue for async processing
- Database connection pooling

### Modular Architecture
- Context-based organization
- Independent deployable units
- Clear interface boundaries

## Docker Services

### Application Stack
- **app**: FastAPI application (port 8000)
- **db**: PostgreSQL 15 (port 5432)
- **rabbitmq**: Message broker (ports 5672, 15672)

### Environment Variables
- `DATABASE_URL`: PostgreSQL connection string
- `RABBITMQ_URL`: RabbitMQ connection string
- `SECRET_KEY`: JWT signing key
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time

## Development Guidelines

### Code Quality
- Type hints throughout the codebase
- Comprehensive docstrings
- PEP 8 code style compliance
- Error handling and logging

### Testing Requirements
- Unit tests for all domain logic
- Integration tests for API endpoints
- Minimum 80% coverage for domain layer
- Mocking external dependencies

### Architecture Compliance
- No framework dependencies in domain layer
- Repository interfaces in domain
- Command/Query separation maintained
- Event-driven communication between contexts

## Future Enhancements

### Planned Features
- User roles and permissions
- Email verification workflow
- Password reset functionality
- Audit logging system
- API rate limiting

### Technical Improvements
- Redis caching layer
- Database migrations with Alembic
- Monitoring and metrics
- CI/CD pipeline
- Performance optimization

## Conclusion

This project demonstrates a production-ready implementation of modern software architecture patterns. The combination of Hexagonal Architecture, CQRS, and Bundle-contexts provides a solid foundation for scalable, maintainable, and testable applications.

The emphasis on domain-driven design ensures that business logic remains pure and independent of technical concerns, while the comprehensive testing strategy provides confidence in the system's reliability and correctness. 