#!/bin/bash

# Script para configurar y verificar el dashboard de Grafana
set -e

echo "🚀 Configurando Dashboard de Grafana"
echo "===================================="

# Verificar que docker-compose esté ejecutándose
check_services() {
    echo "🔍 Verificando servicios..."
    
    if ! docker-compose ps | grep -q "Up"; then
        echo "❌ Los servicios no están ejecutándose"
        echo "💡 Ejecutando: docker-compose up -d"
        docker-compose up -d
        sleep 10
    else
        echo "✅ Servicios ejecutándose"
    fi
}

# Verificar que Grafana esté disponible
check_grafana() {
    echo "📊 Verificando Grafana..."
    
    max_attempts=30
    attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s http://localhost:3000/api/health > /dev/null 2>&1; then
            echo "✅ Grafana disponible en http://localhost:3000"
            return 0
        fi
        
        echo "⏳ Esperando Grafana... (intento $attempt/$max_attempts)"
        sleep 2
        attempt=$((attempt + 1))
    done
    
    echo "❌ Grafana no está disponible después de $max_attempts intentos"
    return 1
}

# Verificar que Prometheus esté scrapeando
check_prometheus() {
    echo "📈 Verificando Prometheus..."
    
    if curl -s http://localhost:9090/api/v1/targets | grep -q "hexagonal-api"; then
        echo "✅ Prometheus scrapeando la aplicación"
    else
        echo "⚠️ Prometheus no está scrapeando la aplicación"
        echo "💡 Verificando configuración..."
        
        # Verificar que la app esté disponible
        if curl -s http://localhost:8000/metrics > /dev/null 2>&1; then
            echo "✅ Aplicación disponible en /metrics"
        else
            echo "❌ Aplicación no disponible en /metrics"
        fi
    fi
}

# Generar tráfico para ver métricas
generate_traffic() {
    echo "🚀 Generando tráfico para ver métricas..."
    
    # Generar algunas requests
    for i in {1..5}; do
        curl -s http://localhost:8000/health > /dev/null
        curl -s http://localhost:8000/metrics > /dev/null
        sleep 1
    done
    
    echo "✅ Tráfico generado"
}

# Mostrar información del dashboard
show_info() {
    echo ""
    echo "🎯 Información del Dashboard:"
    echo "============================"
    echo "📊 Grafana: http://localhost:3000"
    echo "👤 Usuario: admin"
    echo "🔑 Contraseña: admin123"
    echo ""
    echo "📈 Prometheus: http://localhost:9090"
    echo "🌐 API: http://localhost:8000"
    echo "📊 Métricas: http://localhost:8000/metrics"
    echo ""
    echo "🔧 Scripts disponibles:"
    echo "- ./generate_metrics.sh all    # Generar tráfico completo"
    echo "- python test_metrics.py       # Script interactivo"
    echo ""
    echo "💡 Para ver métricas en tiempo real:"
    echo "curl http://localhost:8000/metrics"
}

# Función principal
main() {
    check_services
    check_grafana
    check_prometheus
    generate_traffic
    show_info
    
    echo ""
    echo "🎉 Dashboard configurado correctamente!"
    echo "📊 Abre http://localhost:3000 en tu navegador"
}

# Ejecutar función principal
main "$@" 