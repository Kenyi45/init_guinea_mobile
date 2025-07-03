# 🚀 Hexagonal Architecture API

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green.svg)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)](https://www.postgresql.org)
[![RabbitMQ](https://img.shields.io/badge/RabbitMQ-3.12+-orange.svg)](https://www.rabbitmq.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com)
[![Tests](https://img.shields.io/badge/Tests-pytest-brightgreen.svg)](https://pytest.org)

> **Aplicación backend moderna** construida con **FastAPI** implementando **Arquitectura Hexagonal** y **Domain-Driven Design** siguiendo principios **SOLID**.

## 📖 Tabla de Contenidos

- [🏗️ Arquitectura](#️-arquitectura)
- [⚙️ Tecnologías](#️-tecnologías)
- [🚀 Inicio Rápido](#-inicio-rápido)
- [📁 Estructura del Proyecto](#-estructura-del-proyecto)
- [🔗 API Endpoints](#-api-endpoints)
- [🧪 Testing](#-testing)
- [🎯 Características Implementadas](#-características-implementadas)
- [🔜 Funcionalidades Planificadas](#-funcionalidades-planificadas)
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

### **Domain-Driven Design (DDD)**
- **🏛️ Entities**: `User` con lógica de negocio e invariantes
- **💎 Value Objects**: `Email`, `Username`, `FullName`, `HashedPassword`
- **⚙️ Domain Services**: `PasswordService`, `AuthService`
- **📢 Domain Events**: `UserCreated`, `UserUpdated`, `UserDeleted`
- **🗃️ Repository Pattern**: Abstracción de persistencia

### **Bundle-contexts (Bounded Contexts)**
- **👥 Users Context**: Gestión completa de usuarios (CRUD, validaciones, eventos)
- **🔐 Auth Context**: Autenticación y autorización (JWT, passwords, tokens)
- **🔗 Shared Context**: Infraestructura común y patrones base
- **📊 Modularidad**: Cada contexto incluye capas Domain, Application e Infrastructure

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
- **🎯 Type Hints** - Tipado estático completo
- **📝 Logging** - Sistema de logs estructurado

### **Monitoreo & Observabilidad**
- **📊 Prometheus** - Sistema de métricas y monitoreo
- **📈 Métricas personalizadas** - Instrumentación de negocio
- **⏱️ Performance tracking** - Métricas de latencia y throughput

### **DevOps & Deployment**
- **🐳 Docker** - Containerización
- **🎼 Docker Compose** - Orquestación de servicios
- **🔄 Hot Reload** - Desarrollo con recarga automática

---

## 🚀 Inicio Rápido

### **🐳 Usando Docker (Recomendado)**

```bash
# Clonar el repositorio
git clone <repository-url>
cd init_project

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
export DATABASE_URL=postgresql://postgres:password@localhost:5432/hexagonal_db
export RABBITMQ_URL=amqp://guest:guest@localhost:5672/
export SECRET_KEY=your-secret-key-here
export ALGORITHM=HS256
export ACCESS_TOKEN_EXPIRE_MINUTES=30

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
📦 init_project/
├── 📂 src/
│   ├── 📂 shared/                    # 🔗 Código compartido entre contextos
│   │   ├── 📂 domain/               # 🏛️ Entidades base y value objects
│   │   ├── 📂 application/          # ⚙️ Patrones CQRS base
│   │   └── 📂 infrastructure/       # 🔧 Base de datos y Message Broker
│   ├── 📂 contexts/
│   │   ├── 📂 users/                # 👥 Contexto de gestión de usuarios
│   │   │   ├── 📂 domain/           # 🏛️ Entidades, value objects, repositorios
│   │   │   ├── 📂 application/      # ⚙️ Comandos, queries, handlers, DTOs
│   │   │   └── 📂 infrastructure/   # 🔧 Modelos SQLAlchemy, repositorios, adaptadores
│   │   └── 📂 auth/                 # 🔐 Contexto de autenticación
│   │       ├── 📂 domain/           # 🏛️ Servicios de autenticación
│   │       ├── 📂 application/      # ⚙️ DTOs y lógica de aplicación
│   │       └── 📂 infrastructure/   # 🔧 Adaptadores REST
│   └── 📄 main.py                   # 🚀 Aplicación FastAPI
├── 📂 tests/                        # 🧪 Tests organizados por contexto
├── 📄 docker-compose.yml            # 🎼 Orquestación de servicios
├── 📄 Dockerfile                    # 🐳 Configuración Docker
├── 📄 requirements.txt              # 📦 Dependencias Python
├── 📄 pytest.ini                    # ⚙️ Configuración de tests
├── 📄 alembic.ini                   # 🔄 Migraciones de base de datos
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
| `GET` | `/metrics` | Métricas de Prometheus |
| `GET` | `/docs` | Documentación Swagger |
| `GET` | `/redoc` | Documentación ReDoc |

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

### **🛠️ Estructura de Testing**

- **🧪 Unit Tests**: Value objects, entities, services
- **🔗 Integration Tests**: Handlers, repositories, APIs
- **📊 Domain Tests**: Lógica de negocio y invariantes
- **🔐 Authentication Tests**: Flujo completo de autenticación

---

## 🎯 Características Implementadas

### **✅ Funcionalidades Completadas**

- **👤 Gestión de Usuarios**
  - ✅ CRUD completo con validaciones de dominio
  - ✅ Value objects para email, username, nombres
  - ✅ Domain events (UserCreated, UserUpdated, UserDeleted)
  - ✅ Desactivación suave de usuarios (soft delete)
  - ✅ Validación de duplicados (email, username)

- **🔐 Autenticación Completa**
  - ✅ JWT con expiración configurable
  - ✅ Hashing de contraseñas con bcrypt + salt
  - ✅ Login, verificación y renovación de tokens
  - ✅ Middleware de autenticación para endpoints protegidos

- **🏗️ Arquitectura Hexagonal**
  - ✅ Separación clara de capas (Domain, Application, Infrastructure)
  - ✅ Repository pattern con abstracción
  - ✅ Domain-Driven Design con entities y value objects
  - ✅ Principios SOLID aplicados

- **🧪 Testing**
  - ✅ Tests unitarios para value objects y entities
  - ✅ Tests de integración para handlers
  - ✅ Tests de API endpoints
  - ✅ Fixtures para datos de prueba

- **🚀 DevOps**
  - ✅ Containerización con Docker
  - ✅ Docker Compose para desarrollo
  - ✅ Logging estructurado
  - ✅ Type hints completo
  - ✅ Variables de entorno configuradas (example.env)

- **📊 Monitoreo y Observabilidad**
  - ✅ Métricas con Prometheus implementadas
  - ✅ Instrumentación completa de HTTP requests
  - ✅ Métricas de negocio (usuarios, autenticación, comandos)
  - ✅ Métricas de base de datos y RabbitMQ
  - ✅ Endpoint /metrics expuesto

- **🔄 CQRS y Mensajería**
  - ✅ CQRS completamente implementado
  - ✅ RabbitMQ integrado para procesamiento asíncrono
  - ✅ EventBus real conectado a RabbitMQ
  - ✅ Consumers configurados para comandos
  - ✅ Eventos de dominio procesados asincrónicamente

### **⚠️ Limitaciones Actuales**

- **🔍 Cobertura de Tests**: No hay medición automática de cobertura de código
- **🛡️ Rate Limiting**: No hay límites de velocidad en endpoints
- **📱 Healthchecks**: Los servicios Docker no tienen healthchecks configurados
- **🔐 Validación de JWT**: Falta validación de expiración en algunos endpoints

**Respuesta:**
```json
{
  "id": "uuid-here",
  "email": "juan.perez@example.com",
  "username": "jperez",
  "first_name": "Juan",
  "last_name": "Pérez",
  "full_name": "Juan Pérez",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
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

| Servicio | Puerto | Descripción |
|----------|--------|-------------|
| **app** | `8000` | Aplicación FastAPI |
| **db** | `5432` | PostgreSQL 15 |
| **rabbitmq** | `5672`, `15672` | Message broker + Management UI |

### **🔧 Configuración Docker Compose**

```yaml
# docker-compose.yml
version: '3.8'

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
    volumes:
      - .:/app

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: hexagonal_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  rabbitmq:
    image: rabbitmq:3-management-alpine
    ports:
      - "5672:5672"      # AMQP
      - "15672:15672"    # Management UI
    environment:
      RABBITMQ_DEFAULT_USER: guest
      RABBITMQ_DEFAULT_PASS: guest
    volumes:
      - rabbitmq_data:/var/lib/rabbitmq

volumes:
  postgres_data:
  rabbitmq_data:
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
- **🏗️ Análisis del Proyecto**: [ANALISIS_PROYECTO_ENTREVISTA.md](./ANALISIS_PROYECTO_ENTREVISTA.md)

### **🎯 Decisiones Arquitecturales**

1. **🏗️ Arquitectura Hexagonal**: Independencia del dominio y testabilidad
2. **📦 Bundle-contexts**: Organización modular para escalabilidad
3. **🏛️ Domain-Driven Design**: Value objects, entities, y eventos de dominio
4. **🔌 Dependency Injection**: Acoplamiento débil y testabilidad
5. **🐳 Containerización**: Consistencia entre entornos y deploy sencillo

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
- **🧪 Tests**: pytest, cobertura en componentes críticos
- **📝 Commits**: Conventional commits
- **📋 Documentación**: Markdown, diagramas cuando sea necesario

---

## 🚀 Tecnologías Utilizadas

**Core:**
- Python 3.11 + FastAPI
- PostgreSQL + SQLAlchemy
- RabbitMQ (preparado)
- JWT + bcrypt
- Docker + Docker Compose

**Testing:**
- pytest + pytest-asyncio
- pytest-cov
- httpx (para tests de API)

**Arquitectura:**
- Hexagonal Architecture
- Domain-Driven Design
- Repository Pattern
- Dependency Injection

---

*Este proyecto demuestra una implementación sólida de arquitectura hexagonal con FastAPI, ideal para aplicaciones empresariales que requieren mantenibilidad y escalabilidad.*
