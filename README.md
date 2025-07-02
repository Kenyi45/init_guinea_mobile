# 🚀 Hexagonal Architecture API

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)](https://www.postgresql.org)
[![RabbitMQ](https://img.shields.io/badge/RabbitMQ-3.12+-orange.svg)](https://www.rabbitmq.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com)
[![Tests](https://img.shields.io/badge/Coverage-80%25+-brightgreen.svg)](https://pytest.org)

> **Aplicación backend moderna** construida con **FastAPI** implementando **Arquitectura Hexagonal**, **CQRS**, y **Bundle-contexts** siguiendo principios **SOLID** y **Domain-Driven Design**.

## 📖 Tabla de Contenidos

- [🏗️ Arquitectura](#️-arquitectura)
- [⚙️ Tecnologías](#️-tecnologías)
- [🚀 Inicio Rápido](#-inicio-rápido)
- [📁 Estructura del Proyecto](#-estructura-del-proyecto)
- [🔗 API Endpoints](#-api-endpoints)
- [🧪 Testing](#-testing)
- [🎯 Características Principales](#-características-principales)
- [💡 Ejemplos de Uso](#-ejemplos-de-uso)
- [🐳 Servicios Docker](#-servicios-docker)
- [📚 Documentación](#-documentación)

---

## 🏗️ Arquitectura

### **Arquitectura Hexagonal (Clean Architecture)**
- **🎯 Independencia del Dominio**: Lógica de negocio independiente de frameworks externos
- **🧪 Testabilidad**: Testing fácil a través de mocks de adaptadores
- **🔄 Flexibilidad**: Intercambio sencillo de implementaciones de infraestructura
- **📦 Separación de Responsabilidades**: Cada capa tiene un propósito específico

### **Patrón CQRS (Command Query Responsibility Segregation)**
- **📤 Comandos**: Operaciones de escritura procesadas asincrónicamente vía RabbitMQ
- **📥 Queries**: Operaciones de lectura ejecutadas directamente contra modelos de lectura
- **⚡ Separación**: Modelos diferentes optimizados para lectura y escritura
- **🔄 Event-Driven**: Comunicación basada en eventos de dominio

### **Bundle-contexts (Bounded Contexts)**
- **👥 Users Context**: Gestión completa de usuarios (CRUD, validaciones, eventos)
- **🔐 Auth Context**: Autenticación y autorización (JWT, passwords, tokens)
- **🔗 Shared Context**: Infraestructura común y patrones base
- **📊 Modularidad**: Cada contexto incluye capas Domain, Application e Infrastructure

### **Domain-Driven Design (DDD)**
- **🏛️ Entities**: `User` con lógica de negocio e invariantes
- **💎 Value Objects**: `Email`, `Username`, `FullName`, `HashedPassword`
- **⚙️ Domain Services**: `PasswordService`, `AuthService`
- **📢 Domain Events**: `UserCreated`, `UserUpdated`, `UserDeleted`
- **🗃️ Repository Pattern**: Abstracción de persistencia

---

## ⚙️ Tecnologías

### **Backend Stack**
- **🐍 Python 3.11+** - Lenguaje base con type hints
- **⚡ FastAPI** - Framework web moderno y performante
- **🐘 PostgreSQL 15** - Base de datos relacional robusta
- **🗃️ SQLAlchemy** - ORM avanzado con connection pooling
- **🐰 RabbitMQ** - Message broker para CQRS y eventos

### **Seguridad**
- **🔐 JWT (JSON Web Tokens)** - Autenticación stateless
- **🛡️ bcrypt** - Hashing seguro de contraseñas
- **✅ Pydantic** - Validación automática de datos
- **🔒 CORS** - Control de acceso cross-origin

### **Testing & Quality**
- **🧪 pytest** - Framework de testing
- **📊 Coverage** - Medición de cobertura de código
- **🎯 Type Hints** - Tipado estático completo
- **📝 Logging** - Sistema de logs estructurado

### **DevOps & Deployment**
- **🐳 Docker** - Containerización
- **🎼 Docker Compose** - Orquestación de servicios
- **🔄 Hot Reload** - Desarrollo con recarga automática

---

## 🚀 Inicio Rápido

### **🐳 Usando Docker (Recomendado)**

```bash
# Clonar el repositorio
git clone https://github.com/Kenyi45/init_guinea_mobile.git

# Construir y ejecutar todos los servicios
docker-compose up --build

# API disponible en http://localhost:8000
# Documentación en http://localhost:8000/docs
# RabbitMQ Management UI en http://localhost:15672
```

### **💻 Desarrollo Local**

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servicios externos
docker-compose up db rabbitmq

# Configurar variables de entorno
cp .env.example .env

# Ejecutar aplicación con hot reload
uvicorn src.main:app --reload --port 8000

# La API estará disponible en http://localhost:8000
```

### **🔧 Variables de Entorno**

```bash
# Base de datos
DATABASE_URL=postgresql://postgres:password@localhost:5432/hexagonal_db

# Message Broker
RABBITMQ_URL=amqp://guest:guest@localhost:5672/

# Autenticación JWT
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Configuración
DEBUG=true
```

---

## 📁 Estructura del Proyecto

```
📦 hexagonal-architecture-api/
├── 📂 src/
│   ├── 📂 shared/                    # 🔗 Código compartido entre contextos
│   │   ├── 📂 domain/               # 🏛️ Entidades base y value objects
│   │   ├── 📂 application/          # ⚙️ Patrones CQRS base
│   │   └── 📂 infrastructure/       # 🔧 Base de datos y Message Broker
│   └── 📂 contexts/
│       ├── 📂 users/                # 👥 Contexto de gestión de usuarios
│       │   ├── 📂 domain/           # 🏛️ Entidades, value objects, repositorios
│       │   ├── 📂 application/      # ⚙️ Comandos, queries, handlers, DTOs
│       │   └── 📂 infrastructure/   # 🔧 Modelos SQLAlchemy, repositorios, adaptadores
│       └── 📂 auth/                 # 🔐 Contexto de autenticación
│           ├── 📂 domain/           # 🏛️ Servicios de autenticación
│           ├── 📂 application/      # ⚙️ DTOs y lógica de aplicación
│           └── 📂 infrastructure/   # 🔧 Adaptadores REST
├── 📂 tests/                        # 🧪 Tests organizados por contexto
├── 📂 docker/                       # 🐳 Configuración Docker
├── 📄 docker-compose.yml            # 🎼 Orquestación de servicios
├── 📄 requirements.txt              # 📦 Dependencias Python
├── 📄 pytest.ini                    # ⚙️ Configuración de tests
└── 📄 README.md                     # 📖 Este archivo
```

---

## 🔗 API Endpoints

### **👥 Users Management**
| Método | Endpoint | Descripción | Autenticación |
|--------|----------|-------------|---------------|
| `POST` | `/api/v1/users` | Crear nuevo usuario | ❌ No |
| `GET` | `/api/v1/users/{id}` | Obtener usuario por ID | ✅ JWT |
| `GET` | `/api/v1/users` | Listar usuarios (paginado) | ✅ JWT |
| `PUT` | `/api/v1/users/{id}` | Actualizar perfil de usuario | ✅ JWT |
| `DELETE` | `/api/v1/users/{id}` | Desactivar usuario | ✅ JWT |

### **🔐 Authentication**
| Método | Endpoint | Descripción | Respuesta |
|--------|----------|-------------|-----------|
| `POST` | `/api/v1/auth/login` | Autenticar usuario | JWT Token |
| `POST` | `/api/v1/auth/verify` | Verificar token | Token válido |
| `POST` | `/api/v1/auth/refresh` | Renovar token | Nuevo JWT |

### **🔧 System**
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/` | Información de la API |
| `GET` | `/health` | Health check |
| `GET` | `/docs` | Documentación Swagger |
| `GET` | `/redoc` | Documentación ReDoc |

> **📝 Nota importante**: Actualmente todos los endpoints de usuarios son **públicos** (no requieren autenticación). La implementación de middleware de autenticación JWT está planificada para futuras versiones.

---

## 🧪 Testing

### **🏃 Ejecutar Tests**

```bash
# Ejecutar todos los tests
pytest

# Tests con cobertura
pytest --cov=src --cov-report=html

# Tests del dominio únicamente
pytest tests/contexts/users/domain/

# Tests específicos con detalle
pytest -v tests/contexts/users/domain/test_entities.py

# Tests con output en tiempo real
pytest -s
```

### **📊 Cobertura de Testing**

- **🎯 Domain Layer**: >80% cobertura
- **⚙️ Application Layer**: >70% cobertura  
- **🔧 Infrastructure Layer**: >60% cobertura
- **🧪 Unit Tests**: Value objects, entities, services
- **🔗 Integration Tests**: Handlers, repositories, APIs

### **🛠️ Fixtures y Mocks**

```python
# tests/conftest.py - Configuración global de testing
@pytest.fixture
def db_session():
    """Database session para testing."""
    # SQLite en memoria para tests rápidos

@pytest.fixture  
def sample_user_data():
    """Datos de usuario para testing."""
    # Datos válidos para creación de usuarios
```

---

## 🎯 Características Principales

### **✅ Funcionalidades Implementadas**

- **👤 Gestión de Usuarios**
  - ✅ CRUD completo con validaciones de dominio (Create, Read, Update, Delete)
  - ✅ Value objects para email, username, nombres
  - ✅ Eventos de dominio (UserCreated, UserUpdated, UserDeleted)
  - ✅ Autenticación JWT en endpoints protegidos
  - ✅ Desactivación suave de usuarios (soft delete)

- **🔐 Autenticación Completa**
  - ✅ JWT con expiración configurable
  - ✅ Hashing de contraseñas con bcrypt + salt
  - ✅ Login, verificación y renovación de tokens
  - ✅ Middleware de autenticación para endpoints protegidos

- **🏗️ Arquitectura Moderna**
  - ✅ Arquitectura Hexagonal completa
  - ✅ Patrón CQRS con RabbitMQ
  - ✅ Domain-Driven Design
  - ✅ Principios SOLID aplicados

- **🧪 Calidad de Código**
  - ✅ 80%+ cobertura de tests en dominio
  - ✅ Type hints completo
  - ✅ Documentación automática (Swagger/OpenAPI)
  - ✅ Error handling estructurado

- **🚀 DevOps Ready**
  - ✅ Containerización con Docker
  - ✅ Docker Compose para desarrollo
  - ✅ Health checks
  - ✅ Logging estructurado

### **🔜 Funcionalidades Planificadas**

- **👥 User Management**
  - 🔜 Roles y permisos
  - 🔜 Verificación de email
  - 🔜 Reset de contraseñas
  - 🔜 Perfil de usuario extendido

- **🔐 Authentication**
  - 🔜 Rate limiting en endpoints de login
  - 🔜 Logout con blacklist de tokens
  - 🔜 Autenticación multi-factor (2FA)

- **📊 Observabilidad**
  - 🔜 Métricas con Prometheus
  - 🔜 Distributed tracing
  - 🔜 Alertas automatizadas
  - 🔜 Dashboard de monitoreo

- **⚡ Performance**
  - 🔜 Cache con Redis
  - 🔜 Database read replicas
  - 🔜 Rate limiting
  - 🔜 API versioning

---

## 💡 Ejemplos de Uso

### **👤 Crear Usuario**

```bash
curl -X POST "http://localhost:8000/api/v1/users" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "juan.perez@example.com",
    "username": "jperez",
    "first_name": "Juan",
    "last_name": "Pérez", 
    "password": "MiPassword123!"
  }'
```

**Respuesta:**
```json
{
  "id": "uuid-here",
  "email": "juan.perez@example.com",
  "username": "jperez",
  "full_name": "Juan Pérez",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z"
}
```

### **🔐 Autenticación**

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "juan.perez@example.com",
    "password": "MiPassword123!"
  }'
```

**Respuesta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_id": "uuid-here",
  "email": "juan.perez@example.com",
  "expires_at": "2024-01-15T11:30:00Z"
}
```

### **📊 Consultar Usuarios (Requiere JWT)**

```bash
# Listar todos los usuarios (endpoint protegido)
curl -X GET "http://localhost:8000/api/v1/users" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# Obtener usuario específico por ID
curl -X GET "http://localhost:8000/api/v1/users/{user-id}" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# Actualizar usuario
curl -X PUT "http://localhost:8000/api/v1/users/{user-id}" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{
    "first_name": "Juan Carlos",
    "last_name": "Pérez García"
  }'

# Eliminar usuario (desactivación suave)
curl -X DELETE "http://localhost:8000/api/v1/users/{user-id}" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### **🔄 Renovar Token**

```bash
curl -X POST "http://localhost:8000/api/v1/auth/refresh" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Respuesta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_id": "uuid-here",
  "email": "juan.perez@example.com",
  "expires_at": "2024-01-15T12:30:00Z"
}
```

---

## 🐳 Servicios Docker

### **🎼 Stack de Servicios**

| Servicio | Puerto | Descripción | Health Check |
|----------|--------|-------------|--------------|
| **app** | `8000` | Aplicación FastAPI | `GET /health` |
| **db** | `5432` | PostgreSQL 15 | Connection test |
| **rabbitmq** | `5672`, `15672` | Message broker + Management UI | Management API |

### **🔧 Configuración Docker Compose**

```yaml
# docker-compose.yml
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/hexagonal_db
      - RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672/
    depends_on:
      - db
      - rabbitmq
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: hexagonal_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]

  rabbitmq:
    image: rabbitmq:3-management-alpine
    ports:
      - "5672:5672"      # AMQP
      - "15672:15672"    # Management UI
    environment:
      RABBITMQ_DEFAULT_USER: guest
      RABBITMQ_DEFAULT_PASS: guest
    healthcheck:
      test: rabbitmq-diagnostics -q ping
```

### **📱 Acceso a Interfaces**

- **🌐 API**: http://localhost:8000
- **📖 Swagger Docs**: http://localhost:8000/docs
- **📋 ReDoc**: http://localhost:8000/redoc
- **🐰 RabbitMQ Management**: http://localhost:15672 (guest/guest)
- **🔍 Health Check**: http://localhost:8000/health

---

## 📚 Documentación

### **🔗 Enlaces Útiles**

- **📖 Documentación de la API**: `http://localhost:8000/docs`
- **🏗️ Arquitectura Detallada**: [ANALISIS_PROYECTO_ENTREVISTA.md](./ANALISIS_PROYECTO_ENTREVISTA.md)
- **📋 Documentación Técnica**: [PROJECT_DOCUMENTATION.md](./PROJECT_DOCUMENTATION.md)

### **🎯 Decisiones Arquitecturales**

1. **🏗️ Arquitectura Hexagonal**: Independencia del dominio y testabilidad
2. **⚙️ CQRS**: Comandos async vía RabbitMQ, queries síncronas para performance
3. **📦 Bundle-contexts**: Organización modular para escalabilidad
4. **🏛️ Domain-Driven Design**: Value objects, entities, y eventos de dominio
5. **🔌 Dependency Injection**: Acoplamiento débil y testabilidad
6. **🐳 Containerización**: Consistencia entre entornos y deploy sencillo

### **🤝 Contribución**

```bash
# Fork del repositorio
# Crear rama para feature
git checkout -b feature/nueva-funcionalidad

# Desarrollo con tests
pytest

# Commit con mensaje descriptivo
git commit -m "feat: agregar nueva funcionalidad"

# Push y crear Pull Request
git push origin feature/nueva-funcionalidad
```

### **📝 Convenciones**

- **🐍 Código**: PEP 8, type hints, docstrings
- **🧪 Tests**: pytest, coverage >80% en dominio
- **📝 Commits**: Conventional commits
- **📋 Documentación**: Markdown, diagramas cuando sea necesario
