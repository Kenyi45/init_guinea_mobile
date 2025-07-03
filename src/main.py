from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from src.shared.infrastructure.database import create_tables
from src.contexts.users.infrastructure.adapters import router as users_router
from src.contexts.auth.infrastructure.adapters import router as auth_router
from src.shared.infrastructure.metrics import get_metrics, get_content_type
from src.shared.infrastructure.metrics_middleware import PrometheusMiddleware
import logging


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Hexagonal Architecture API",
    description="A FastAPI application using Hexagonal Architecture, CQRS, and Bundle-contexts",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add Prometheus metrics middleware
app.add_middleware(PrometheusMiddleware)

# Include routers
app.include_router(users_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1")


@app.on_event("startup")
async def startup_event():
    """Initialize the application."""
    logger.info("Starting Hexagonal Architecture API...")
    
    # Create database tables
    create_tables()
    logger.info("Database tables created")
    
    logger.info("Application started successfully")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown."""
    logger.info("Shutting down Hexagonal Architecture API...")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Hexagonal Architecture API",
        "version": "1.0.0",
        "architecture": "Hexagonal with CQRS and Bundle-contexts"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "API is running correctly"}


@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint."""
    return Response(
        content=get_metrics(),
        media_type=get_content_type()
    ) 