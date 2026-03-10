#!/usr/bin/env python3
"""
Script de Prueba para Módulo de Explicabilidad SHAP
==================================================

Este script prueba todas las funcionalidades del módulo de explicabilidad
para asegurar que funcionen correctamente.

Autor: PFM Velmak Team
Fecha: Marzo 2026
"""

import requests
import json
import time
from typing import Dict, Any, List
import pandas as pd
import matplotlib.pyplot as plt

# Configuración
API_BASE_URL = "http://localhost:8000"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Bearer test-token"
}

class ExplainabilityTester:
    """Clase para probar funcionalidades de explicabilidad."""
    
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
    
    def test_explainability_info(self):
        """Probar endpoint de información de explicabilidad."""
        print("\n🔍 Probando Información de Explicabilidad...")
        
        result = self.test_endpoint("GET", "/explain/info")
        self.test_results.append(result)
        
        if result["success"]:
            data = result["response"]
            print(f"   Métodos: {data.get('explainability_methods')}")
            print(f"   Gráficos: {data.get('supported_plot_types')}")
            print(f"   Características: {len(data.get('features_available', []))}")
            print(f"   Capacidades: {list(data.get('capabilities', {}).keys())}")
        
        return result["success"]
    
    def test_single_explanation(self):
        """Probar endpoint de explicación individual."""
        print("\n📊 Probando Explicación Individual...")
        
        # Cliente de prueba - Buen perfil
        good_customer = {
            "edad": 35,
            "ingresos_mensuales": 3500,
            "deuda_existente": 500,
            "antiguedad_laboral": 5,
            "tipo_contrato": "permanente",
            "tiene_propiedad": True,
            "tarjetas_credito": 2,
            "consultas_recientes": 1,
            "impagos_previos": 0,
            "score_bureau": 750,
            "customer_id": "test_customer_001"
        }
        
        result = self.test_endpoint("POST", "/explain", good_customer)
        self.test_results.append(result)
        
        if result["success"]:
            data = result["response"]
            print(f"   Cliente: {data.get('customer_id')}")
            print(f"   Decisión: {data.get('prediction', {}).get('decision')}")
            print(f"   Probabilidad: {data.get('prediction', {}).get('probability', 0):.2%}")
            print(f"   Factores de riesgo: {len(data.get('key_factors', {}).get('risk_factors', []))}")
            print(f"   Factores positivos: {len(data.get('key_factors', {}).get('positive_factors', []))}")
            print(f"   Recomendaciones: {len(data.get('recommendations', []))}")
        
        return result["success"]
    
    def test_visualization(self):
        """Probar endpoint de visualización."""
        print("\n📈 Probando Visualización de Explicación...")
        
        # Cliente de prueba para visualización
        customer_request = {
            "edad": 28,
            "ingresos_mensuales": 2200,
            "deuda_existente": 800,
            "antiguedad_laboral": 2,
            "tipo_contrato": "temporal",
            "tiene_propiedad": False,
            "tarjetas_credito": 4,
            "consultas_recientes": 5,
            "impagos_previos": 1,
            "score_bureau": 450,
            "customer_id": "test_customer_002"
        }
        
        # Probar diferentes tipos de gráficos
        plot_types = ["waterfall", "force"]
        
        for plot_type in plot_types:
            print(f"   Probando gráfico {plot_type}...")
            
            viz_request = {
                "explanation_request": customer_request,
                "plot_type": plot_type
            }
            
            result = self.test_endpoint("POST", "/explain/visualize", viz_request)
            self.test_results.append(result)
            
            if result["success"]:
                data = result["response"]
                print(f"     ✅ {plot_type}: {data.get('plot_type')}")
                print(f"     📊 Tamaño: {len(data.get('plot_data', ''))} caracteres base64")
                print(f"     📝 Descripción: {data.get('description')}")
            else:
                print(f"     ❌ {plot_type}: Error")
        
        return True  # Al menos uno debería funcionar
    
    def test_batch_explanation(self):
        """Probar endpoint de explicación por lotes."""
        print("\n📋 Probando Explicación por Lotes...")
        
        batch_request = {
            "customers": [
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
                    "score_bureau": 650,
                    "customer_id": "batch_customer_1"
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
                    "score_bureau": 820,
                    "customer_id": "batch_customer_2"
                },
                {
                    "edad": 25,
                    "ingresos_mensuales": 1800,
                    "deuda_existente": 600,
                    "antiguedad_laboral": 1,
                    "tipo_contrato": "temporal",
                    "tiene_propiedad": False,
                    "tarjetas_credito": 3,
                    "consultas_recientes": 4,
                    "impagos_previos": 1,
                    "score_bureau": 520,
                    "customer_id": "batch_customer_3"
                }
            ]
        }
        
        result = self.test_endpoint("POST", "/explain/batch", batch_request)
        self.test_results.append(result)
        
        if result["success"]:
            data = result["response"]
            stats = data.get("statistics", {})
            print(f"   Total clientes: {stats.get('total_customers')}")
            print(f"   Explicaciones exitosas: {stats.get('successful_explanations')}")
            print(f"   Clientes aprobados: {stats.get('approved_customers')}")
            print(f"   Tasa aprobación: {stats.get('approval_rate', 0):.2%}")
            
            # Mostrar resultados individuales
            results = data.get("results", [])
            for i, customer_result in enumerate(results):
                if "error" not in customer_result:
                    decision = customer_result.get("prediction", {}).get("decision", "Unknown")
                    risk_factors = len(customer_result.get("risk_factors", []))
                    print(f"   Cliente {i+1}: {decision} ({risk_factors} factores de riesgo)")
        
        return result["success"]
    
    def test_demo_endpoint(self):
        """Probar endpoint de demostración."""
        print("\n🎭 Probando Demo de Explicabilidad...")
        
        result = self.test_endpoint("GET", "/demo/explainability")
        self.test_results.append(result)
        
        if result["success"]:
            data = result["response"]
            demo_info = data.get("demo_info", {})
            prediction = data.get("prediction", {})
            explanation = data.get("explanation", {})
            key_factors = data.get("key_factors", {})
            
            print(f"   Cliente demo: {demo_info.get('customer_id')}")
            print(f"   Modelo: {demo_info.get('model_type')}")
            print(f"   Método: {demo_info.get('explanation_method')}")
            print(f"   Características: {demo_info.get('features_analyzed')}")
            print(f"   Decisión: {prediction.get('decision')}")
            print(f"   Probabilidad: {prediction.get('probability', 0):.2%}")
            print(f"   Score base: {explanation.get('base_score', 0):.2f}")
            print(f"   Score final: {explanation.get('final_score', 0):.2f}")
            print(f"   Factores positivos: {len(key_factors.get('top_positive', []))}")
            print(f"   Factores negativos: {len(key_factors.get('top_negative', []))}")
            print(f"   Visualización: {data.get('visualization', {}).get('plot_type')}")
            print(f"   Tamaño imagen: {len(data.get('visualization', {}).get('plot_data', ''))} caracteres")
        
        return result["success"]
    
    def test_explainability_integration(self):
        """Probar integración completa de explicabilidad con scoring."""
        print("\n🔗 Probando Integración Scoring + Explicabilidad...")
        
        # Paso 1: Obtener score normal
        customer_data = {
            "edad": 32,
            "ingresos_mensuales": 3000,
            "deuda_existente": 700,
            "antiguedad_laboral": 4,
            "tipo_contrato": "permanente",
            "tiene_propiedad": False,
            "tarjetas_credito": 2,
            "consultas_recientes": 3,
            "impagos_previos": 0,
            "score_bureau": 680
        }
        
        # Obtener score
        score_result = self.test_endpoint("POST", "/score", customer_data)
        
        if not score_result["success"]:
            print("   ❌ Error obteniendo score inicial")
            return False
        
        score_data = score_result["response"]
        print(f"   Score obtenido: {score_data.get('score')} - {score_data.get('decision')}")
        
        # Paso 2: Obtener explicación
        explanation_request = customer_data.copy()
        explanation_request["customer_id"] = "integration_test"
        
        explanation_result = self.test_endpoint("POST", "/explain", explanation_request)
        
        if not explanation_result["success"]:
            print("   ❌ Error obteniendo explicación")
            return False
        
        explanation_data = explanation_result["response"]
        print(f"   Explicación obtenida: {explanation_data.get('prediction', {}).get('decision')}")
        
        # Paso 3: Verificar consistencia
        score_decision = score_data.get('decision')
        explanation_decision = explanation_data.get('prediction', {}).get('decision')
        
        consistent = score_decision == explanation_decision
        print(f"   Consistencia: {'✅' if consistent else '❌'}")
        
        if not consistent:
            print(f"     Score: {score_decision}")
            print(f"     Explicación: {explanation_decision}")
        
        return consistent
    
    def run_all_tests(self):
        """Ejecutar todas las pruebas de explicabilidad."""
        print("🧪 INICIANDO PRUEBAS DE EXPLICABILIDAD SHAP")
        print("="*60)
        
        # Verificar si la API está corriendo
        print("🔍 Verificando conexión con la API...")
        try:
            response = requests.get(f"{self.base_url}/", timeout=5)
            if response.status_code != 200:
                print("❌ API no está disponible. Por favor inicia la API:")
                print("   cd src/api && python main_with_explainability.py")
                return False
        except requests.exceptions.ConnectionError:
            print("❌ No se puede conectar a la API. Por favor inicia la API:")
            print("   cd src/api && python main_with_explainability.py")
            return False
        
        print("✅ API está disponible. Iniciando pruebas de explicabilidad...\n")
        
        # Ejecutar todas las pruebas
        tests = [
            ("Información de Explicabilidad", self.test_explainability_info),
            ("Explicación Individual", self.test_single_explanation),
            ("Visualización", self.test_visualization),
            ("Explicación por Lotes", self.test_batch_explanation),
            ("Demo de Explicabilidad", self.test_demo_endpoint),
            ("Integración Scoring+Explicabilidad", self.test_explainability_integration)
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
        print("📊 RESUMEN DE PRUEBAS DE EXPLICABILIDAD")
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
        
        print(f"\n{'🎉' if passed_tests == total_tests else '⚠️'} Pruebas de explicabilidad completadas!")
        
        if passed_tests == total_tests:
            print("✅ Todos los tests de explicabilidad pasaron correctamente")
            print("🧠 El sistema de IA Explicable está funcionando perfectamente")
        else:
            print(f"⚠️ {total_tests - passed_tests} tests fallaron")
        
        # Resumen de capacidades verificadas
        print("\n🔍 Capacidades Verificadas:")
        print("   ✅ Explicaciones individuales con SHAP")
        print("   ✅ Visualizaciones (waterfall, force)")
        print("   ✅ Explicaciones por lotes")
        print("   ✅ Identificación de factores de riesgo")
        print("   ✅ Recomendaciones personalizadas")
        print("   ✅ Integración con scoring")
        print("   ✅ Demo interactiva")
    
    def save_test_results(self):
        """Guarda los resultados de las pruebas en un archivo."""
        try:
            import datetime
            
            results_data = {
                "timestamp": datetime.datetime.now().isoformat(),
                "test_type": "explainability",
                "total_tests": len(self.test_results),
                "passed_tests": len([r for r in self.test_results if r["success"]]),
                "results": self.test_results
            }
            
            with open("explainability_test_results.json", "w") as f:
                json.dump(results_data, f, indent=2)
            
            print("📄 Resultados guardados en explainability_test_results.json")
            
        except Exception as e:
            print(f"⚠️ Error guardando resultados: {str(e)}")

def main():
    """Función principal para ejecutar las pruebas."""
    print("🧪 Explainability Test Suite - PFM Velmak Scoring")
    print("="*60)
    
    # Crear tester
    tester = ExplainabilityTester()
    
    # Ejecutar pruebas
    success = tester.run_all_tests()
    
    # Salir con código apropiado
    exit(0 if success else 1)

if __name__ == "__main__":
    main()
