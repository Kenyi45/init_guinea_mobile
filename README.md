# Hexagonal Architecture API

Backend application built with **FastAPI** using **Hexagonal Architecture**, **CQRS**, and **Bundle-contexts**.

## Architecture

### Hexagonal Architecture
- **Domain Independence**: Business logic independent of external frameworks
- **Testability**: Easy testing through adapter mocks
- **Flexibility**: Easy swapping of infrastructure implementations

### CQRS Pattern
- **Commands**: Write operations processed asynchronously via RabbitMQ
- **Queries**: Read operations executed directly against read models
- **Separation**: Different optimized models for reading and writing

### Bundle-contexts
- **Users Context**: User management
- **Auth Context**: Authentication and authorization
- Each context includes Domain, Application, and Infrastructure layers

## Project Structure

```
src/
├── shared/                    # Shared code between contexts
│   ├── domain/               # Base entities and value objects
│   ├── application/          # Base CQRS patterns
│   └── infrastructure/       # Database and Message Broker
└── contexts/
    ├── users/                # Users context
    │   ├── domain/           # User entities, value objects, repositories
    │   ├── application/      # Commands, queries, handlers, DTOs
    │   └── infrastructure/   # SQLAlchemy models, repositories, adapters
    └── auth/                 # Authentication context
        ├── domain/
        ├── application/
        └── infrastructure/
```

## Technologies

- **Python 3.11** + **FastAPI**
- **SQLAlchemy** + **PostgreSQL**
- **RabbitMQ** for CQRS commands
- **JWT** authentication
- **Docker** containerization
- **pytest** for testing

## Quick Start

### Using Docker (Recommended)

```bash
# Build and run services
docker-compose up --build

# API available at http://localhost:8000
```

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run external services
docker-compose up db rabbitmq

# Run application
uvicorn src.main:app --reload
```

## API Endpoints

### Users
- `POST /api/v1/users` - Create user
- `GET /api/v1/users/{id}` - Get user by ID
- `GET /api/v1/users` - List users
- `PUT /api/v1/users/{id}` - Update user

### Authentication
- `POST /api/v1/auth/login` - Login
- `POST /api/v1/auth/verify` - Verify token

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Domain tests only
pytest tests/contexts/users/domain/
```

## Key Features

- ✅ User CRUD operations with domain validation
- ✅ JWT authentication
- ✅ Password hashing with bcrypt
- ✅ Domain events (UserCreated, UserUpdated)
- ✅ CQRS pattern implementation
- ✅ 80%+ domain layer test coverage
- ✅ Docker containerization
- ✅ SOLID principles

## Example Usage

### Create User
```bash
curl -X POST "http://localhost:8000/api/v1/users" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "user123",
    "first_name": "John",
    "last_name": "Doe",
    "password": "MyPassword123"
  }'
```

### Login
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "MyPassword123"
  }'
```

## Architectural Decisions

1. **Hexagonal Architecture**: Domain independence and testability
2. **CQRS**: Async commands via RabbitMQ, sync queries for performance
3. **Bundle-contexts**: Modular organization for scalability
4. **Domain-Driven Design**: Value objects, entities, and domain events
5. **Dependency Injection**: Loose coupling and testability

## Docker Services

- **app**: FastAPI application (port 8000)
- **db**: PostgreSQL database (port 5432)
- **rabbitmq**: Message broker (port 5672, management UI 15672)

---

**Built with ❤️ using Hexagonal Architecture, CQRS, and SOLID principles** 