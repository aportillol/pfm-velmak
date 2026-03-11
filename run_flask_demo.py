#!/usr/bin/env python3
"""
Servidor Flask Multiusuario para PFM Velmak Demo
=================================================

Servidor web profesional con soporte para múltiples usuarios simultáneos.
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
import threading
import time
import random
from datetime import datetime
import os

app = Flask(__name__)

# Simulación de datos para múltiples usuarios
user_sessions = {}
analytics_data = {
    'total_evaluations': 1247,
    'active_users': 0,
    'avg_score': 687,
    'approval_rate': 68.5
}

@app.route('/')
def index():
    """Página principal de la demo."""
    return send_from_directory('.', 'demo_web.html')

@app.route('/api/evaluate', methods=['POST'])
def evaluate_credit():
    """API para evaluación de crédito."""
    data = request.get_json()
    
    # Simular procesamiento
    score = calculate_score(data)
    
    # Actualizar analytics
    analytics_data['total_evaluations'] += 1
    analytics_data['avg_score'] = (analytics_data['avg_score'] + score) / 2
    
    return jsonify({
        'score': score,
        'decision': get_decision(score),
        'approval_probability': get_approval_prob(score),
        'risk_factors': get_risk_factors(data, score),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/analytics')
def get_analytics():
    """Obtener datos analíticos del sistema."""
    return jsonify(analytics_data)

@app.route('/api/batch-process', methods=['POST'])
def batch_process():
    """Procesamiento por lotes."""
    # Simular procesamiento batch
    total_records = random.randint(100, 1000)
    approval_rate = random.uniform(50, 80)
    
    return jsonify({
        'total_records': total_records,
        'approval_rate': round(approval_rate, 1),
        'processing_time': f"{random.uniform(0.5, 2.5):.2f}s"
    })

def calculate_score(data):
    """Calcular score de crédito."""
    score = 500
    
    # Factores positivos
    score += (data.get('scoreBureau', 750) - 684) * 0.5
    score += (data.get('edad', 35) - 34) * 2
    score += (data.get('ingresos', 3500) - 3715) * 0.01
    score += (data.get('antiguedad', 5) - 6) * 5
    
    if data.get('tienePropiedad', False):
        score += 50
    
    # Factores negativos
    score -= data.get('impagos', 0) * 100
    score -= data.get('consultas', 1) * 30
    score -= data.get('tarjetas', 2) * 10
    
    # Ratio deuda
    debt_ratio = data.get('deuda', 500) / data.get('ingresos', 3500)
    if debt_ratio > 0.5:
        score -= 100
    elif debt_ratio > 0.3:
        score -= 50
    
    return max(0, min(1000, int(score)))

def get_decision(score):
    """Obtener decisión basada en score."""
    if score >= 650:
        return "Aprobado Automático"
    elif score >= 500:
        return "Revisión Manual"
    else:
        return "Rechazado"

def get_approval_prob(score):
    """Calcular probabilidad de aprobación."""
    return max(0, min(100, (score - 300) / 7))

def get_risk_factors(data, score):
    """Identificar factores de riesgo."""
    factors = []
    
    if data.get('impagos', 0) > 0:
        factors.append(f"Impagos previos: {data.get('impagos', 0)}")
    
    if data.get('consultas', 0) > 3:
        factors.append(f"Consultas recientes: {data.get('consultas', 0)}")
    
    debt_ratio = data.get('deuda', 0) / data.get('ingresos', 1)
    if debt_ratio > 0.5:
        factors.append(f"Ratio deuda/ingresos: {debt_ratio*100:.1f}%")
    
    return factors

def update_analytics():
    """Actualizar datos analíticos periódicamente."""
    while True:
        time.sleep(30)  # Actualizar cada 30 segundos
        analytics_data['active_users'] = len(user_sessions)
        analytics_data['avg_score'] += random.uniform(-5, 5)
        analytics_data['approval_rate'] += random.uniform(-2, 2)
        analytics_data['approval_rate'] = max(0, min(100, analytics_data['approval_rate']))

if __name__ == '__main__':
    print("🌐 PFM Velmak - Servidor Flask Multiusuario")
    print("=" * 50)
    print("🚀 Iniciando servidor avanzado...")
    print("📍 URL: http://localhost:5000")
    print("👥 Soporte para múltiples usuarios simultáneos")
    print("📊 Analytics en tiempo real")
    print("⏹️  Presiona Ctrl+C para detener")
    print("-" * 50)
    
    # Iniciar hilo de analytics
    analytics_thread = threading.Thread(target=update_analytics, daemon=True)
    analytics_thread.start()
    
    # Iniciar servidor Flask
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
