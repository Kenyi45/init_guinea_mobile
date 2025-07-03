#!/usr/bin/env python3
"""
Script para generar tráfico y probar las métricas del sistema.
"""

import requests
import time
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

class MetricsTestGenerator:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        
    def health_check(self):
        """Verificar que la API esté funcionando."""
        try:
            response = self.session.get(f"{self.base_url}/health")
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Error en health check: {e}")
            return False
    
    def generate_http_traffic(self, duration=30):
        """Generar tráfico HTTP básico."""
        print(f"🌐 Generando tráfico HTTP por {duration} segundos...")
        
        endpoints = [
            "/health",
            "/metrics",
            "/api/v1/users",  # Esto dará 405 pero genera métricas
        ]
        
        start_time = time.time()
        requests_count = 0
        
        while time.time() - start_time < duration:
            for endpoint in endpoints:
                try:
                    response = self.session.get(f"{self.base_url}{endpoint}")
                    requests_count += 1
                    print(f"📊 {endpoint} -> {response.status_code}")
                except Exception as e:
                    print(f"❌ Error: {e}")
                
                time.sleep(0.5)
        
        print(f"✅ Generadas {requests_count} requests en {duration} segundos")
    
    def create_test_users(self, count=5):
        """Crear usuarios de prueba."""
        print(f"👥 Creando {count} usuarios de prueba...")
        
        for i in range(count):
            user_data = {
                "email": f"test{i}@example.com",
                "username": f"testuser{i}",
                "first_name": f"Test{i}",
                "last_name": f"User{i}",
                "password": "password123"
            }
            
            try:
                response = self.session.post(
                    f"{self.base_url}/api/v1/users",
                    json=user_data
                )
                if response.status_code == 201:
                    print(f"✅ Usuario {i+1} creado exitosamente")
                else:
                    print(f"⚠️ Usuario {i+1} falló: {response.status_code}")
            except Exception as e:
                print(f"❌ Error creando usuario {i+1}: {e}")
            
            time.sleep(1)
    
    def test_authentication(self, attempts=10):
        """Probar autenticación con diferentes credenciales."""
        print(f"🔐 Probando autenticación con {attempts} intentos...")
        
        # Credenciales de prueba (algunas correctas, algunas incorrectas)
        credentials = [
            {"email": "test0@example.com", "password": "password123"},  # Correcto
            {"email": "test1@example.com", "password": "wrongpassword"},  # Incorrecto
            {"email": "nonexistent@example.com", "password": "password123"},  # No existe
            {"email": "test0@example.com", "password": "password123"},  # Correcto
        ]
        
        for i in range(attempts):
            creds = credentials[i % len(credentials)]
            
            try:
                response = self.session.post(
                    f"{self.base_url}/api/v1/auth/login",
                    json=creds
                )
                
                if response.status_code == 200:
                    print(f"✅ Login exitoso: {creds['email']}")
                else:
                    print(f"❌ Login fallido: {creds['email']} -> {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Error en login: {e}")
            
            time.sleep(1)
    
    def stress_test(self, concurrent_users=5, duration=60):
        """Prueba de estrés con múltiples usuarios concurrentes."""
        print(f"🚀 Iniciando prueba de estrés: {concurrent_users} usuarios por {duration} segundos...")
        
        def user_session(user_id):
            session = requests.Session()
            start_time = time.time()
            request_count = 0
            
            while time.time() - start_time < duration:
                try:
                    # Simular comportamiento de usuario
                    endpoints = [
                        "/health",
                        "/api/v1/users",
                        "/metrics"
                    ]
                    
                    for endpoint in endpoints:
                        response = session.get(f"{self.base_url}{endpoint}")
                        request_count += 1
                        time.sleep(0.1)
                
                except Exception as e:
                    pass
                
                time.sleep(0.5)
            
            return f"Usuario {user_id}: {request_count} requests"
        
        # Ejecutar usuarios concurrentes
        with ThreadPoolExecutor(max_workers=concurrent_users) as executor:
            futures = [executor.submit(user_session, i) for i in range(concurrent_users)]
            
            for future in as_completed(futures):
                result = future.result()
                print(f"✅ {result}")
    
    def show_current_metrics(self):
        """Mostrar métricas actuales."""
        print("📈 Métricas actuales:")
        
        try:
            response = self.session.get(f"{self.base_url}/metrics")
            if response.status_code == 200:
                metrics_lines = response.text.split('\n')
                
                # Filtrar métricas importantes
                important_metrics = [
                    'http_requests_total',
                    'user_operations_total',
                    'auth_attempts_total',
                    'db_operations_total',
                    'application_errors_total'
                ]
                
                for line in metrics_lines:
                    if any(metric in line for metric in important_metrics):
                        if not line.startswith('#') and line.strip():
                            print(f"  {line}")
            else:
                print(f"❌ Error obteniendo métricas: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {e}")

def main():
    """Función principal."""
    print("🚀 Generador de Tráfico para Métricas")
    print("=" * 50)
    
    generator = MetricsTestGenerator()
    
    # Verificar conectividad
    if not generator.health_check():
        print("❌ La API no está disponible en http://localhost:8000")
        sys.exit(1)
    
    print("✅ API disponible")
    
    # Mostrar opciones
    print("\n📋 Opciones disponibles:")
    print("1. Generar tráfico HTTP básico")
    print("2. Crear usuarios de prueba")
    print("3. Probar autenticación")
    print("4. Prueba de estrés")
    print("5. Mostrar métricas actuales")
    print("6. Ejecutar todo automáticamente")
    print("0. Salir")
    
    while True:
        try:
            choice = input("\n👉 Selecciona una opción (0-6): ").strip()
            
            if choice == "0":
                print("👋 ¡Hasta luego!")
                break
            elif choice == "1":
                duration = int(input("⏱️ Duración en segundos (default: 30): ") or 30)
                generator.generate_http_traffic(duration)
            elif choice == "2":
                count = int(input("👥 Número de usuarios (default: 5): ") or 5)
                generator.create_test_users(count)
            elif choice == "3":
                attempts = int(input("🔐 Número de intentos (default: 10): ") or 10)
                generator.test_authentication(attempts)
            elif choice == "4":
                users = int(input("👥 Usuarios concurrentes (default: 5): ") or 5)
                duration = int(input("⏱️ Duración en segundos (default: 60): ") or 60)
                generator.stress_test(users, duration)
            elif choice == "5":
                generator.show_current_metrics()
            elif choice == "6":
                print("🚀 Ejecutando secuencia completa...")
                generator.create_test_users(3)
                time.sleep(2)
                generator.test_authentication(8)
                time.sleep(2)
                generator.generate_http_traffic(30)
                time.sleep(2)
                generator.show_current_metrics()
            else:
                print("❌ Opción no válida")
                
        except KeyboardInterrupt:
            print("\n👋 Interrumpido por el usuario")
            break
        except ValueError:
            print("❌ Por favor ingresa un número válido")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 