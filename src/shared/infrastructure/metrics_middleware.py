from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from src.shared.infrastructure.metrics import record_http_request
import time
import logging


logger = logging.getLogger(__name__)


class PrometheusMiddleware(BaseHTTPMiddleware):
    """Middleware to automatically record HTTP metrics for all requests."""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next):
        """Process request and record metrics."""
        start_time = time.time()
        method = request.method
        path = request.url.path
        
        # Clean up the path for metrics (remove query params and specific IDs)
        endpoint = self._normalize_endpoint(path)
        
        try:
            response = await call_next(request)
            status_code = response.status_code
        except Exception as e:
            # Record error metrics
            duration = time.time() - start_time
            record_http_request(method, endpoint, 500, duration)
            logger.error(f"Request failed: {method} {path} - {str(e)}")
            raise
        
        # Record successful request metrics
        duration = time.time() - start_time
        record_http_request(method, endpoint, status_code, duration)
        
        # Add response headers with metrics info
        response.headers["X-Response-Time"] = str(duration)
        
        return response
    
    def _normalize_endpoint(self, path: str) -> str:
        """Normalize endpoint path for metrics to avoid high cardinality."""
        # Remove trailing slash
        if path.endswith('/') and len(path) > 1:
            path = path[:-1]
        
        # Replace UUIDs and numeric IDs with placeholders
        import re
        
        # Replace UUIDs (e.g., /api/v1/users/123e4567-e89b-12d3-a456-426614174000)
        path = re.sub(
            r'/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}',
            '/{id}',
            path,
            flags=re.IGNORECASE
        )
        
        # Replace numeric IDs (e.g., /api/v1/users/123)
        path = re.sub(r'/\d+', '/{id}', path)
        
        # Keep meaningful endpoints, generalize others
        known_endpoints = [
            '/api/v1/users',
            '/api/v1/users/{id}',
            '/api/v1/auth/login',
            '/api/v1/auth/verify',
            '/api/v1/auth/refresh',
            '/',
            '/health',
            '/metrics',
            '/docs',
            '/redoc',
            '/openapi.json'
        ]
        
        if path in known_endpoints:
            return path
        
        # For unknown endpoints, use a generic label
        if path.startswith('/api/'):
            return '/api/unknown'
        
        return '/unknown' 