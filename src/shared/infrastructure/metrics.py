from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from typing import Dict, Any
import time
import logging
from functools import wraps


logger = logging.getLogger(__name__)


# =============================================================================
# HTTP METRICS
# =============================================================================

# HTTP request counter
http_requests_total = Counter(
    'http_requests_total',
    'Total number of HTTP requests',
    ['method', 'endpoint', 'status_code']
)

# HTTP request duration
http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)

# HTTP requests currently being processed
http_requests_in_progress = Gauge(
    'http_requests_in_progress',
    'Number of HTTP requests currently being processed'
)


# =============================================================================
# BUSINESS METRICS
# =============================================================================

# User operations
user_operations_total = Counter(
    'user_operations_total',
    'Total number of user operations',
    ['operation', 'status']
)

# Authentication attempts
auth_attempts_total = Counter(
    'auth_attempts_total',
    'Total number of authentication attempts',
    ['status']
)

# JWT tokens issued
jwt_tokens_issued_total = Counter(
    'jwt_tokens_issued_total',
    'Total number of JWT tokens issued'
)

# Active users gauge
active_users_total = Gauge(
    'active_users_total',
    'Total number of active users'
)


# =============================================================================
# DATABASE METRICS
# =============================================================================

# Database operations
db_operations_total = Counter(
    'db_operations_total',
    'Total number of database operations',
    ['operation', 'table', 'status']
)

# Database connection pool
db_connections_active = Gauge(
    'db_connections_active',
    'Number of active database connections'
)

# Database operation duration
db_operation_duration_seconds = Histogram(
    'db_operation_duration_seconds',
    'Database operation duration in seconds',
    ['operation', 'table']
)


# =============================================================================
# RABBITMQ METRICS
# =============================================================================

# Messages published
messages_published_total = Counter(
    'messages_published_total',
    'Total number of messages published to RabbitMQ',
    ['queue', 'status']
)

# Messages consumed
messages_consumed_total = Counter(
    'messages_consumed_total',
    'Total number of messages consumed from RabbitMQ',
    ['queue', 'status']
)

# Queue depth
queue_depth = Gauge(
    'queue_depth',
    'Current depth of RabbitMQ queues',
    ['queue']
)


# =============================================================================
# APPLICATION METRICS
# =============================================================================

# Application errors
application_errors_total = Counter(
    'application_errors_total',
    'Total number of application errors',
    ['error_type', 'component']
)

# Command processing
command_processing_total = Counter(
    'command_processing_total',
    'Total number of commands processed',
    ['command_type', 'status']
)

# Query processing
query_processing_total = Counter(
    'query_processing_total',
    'Total number of queries processed',
    ['query_type', 'status']
)


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def record_http_request(method: str, endpoint: str, status_code: int, duration: float):
    """Record HTTP request metrics."""
    http_requests_total.labels(
        method=method,
        endpoint=endpoint,
        status_code=status_code
    ).inc()
    
    http_request_duration_seconds.labels(
        method=method,
        endpoint=endpoint
    ).observe(duration)


def record_user_operation(operation: str, status: str):
    """Record user operation metrics."""
    user_operations_total.labels(
        operation=operation,
        status=status
    ).inc()


def record_auth_attempt(status: str):
    """Record authentication attempt metrics."""
    auth_attempts_total.labels(status=status).inc()


def record_jwt_token_issued():
    """Record JWT token issued metric."""
    jwt_tokens_issued_total.inc()


def record_db_operation(operation: str, table: str, status: str, duration: float = None):
    """Record database operation metrics."""
    db_operations_total.labels(
        operation=operation,
        table=table,
        status=status
    ).inc()
    
    if duration is not None:
        db_operation_duration_seconds.labels(
            operation=operation,
            table=table
        ).observe(duration)


def record_message_published(queue: str, status: str):
    """Record message published metrics."""
    messages_published_total.labels(
        queue=queue,
        status=status
    ).inc()


def record_message_consumed(queue: str, status: str):
    """Record message consumed metrics."""
    messages_consumed_total.labels(
        queue=queue,
        status=status
    ).inc()


def record_application_error(error_type: str, component: str):
    """Record application error metrics."""
    application_errors_total.labels(
        error_type=error_type,
        component=component
    ).inc()


def record_command_processing(command_type: str, status: str):
    """Record command processing metrics."""
    command_processing_total.labels(
        command_type=command_type,
        status=status
    ).inc()


def record_query_processing(query_type: str, status: str):
    """Record query processing metrics."""
    query_processing_total.labels(
        query_type=query_type,
        status=status
    ).inc()


def update_active_users_count(count: int):
    """Update active users count."""
    active_users_total.set(count)


def update_queue_depth(queue: str, depth: int):
    """Update queue depth metric."""
    queue_depth.labels(queue=queue).set(depth)


def get_metrics() -> str:
    """Get all metrics in Prometheus format."""
    return generate_latest()


def get_content_type() -> str:
    """Get the content type for metrics."""
    return CONTENT_TYPE_LATEST


# =============================================================================
# DECORATORS
# =============================================================================

def monitor_endpoint(endpoint_name: str = None):
    """Decorator to monitor HTTP endpoint performance."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            http_requests_in_progress.inc()
            
            try:
                result = await func(*args, **kwargs)
                status_code = getattr(result, 'status_code', 200)
                status = 'success'
            except Exception as e:
                status_code = 500
                status = 'error'
                record_application_error(
                    error_type=type(e).__name__,
                    component='http_endpoint'
                )
                raise
            finally:
                duration = time.time() - start_time
                http_requests_in_progress.dec()
                
                # Try to get method from request context or default to 'unknown'
                method = 'unknown'
                endpoint = endpoint_name or func.__name__
                
                record_http_request(method, endpoint, status_code, duration)
                
            return result
        return wrapper
    return decorator


def monitor_command(command_type: str):
    """Decorator to monitor command processing."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                result = await func(*args, **kwargs)
                record_command_processing(command_type, 'success')
                return result
            except Exception as e:
                record_command_processing(command_type, 'error')
                record_application_error(
                    error_type=type(e).__name__,
                    component='command_handler'
                )
                raise
        return wrapper
    return decorator


def monitor_query(query_type: str):
    """Decorator to monitor query processing."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                result = await func(*args, **kwargs)
                record_query_processing(query_type, 'success')
                return result
            except Exception as e:
                record_query_processing(query_type, 'error')
                record_application_error(
                    error_type=type(e).__name__,
                    component='query_handler'
                )
                raise
        return wrapper
    return decorator


def monitor_db_operation(operation: str, table: str):
    """Decorator to monitor database operations."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                duration = time.time() - start_time
                record_db_operation(operation, table, 'success', duration)
                return result
            except Exception as e:
                duration = time.time() - start_time
                record_db_operation(operation, table, 'error', duration)
                record_application_error(
                    error_type=type(e).__name__,
                    component='database'
                )
                raise
        return wrapper
    return decorator 