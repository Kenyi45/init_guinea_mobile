# 📊 Dashboard de Métricas - Guía Completa

## 🚀 Configuración del Dashboard

### 1. **Levantar el Stack Completo**

```bash
# Construir y levantar todos los servicios
docker-compose up -d

# Verificar que todos los servicios estén corriendo
docker-compose ps
```

### 2. **Acceder a los Servicios**

| Servicio | URL | Credenciales |
|----------|-----|-------------|
| **API** | http://localhost:8000 | N/A |
| **Grafana** | http://localhost:3000 | admin / admin123 |
| **Prometheus** | http://localhost:9090 | N/A |
| **RabbitMQ** | http://localhost:15672 | guest / guest |

### 3. **Verificar Métricas**

```bash
# Verificar que las métricas están disponibles
curl http://localhost:8000/metrics

# Verificar que Prometheus está scrapeando
curl http://localhost:9090/api/v1/targets
```

## 📈 **Métricas Disponibles**

### **HTTP Metrics**
- `http_requests_total` - Total de requests por método/endpoint/status
- `http_request_duration_seconds` - Latencia de requests
- `http_requests_in_progress` - Requests en progreso

### **Business Metrics**
- `user_operations_total` - Operaciones de usuario por tipo/status
- `auth_attempts_total` - Intentos de autenticación
- `jwt_tokens_issued_total` - Tokens JWT emitidos
- `active_users_total` - Usuarios activos

### **Database Metrics**
- `db_operations_total` - Operaciones de BD por tabla/tipo/status
- `db_connections_active` - Conexiones activas
- `db_operation_duration_seconds` - Latencia de operaciones

### **RabbitMQ Metrics**
- `messages_published_total` - Mensajes publicados por cola
- `messages_consumed_total` - Mensajes consumidos por cola
- `queue_depth` - Profundidad de colas

### **Application Metrics**
- `application_errors_total` - Errores por tipo/componente
- `command_processing_total` - Comandos procesados
- `query_processing_total` - Queries procesadas

## 🎯 **Usando el Dashboard**

### 1. **Acceder a Grafana**
1. Ir a http://localhost:3000
2. Login: `admin` / `admin123`
3. El dashboard se carga automáticamente

### 2. **Paneles Disponibles**

#### **📊 Paneles de Performance**
- **HTTP Requests Total**: Requests por segundo
- **HTTP Request Duration**: Percentiles de latencia
- **HTTP Requests by Status Code**: Distribución por códigos
- **HTTP Requests by Endpoint**: Tráfico por endpoint

#### **👥 Paneles de Negocio**
- **User Operations**: Operaciones CRUD de usuarios
- **Authentication Attempts**: Intentos de login
- **Active Users**: Usuarios activos en tiempo real

#### **🗄️ Paneles de Infraestructura**
- **Database Operations**: Operaciones de BD
- **Active Database Connections**: Conexiones activas
- **RabbitMQ Messages**: Mensajes publicados/consumidos

#### **⚠️ Paneles de Monitoreo**
- **Application Errors**: Errores por tipo y componente

### 3. **Generar Tráfico para Ver Métricas**

```bash
# Generar tráfico HTTP
for i in {1..10}; do curl http://localhost:8000/health; done

# Crear usuarios (genera métricas de negocio)
curl -X POST http://localhost:8000/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "first_name": "Test",
    "last_name": "User", 
    "password": "password123"
  }'

# Intentar login (genera métricas de auth)
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

## 🔧 **Configuración Avanzada**

### **Personalizar Dashboards**
1. Editar `monitoring/grafana/dashboards/hexagonal-api-dashboard.json`
2. Reiniciar Grafana: `docker-compose restart grafana`

### **Ajustar Intervalos de Scraping**
1. Editar `monitoring/prometheus.yml`
2. Reiniciar Prometheus: `docker-compose restart prometheus`

### **Agregar Alertas**
```yaml
# En prometheus.yml
rule_files:
  - "alerts.yml"

# Crear monitoring/alerts.yml
groups:
  - name: api_alerts
    rules:
      - alert: HighErrorRate
        expr: sum(rate(http_requests_total{status_code=~"5.."}[5m])) > 0.1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High error rate detected"
```

## 📱 **Opciones Adicionales**

### **Opción 1: Usar Prometheus Standalone**
```bash
# Solo Prometheus (sin Grafana)
docker run -p 9090:9090 \
  -v ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus:latest
```

### **Opción 2: Integrar con Sistemas Existentes**
```yaml
# docker-compose.override.yml
version: '3.8'
services:
  prometheus:
    environment:
      - PROMETHEUS_REMOTE_WRITE_URL=https://your-prometheus-server.com
```

### **Opción 3: Dashboard en la Nube**
- **Grafana Cloud**: https://grafana.com/cloud/
- **Prometheus Cloud**: https://prometheus.io/docs/operating/integrations/
- **DataDog**: Integración con métricas Prometheus

## 🎨 **Queries Útiles de Prometheus**

### **Performance Queries**
```prometheus
# Requests por segundo por endpoint
sum(rate(http_requests_total[5m])) by (endpoint)

# Latencia P95 por endpoint
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, endpoint))

# Tasa de errores
sum(rate(http_requests_total{status_code=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))
```

### **Business Queries**
```prometheus
# Usuarios creados por hora
increase(user_operations_total{operation="create",status="success"}[1h])

# Tasa de éxito de login
sum(rate(auth_attempts_total{status="success"}[5m])) / sum(rate(auth_attempts_total[5m]))

# Comandos procesados por segundo
sum(rate(command_processing_total[5m])) by (command_type)
```

## 🛠️ **Troubleshooting**

### **Problemas Comunes**

1. **Prometheus no puede scraper la app**
   ```bash
   # Verificar conectividad
   docker exec -it prometheus wget -O- http://app:8000/metrics
   ```

2. **Grafana no muestra datos**
   ```bash
   # Verificar datasource
   curl -u admin:admin123 http://localhost:3000/api/datasources
   ```

3. **Métricas no aparecen**
   ```bash
   # Verificar configuración de Prometheus
   docker exec -it prometheus promtool check config /etc/prometheus/prometheus.yml
   ```

### **Logs de Debugging**
```bash
# Ver logs de Prometheus
docker-compose logs prometheus

# Ver logs de Grafana
docker-compose logs grafana

# Ver logs de la aplicación
docker-compose logs app
```

## 📋 **Checklist de Configuración**

- [ ] ✅ Docker y Docker Compose instalados
- [ ] ✅ Puertos libres: 3000, 8000, 9090, 5432, 5672, 15672
- [ ] ✅ Servicios corriendo: `docker-compose ps`
- [ ] ✅ Métricas disponibles: `curl http://localhost:8000/metrics`
- [ ] ✅ Prometheus scrapeando: http://localhost:9090/targets
- [ ] ✅ Grafana accesible: http://localhost:3000
- [ ] ✅ Dashboard cargado automáticamente
- [ ] ✅ Datos visibles en paneles