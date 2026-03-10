#!/usr/bin/env python3
"""
Script de Prueba para API PFM Velmak Scoring
=============================================

Este script prueba todos los endpoints de la API para verificar
su funcionamiento correcto.

Autor: PFM Velmak Team
Fecha: Marzo 2026
"""

import requests
import json
import time
from typing import Dict, Any

# Configuración
API_BASE_URL = "http://localhost:8000"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Bearer test-token"
}

class APITester:
    """Clase para probar endpoints de la API."""
    
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url
        self.test_results = []
        
    def test_endpoint(self, method: str, endpoint: str, data: Dict = None) -> Dict[str, Any]:
        """
        Probar un endpoint específico.
        
        Args:
            method: Método HTTP (GET, POST)
            endpoint: Endpoint a probar
            data: Datos para enviar (opcional)
            
        Returns:
            Dict: Resultado de la prueba
        """
        url = f"{self.base_url}{endpoint}"
        start_time = time.time()
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=HEADERS)
            elif method.upper() == "POST":
                response = requests.post(url, headers=HEADERS, json=data)
            else:
                raise ValueError(f"Método no soportado: {method}")
            
            end_time = time.time()
            response_time = end_time - start_time
            
            result = {
                "endpoint": endpoint,
                "method": method,
                "status_code": response.status_code,
                "response_time": response_time,
                "success": response.status_code < 400,
                "response": response.json() if response.headers.get("content-type", "").startswith("application/json") else response.text
            }
            
            print(f"{'✅' if result['success'] else '❌'} {method} {endpoint} - {response.status_code} ({response_time:.3f}s)")
            
            return result
            
        except requests.exceptions.ConnectionError:
            print(f"❌ {method} {endpoint} - Error de conexión")
            return {
                "endpoint": endpoint,
                "method": method,
                "status_code": 0,
                "response_time": 0,
                "success": False,
                "response": "Error de conexión"
            }
        except Exception as e:
            print(f"❌ {method} {endpoint} - Error: {str(e)}")
            return {
                "endpoint": endpoint,
                "method": method,
                "status_code": 0,
                "response_time": 0,
                "success": False,
                "response": str(e)
            }
    
    def test_health_check(self):
        """Probar endpoint de health check."""
        print("\n🏥 Probando Health Check...")
        result = self.test_endpoint("GET", "/health")
        self.test_results.append(result)
        
        if result["success"]:
            data = result["response"]
            print(f"   Status: {data.get('status')}")
            print(f"   Version: {data.get('version')}")
            print(f"   Uptime: {data.get('uptime'):.2f}s")
        
        return result["success"]
    
    def test_single_scoring(self):
        """Probar endpoint de scoring individual."""
        print("\n📊 Probando Scoring Individual...")
        
        # Caso de prueba 1: Buen solicitante
        good_applicant = {
            "edad": 35,
            "ingresos_mensuales": 3500,
            "deuda_existente": 500,
            "antiguedad_laboral": 5,
            "tipo_contrato": "permanente",
            "tiene_propiedad": True,
            "tarjetas_credito": 2,
            "consultas_recientes": 1,
            "impagos_previos": 0,
            "score_bureau": 750
        }
        
        result1 = self.test_endpoint("POST", "/score", good_applicant)
        self.test_results.append(result1)
        
        if result1["success"]:
            data = result1["response"]
            print(f"   Score: {data.get('score')}")
            print(f"   Riesgo: {data.get('riesgo')}")
            print(f"   Decisión: {data.get('decision')}")
            print(f"   Probabilidad: {data.get('probabilidad_aprobacion'):.2%}")
        
        # Caso de prueba 2: Solicitante de riesgo
        risky_applicant = {
            "edad": 25,
            "ingresos_mensuales": 1800,
            "deuda_existente": 800,
            "antiguedad_laboral": 1,
            "tipo_contrato": "temporal",
            "tiene_propiedad": False,
            "tarjetas_credito": 4,
            "consultas_recientes": 5,
            "impagos_previos": 1,
            "score_bureau": 450
        }
        
        result2 = self.test_endpoint("POST", "/score", risky_applicant)
        self.test_results.append(result2)
        
        if result2["success"]:
            data = result2["response"]
            print(f"   Score: {data.get('score')}")
            print(f"   Riesgo: {data.get('riesgo')}")
            print(f"   Decisión: {data.get('decision')}")
            print(f"   Probabilidad: {data.get('probabilidad_aprobacion'):.2%}")
        
        return result1["success"] and result2["success"]
    
    def test_batch_scoring(self):
        """Probar endpoint de scoring por lotes."""
        print("\n📋 Probando Scoring por Lotes...")
        
        batch_request = {
            "solicitudes": [
                {
                    "edad": 30,
                    "ingresos_mensuales": 2500,
                    "deuda_existente": 400,
                    "antiguedad_laboral": 3,
                    "tipo_contrato": "permanente",
                    "tiene_propiedad": False,
                    "tarjetas_credito": 2,
                    "consultas_recientes": 2,
                    "impagos_previos": 0,
                    "score_bureau": 650
                },
                {
                    "edad": 45,
                    "ingresos_mensuales": 5500,
                    "deuda_existente": 1500,
                    "antiguedad_laboral": 15,
                    "tipo_contrato": "permanente",
                    "tiene_propiedad": True,
                    "tarjetas_credito": 1,
                    "consultas_recientes": 0,
                    "impagos_previos": 0,
                    "score_bureau": 820
                },
                {
                    "edad": 28,
                    "ingresos_mensuales": 2000,
                    "deuda_existente": 600,
                    "antiguedad_laboral": 2,
                    "tipo_contrato": "temporal",
                    "tiene_propiedad": False,
                    "tarjetas_credito": 3,
                    "consultas_recientes": 4,
                    "impagos_previos": 1,
                    "score_bureau": 520
                }
            ]
        }
        
        result = self.test_endpoint("POST", "/score/batch", batch_request)
        self.test_results.append(result)
        
        if result["success"]:
            data = result["response"]
            stats = data.get("estadisticas", {})
            print(f"   Total solicitudes: {stats.get('total_solicitudes')}")
            print(f"   Aprobaciones: {stats.get('aprobaciones')}")
            print(f"   Rechazos: {stats.get('rechazos')}")
            print(f"   Revisión manual: {stats.get('revision_manual')}")
            print(f"   Tasa aprobación: {stats.get('tasa_aprobacion'):.2%}")
        
        return result["success"]
    
    def test_model_info(self):
        """Probar endpoint de información del modelo."""
        print("\n🤖 Probando Información del Modelo...")
        
        result = self.test_endpoint("GET", "/models/info")
        self.test_results.append(result)
        
        if result["success"]:
            data = result["response"]
            print(f"   Modelo: {data.get('modelo_actual')}")
            print(f"   Versión: {data.get('version')}")
            print(f"   Características: {data.get('caracteristicas')}")
            
            metrics = data.get('métricas_último_entrenamiento', {})
            print(f"   Accuracy: {metrics.get('accuracy', 0):.3f}")
            print(f"   ROC AUC: {metrics.get('roc_auc', 0):.3f}")
        
        return result["success"]
    
    def test_general_stats(self):
        """Probar endpoint de estadísticas generales."""
        print("\n📈 Probando Estadísticas Generales...")
        
        result = self.test_endpoint("GET", "/stats/general")
        self.test_results.append(result)
        
        if result["success"]:
            data = result["response"]
            print(f"   Evaluaciones totales: {data.get('evaluaciones_totales'):,}")
            print(f"   Evaluaciones hoy: {data.get('evaluaciones_hoy')}")
            print(f"   Score promedio: {data.get('score_promedio')}")
            print(f"   Tiempo procesamiento: {data.get('tiempo_promedio_procesamiento'):.3f}s")
        
        return result["success"]
    
    def test_invalid_requests(self):
        """Probar solicitudes inválidas para validación."""
        print("\n🚨 Probando Validación de Solicitudes...")
        
        # Test 1: Datos incompletos
        incomplete_data = {
            "edad": 35,
            "ingresos_mensuales": 3500
            # Faltan campos requeridos
        }
        
        result1 = self.test_endpoint("POST", "/score", incomplete_data)
        self.test_results.append(result1)
        
        # Test 2: Datos inválidos
        invalid_data = {
            "edad": -5,  # Edad inválida
            "ingresos_mensuales": -1000,  # Ingresos inválidos
            "deuda_existente": 500,
            "antiguedad_laboral": 5,
            "tipo_contrato": "permanente",
            "tiene_propiedad": True,
            "tarjetas_credito": 2,
            "consultas_recientes": 1,
            "impagos_previos": 0,
            "score_bureau": 750
        }
        
        result2 = self.test_endpoint("POST", "/score", invalid_data)
        self.test_results.append(result2)
        
        # Test 3: Endpoint no existente
        result3 = self.test_endpoint("GET", "/endpoint_no_existente")
        self.test_results.append(result3)
        
        validation_passed = (
            not result1["success"] and 
            not result2["success"] and 
            not result3["success"]
        )
        
        print(f"   Validación: {'✅' if validation_passed else '❌'}")
        
        return validation_passed
    
    def run_all_tests(self):
        """Ejecutar todas las pruebas de la API."""
        print("🚀 INICIANDO PRUEBAS COMPLETAS DE API")
        print("="*60)
        
        # Verificar si la API está corriendo
        print("🔍 Verificando conexión con la API...")
        try:
            response = requests.get(f"{self.base_url}/", timeout=5)
            if response.status_code != 200:
                print("❌ API no está disponible. Por favor inicia la API primero:")
                print("   cd src/api && python main.py")
                return False
        except requests.exceptions.ConnectionError:
            print("❌ No se puede conectar a la API. Por favor inicia la API primero:")
            print("   cd src/api && python main.py")
            return False
        
        print("✅ API está disponible. Iniciando pruebas...\n")
        
        # Ejecutar todas las pruebas
        tests = [
            ("Health Check", self.test_health_check),
            ("Single Scoring", self.test_single_scoring),
            ("Batch Scoring", self.test_batch_scoring),
            ("Model Info", self.test_model_info),
            ("General Stats", self.test_general_stats),
            ("Validation", self.test_invalid_requests)
        ]
        
        passed_tests = 0
        total_tests = len(tests)
        
        for test_name, test_func in tests:
            try:
                if test_func():
                    passed_tests += 1
            except Exception as e:
                print(f"❌ Error en prueba {test_name}: {str(e)}")
        
        # Generar resumen
        self.generate_test_summary(passed_tests, total_tests)
        
        return passed_tests == total_tests
    
    def generate_test_summary(self, passed_tests: int, total_tests: int):
        """Genera un resumen de las pruebas."""
        print("\n" + "="*60)
        print("📊 RESUMEN DE PRUEBAS")
        print("="*60)
        
        success_rate = (passed_tests / total_tests) * 100
        print(f"Pruebas exitosas: {passed_tests}/{total_tests} ({success_rate:.1f}%)")
        
        # Estadísticas de respuesta
        response_times = [r["response_time"] for r in self.test_results if r["success"]]
        if response_times:
            avg_time = sum(response_times) / len(response_times)
            max_time = max(response_times)
            min_time = min(response_times)
            
            print(f"Tiempo promedio respuesta: {avg_time:.3f}s")
            print(f"Tiempo máximo respuesta: {max_time:.3f}s")
            print(f"Tiempo mínimo respuesta: {min_time:.3f}s")
        
        # Resultados por endpoint
        print("\n📋 Resultados por endpoint:")
        for result in self.test_results:
            status = "✅" if result["success"] else "❌"
            print(f"   {status} {result['method']} {result['endpoint']} - {result['status_code']}")
        
        # Guardar resultados en archivo
        self.save_test_results()
        
        print(f"\n{'🎉' if passed_tests == total_tests else '⚠️'} Pruebas completadas!")
        
        if passed_tests == total_tests:
            print("✅ Todos los tests pasaron correctamente")
        else:
            print(f"⚠️ {total_tests - passed_tests} tests fallaron")
    
    def save_test_results(self):
        """Guarda los resultados de las pruebas en un archivo."""
        try:
            import datetime
            
            results_data = {
                "timestamp": datetime.datetime.now().isoformat(),
                "total_tests": len(self.test_results),
                "passed_tests": len([r for r in self.test_results if r["success"]]),
                "results": self.test_results
            }
            
            with open("api_test_results.json", "w") as f:
                json.dump(results_data, f, indent=2)
            
            print("📄 Resultados guardados en api_test_results.json")
            
        except Exception as e:
            print(f"⚠️ Error guardando resultados: {str(e)}")

def main():
    """Función principal para ejecutar las pruebas."""
    print("🧪 API Test Suite - PFM Velmak Scoring")
    print("="*60)
    
    # Crear tester
    tester = APITester()
    
    # Ejecutar pruebas
    success = tester.run_all_tests()
    
    # Salir con código apropiado
    exit(0 if success else 1)

if __name__ == "__main__":
    main()
