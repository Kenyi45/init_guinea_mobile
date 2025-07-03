#!/bin/bash

# Script para generar tráfico y ver métricas
set -e

BASE_URL="http://localhost:8000"
GRAFANA_URL="http://localhost:3000"
PROMETHEUS_URL="http://localhost:9090"

echo "🚀 Generador de Tráfico para Métricas"
echo "======================================"

# Verificar que la API esté disponible
check_api() {
    echo "🔍 Verificando disponibilidad de la API..."
    if curl -s "$BASE_URL/health" > /dev/null; then
        echo "✅ API disponible en $BASE_URL"
    else
        echo "❌ API no disponible en $BASE_URL"
        echo "💡 Asegúrate de que docker-compose esté ejecutándose"
        exit 1
    fi
}

# Mostrar servicios disponibles
show_services() {
    echo ""
    echo "🌐 Servicios disponibles:"
    echo "- API: $BASE_URL"
    echo "- Grafana: $GRAFANA_URL (admin/admin123)"
    echo "- Prometheus: $PROMETHEUS_URL"
    echo "- RabbitMQ: http://localhost:15672 (guest/guest)"
    echo ""
}

# Generar tráfico HTTP
generate_http_traffic() {
    echo "🌐 Generando tráfico HTTP..."
    
    for i in {1..20}; do
        echo "📊 Request $i/20"
        curl -s "$BASE_URL/health" > /dev/null
        curl -s "$BASE_URL/metrics" > /dev/null
        curl -s "$BASE_URL/api/v1/users" > /dev/null 2>&1 || true
        sleep 0.5
    done
    
    echo "✅ Tráfico HTTP generado"
}

# Crear usuarios de prueba
create_test_users() {
    echo "👥 Creando usuarios de prueba..."
    
    for i in {1..3}; do
        echo "👤 Creando usuario $i..."
        curl -s -X POST "$BASE_URL/api/v1/users" \
            -H "Content-Type: application/json" \
            -d "{
                \"email\": \"test$i@example.com\",
                \"username\": \"testuser$i\",
                \"first_name\": \"Test$i\",
                \"last_name\": \"User$i\",
                \"password\": \"password123\"
            }" > /dev/null || echo "⚠️ Usuario $i falló (puede ser que ya exista)"
        sleep 1
    done
    
    echo "✅ Usuarios de prueba creados"
}

# Probar autenticación
test_authentication() {
    echo "🔐 Probando autenticación..."
    
    # Intentos correctos
    for i in {1..2}; do
        echo "🔑 Intento de login exitoso $i..."
        curl -s -X POST "$BASE_URL/api/v1/auth/login" \
            -H "Content-Type: application/json" \
            -d "{
                \"email\": \"test$i@example.com\",
                \"password\": \"password123\"
            }" > /dev/null || echo "⚠️ Login falló (usuario puede no existir)"
        sleep 1
    done
    
    # Intentos incorrectos
    for i in {1..3}; do
        echo "❌ Intento de login fallido $i..."
        curl -s -X POST "$BASE_URL/api/v1/auth/login" \
            -H "Content-Type: application/json" \
            -d "{
                \"email\": \"test$i@example.com\",
                \"password\": \"wrongpassword\"
            }" > /dev/null || true
        sleep 1
    done
    
    echo "✅ Pruebas de autenticación completadas"
}

# Mostrar métricas actuales
show_metrics() {
    echo "📈 Métricas actuales:"
    echo "==================="
    
    # Obtener métricas y filtrar las importantes
    metrics=$(curl -s "$BASE_URL/metrics")
    
    echo "🌐 HTTP Requests:"
    echo "$metrics" | grep "http_requests_total" | grep -v "^#"
    
    echo ""
    echo "👥 User Operations:"
    echo "$metrics" | grep "user_operations_total" | grep -v "^#"
    
    echo ""
    echo "🔐 Auth Attempts:"
    echo "$metrics" | grep "auth_attempts_total" | grep -v "^#"
    
    echo ""
    echo "🗃️ Database Operations:"
    echo "$metrics" | grep "db_operations_total" | grep -v "^#"
    
    echo ""
    echo "⚠️ Application Errors:"
    echo "$metrics" | grep "application_errors_total" | grep -v "^#"
    
    echo ""
    echo "🎯 Para ver métricas completas: curl $BASE_URL/metrics"
}

# Ejecutar todo automáticamente
run_all() {
    echo "🚀 Ejecutando secuencia completa..."
    
    create_test_users
    echo ""
    
    test_authentication
    echo ""
    
    generate_http_traffic
    echo ""
    
    show_metrics
    echo ""
    
    echo "🎉 Secuencia completa ejecutada"
    echo "📊 Abre Grafana en: $GRAFANA_URL"
}

# Mostrar ayuda
show_help() {
    echo "📋 Uso: $0 [opción]"
    echo ""
    echo "Opciones:"
    echo "  check       - Verificar que la API esté disponible"
    echo "  services    - Mostrar servicios disponibles"
    echo "  http        - Generar tráfico HTTP"
    echo "  users       - Crear usuarios de prueba"
    echo "  auth        - Probar autenticación"
    echo "  metrics     - Mostrar métricas actuales"
    echo "  all         - Ejecutar todo automáticamente"
    echo "  help        - Mostrar esta ayuda"
    echo ""
    echo "🎯 Para dashboard visual: $GRAFANA_URL"
}

# Menú principal
main() {
    case "${1:-help}" in
        "check")
            check_api
            ;;
        "services")
            show_services
            ;;
        "http")
            check_api
            generate_http_traffic
            ;;
        "users")
            check_api
            create_test_users
            ;;
        "auth")
            check_api
            test_authentication
            ;;
        "metrics")
            check_api
            show_metrics
            ;;
        "all")
            check_api
            show_services
            run_all
            ;;
        "help"|*)
            show_help
            ;;
    esac
}

# Ejecutar función principal
main "$@" 