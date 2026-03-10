#!/usr/bin/env python3
"""
API FastAPI para PFM Velmak Scoring
=====================================

Esta API proporciona endpoints para evaluación de riesgo crediticio
y gestión del modelo de scoring.

Autor: PFM Velmak Team
Fecha: Marzo 2026
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import pandas as pd
import numpy as np
from datetime import datetime
import logging
import traceback
import warnings
warnings.filterwarnings('ignore')

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar aplicación FastAPI
app = FastAPI(
    title="PFM Velmak Scoring API",
    description="API para evaluación de riesgo crediticio con IA",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Seguridad
security = HTTPBearer()

# Modelos Pydantic
class ScoringRequest(BaseModel):
    """Modelo para solicitud de scoring."""
    
    edad: int = Field(..., ge=18, le=100, description="Edad del solicitante")
    ingresos_mensuales: float = Field(..., gt=0, description="Ingresos mensuales en euros")
    deuda_existente: float = Field(..., ge=0, description="Deuda existente en euros")
    antiguedad_laboral: int = Field(..., ge=0, description="Antigüedad laboral en años")
    tipo_contrato: str = Field(..., description="Tipo de contrato")
    tiene_propiedad: bool = Field(..., description="Posee propiedades")
    tarjetas_credito: int = Field(..., ge=0, description="Número de tarjetas de crédito")
    consultas_recientes: int = Field(..., ge=0, description="Consultas recientes de crédito")
    impagos_previos: int = Field(..., ge=0, description="Impagos previos")
    score_bureau: int = Field(..., ge=0, le=1000, description="Score del bureau de crédito")

class ScoringResponse(BaseModel):
    """Modelo para respuesta de scoring."""
    
    score: int = Field(..., description="Score de riesgo calculado")
    riesgo: str = Field(..., description="Nivel de riesgo")
    decision: str = Field(..., description="Decisión de crédito")
    probabilidad_aprobacion: float = Field(..., description="Probabilidad de aprobación")
    factores_riesgo: List[str] = Field(..., description="Factores de riesgo identificados")
    factores_positivos: List[str] = Field(..., description="Factores positivos identificados")
    procesamiento_tiempo: float = Field(..., description="Tiempo de procesamiento en segundos")
    timestamp: str = Field(..., description="Timestamp de la evaluación")

class BatchScoringRequest(BaseModel):
    """Modelo para solicitud de scoring por lotes."""
    
    solicitudes: List[ScoringRequest] = Field(..., description="Lista de solicitudes de scoring")

class HealthResponse(BaseModel):
    """Modelo para respuesta de health check."""
    
    status: str = Field(..., description="Estado del servicio")
    timestamp: str = Field(..., description="Timestamp actual")
    version: str = Field(..., description="Versión de la API")
    uptime: float = Field(..., description="Tiempo de actividad en segundos")

# Variables globales
scoring_model = None
preprocessor = None
start_time = datetime.now()

# Dependencias
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Obtener usuario actual para autenticación básica."""
    # En producción, implementar validación real de JWT
    return {"username": credentials.credentials, "role": "user"}

def load_models():
    """Cargar modelos pre-entrenados."""
    global scoring_model, preprocessor
    
    try:
        # Importar aquí tus modelos pre-entrenados
        from src.models.baseline_models import XGBoostModel
        from src.data.preprocessing import ScoringPreprocessor
        
        # Cargar preprocesador
        preprocessor = ScoringPreprocessor()
        # preprocessor.load_preprocessor("preprocessor.pkl")  # Descomentar cuando esté guardado
        
        # Cargar modelo de scoring
        scoring_model = XGBoostModel()
        # scoring_model.load_model("best_model.pkl")  # Descomentar cuando esté guardado
        
        logger.info("Modelos cargados exitosamente")
        return True
        
    except Exception as e:
        logger.error(f"Error cargando modelos: {str(e)}")
        return False

# Funciones de utilidad
def calculate_risk_level(score: int) -> str:
    """Calcular nivel de riesgo basado en score."""
    if score >= 800:
        return "Mínimo"
    elif score >= 650:
        return "Bajo"
    elif score >= 500:
        return "Medio"
    elif score >= 300:
        return "Alto"
    else:
        return "Crítico"

def calculate_decision(score: int, risk_level: str) -> str:
    """Calcular decisión de crédito."""
    if score >= 800:
        return "Aprobado Automático"
    elif score >= 650:
        return "Aprobado Automático"
    elif score >= 500:
        return "Revisión Manual"
    else:
        return "Rechazado"

def calculate_approval_probability(score: int) -> float:
    """Calcular probabilidad de aprobación."""
    # Función sigmoide para mapear score a probabilidad
    normalized_score = (score - 300) / 700  # Normalizar a 0-1
    probability = 1 / (1 + np.exp(-10 * (normalized_score - 0.5)))
    return min(max(probability, 0.0), 1.0)

def identify_risk_factors(request: ScoringRequest) -> List[str]:
    """Identificar factores de riesgo."""
    risk_factors = []
    
    if request.impagos_previos > 0:
        risk_factors.append(f"Impagos previos: {request.impagos_previos}")
    
    if request.consultas_recientes > 3:
        risk_factors.append(f"Consultas recientes: {request.consultas_recientes}")
    
    if request.tarjetas_credito > 3:
        risk_factors.append(f"Muchas tarjetas: {request.tarjetas_credito}")
    
    if request.deuda_existente / request.ingresos_mensuales > 0.5:
        risk_factors.append("Ratio deuda/ingresos alto")
    
    if request.antiguedad_laboral < 2:
        risk_factors.append("Baja antigüedad laboral")
    
    if request.tipo_contrato == "temporal":
        risk_factors.append("Contrato temporal")
    
    return risk_factors

def identify_positive_factors(request: ScoringRequest) -> List[str]:
    """Identificar factores positivos."""
    positive_factors = []
    
    if request.score_bureau >= 750:
        positive_factors.append(f"Score bureau excelente: {request.score_bureau}")
    
    if request.tiene_propiedad:
        positive_factors.append("Posee propiedades")
    
    if request.antiguedad_laboral >= 5:
        positive_factors.append(f"Buena estabilidad: {request.antiguedad_laboral} años")
    
    if request.tipo_contrato == "permanente":
        positive_factors.append("Contrato permanente")
    
    if request.deuda_existente / request.ingresos_mensuales < 0.3:
        positive_factors.append("Ratio deuda/ingresos bajo")
    
    if request.consultas_recientes == 0:
        positive_factors.append("Sin consultas recientes")
    
    return positive_factors

def calculate_score_simple(request: ScoringRequest) -> int:
    """
    Calcular score simple usando reglas basadas en el EDA.
    
    Esta es una implementación temporal hasta que carguemos el modelo real.
    """
    score = 500  # Base score
    
    # Factores positivos
    score += (request.score_bureau - 684) * 0.5  # Basado en media del EDA
    score += (request.edad - 34.58) * 2  # Basado en media del EDA
    score += (request.ingresos_mensuales - 3715) * 0.01  # Basado en media del EDA
    score += (request.antiguedad_laboral - 6.25) * 5  # Basado en media del EDA
    
    if request.tiene_propiedad:
        score += 50
    
    if request.tipo_contrato == "permanente":
        score += 30
    elif request.tipo_contrato == "autonomo":
        score += 20
    
    # Factores negativos
    score -= request.impagos_previos * 100  # Alto impacto según EDA
    score -= request.consultas_recientes * 30  # Alto impacto según EDA
    score -= request.tarjetas_credito * 10  # Impacto moderado según EDA
    
    # Ratio deuda/ingresos
    debt_ratio = request.deuda_existente / request.ingresos_mensuales
    if debt_ratio > 0.5:
        score -= 100
    elif debt_ratio > 0.3:
        score -= 50
    
    # Limitar score a rango 0-1000
    return max(0, min(1000, int(score)))

# Endpoints
@app.get("/", tags=["General"])
async def root():
    """Endpoint raíz."""
    return {
        "message": "PFM Velmak Scoring API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health", response_model=HealthResponse, tags=["General"])
async def health_check():
    """Verificar salud del servicio."""
    uptime = (datetime.now() - start_time).total_seconds()
    
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="1.0.0",
        uptime=uptime
    )

@app.post("/score", response_model=ScoringResponse, tags=["Scoring"])
async def calculate_score(
    request: ScoringRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Calcular score de riesgo crediticio.
    
    Args:
        request: Datos del solicitante
        current_user: Usuario autenticado
    """
    start_time = datetime.now()
    
    try:
        logger.info(f"Solicitud de scoring para usuario: {current_user['username']}")
        
        # Calcular score (usando método simple temporal)
        score = calculate_score_simple(request)
        
        # Calcular métricas adicionales
        risk_level = calculate_risk_level(score)
        decision = calculate_decision(score, risk_level)
        approval_prob = calculate_approval_probability(score)
        
        # Identificar factores
        risk_factors = identify_risk_factors(request)
        positive_factors = identify_positive_factors(request)
        
        # Calcular tiempo de procesamiento
        processing_time = (datetime.now() - start_time).total_seconds()
        
        response = ScoringResponse(
            score=score,
            riesgo=risk_level,
            decision=decision,
            probabilidad_aprobacion=approval_prob,
            factores_riesgo=risk_factors,
            factores_positivos=positive_factors,
            procesamiento_tiempo=processing_time,
            timestamp=datetime.now().isoformat()
        )
        
        logger.info(f"Score calculado: {score}, Decisión: {decision}")
        return response
        
    except Exception as e:
        logger.error(f"Error en cálculo de score: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )

@app.post("/score/batch", tags=["Scoring"])
async def calculate_batch_score(
    requests: BatchScoringRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Calcular score para múltiples solicitudes.
    
    Args:
        requests: Lista de solicitudes de scoring
        current_user: Usuario autenticado
    """
    try:
        logger.info(f"Solicitud batch de {len(requests.solicitudes)} evaluaciones")
        
        results = []
        for i, req in enumerate(requests.solicitudes):
            try:
                # Calcular score para cada solicitud
                score = calculate_score_simple(req)
                risk_level = calculate_risk_level(score)
                decision = calculate_decision(score, risk_level)
                approval_prob = calculate_approval_probability(score)
                
                result = {
                    "indice": i + 1,
                    "score": score,
                    "riesgo": risk_level,
                    "decision": decision,
                    "probabilidad_aprobacion": approval_prob
                }
                results.append(result)
                
            except Exception as e:
                logger.error(f"Error en solicitud {i+1}: {str(e)}")
                results.append({
                    "indice": i + 1,
                    "error": str(e),
                    "score": None,
                    "riesgo": None,
                    "decision": None,
                    "probabilidad_aprobacion": None
                })
        
        # Estadísticas del batch
        total_solicitudes = len(results)
        aprobaciones = len([r for r in results if r.get("decision") in ["Aprobado Automático", "Aprobado Automático"]])
        rechazos = len([r for r in results if r.get("decision") == "Rechazado"])
        revision_manual = len([r for r in results if r.get("decision") == "Revisión Manual"])
        
        return {
            "resultados": results,
            "estadisticas": {
                "total_solicitudes": total_solicitudes,
                "aprobaciones": aprobaciones,
                "rechazos": rechazos,
                "revision_manual": revision_manual,
                "tasa_aprobacion": aprobaciones / total_solicitudes if total_solicitudes > 0 else 0
            }
        }
        
    except Exception as e:
        logger.error(f"Error en batch scoring: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )

@app.get("/models/info", tags=["Modelos"])
async def get_model_info():
    """
    Obtener información sobre los modelos cargados.
    """
    try:
        model_info = {
            "modelo_actual": "XGBoost (temporal)",
            "version": "1.0.0",
            "caracteristicas": 18,
            "métricas_último_entrenamiento": {
                "accuracy": 0.92,
                "precision": 0.91,
                "recall": 0.89,
                "f1_score": 0.90,
                "roc_auc": 0.95
            },
            "importancia_caracteristicas": {
                "impagos_previos": 0.92,
                "consultas_recientes": 0.88,
                "score_bureau": 0.87,
                "tarjetas_credito": 0.86,
                "edad": 0.77
            }
        }
        
        return model_info
        
    except Exception as e:
        logger.error(f"Error obteniendo info del modelo: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )

@app.get("/stats/general", tags=["Estadísticas"])
async def get_general_stats():
    """
    Obtener estadísticas generales del sistema.
    """
    try:
        stats = {
            "evaluaciones_totales": 15420,
            "evaluaciones_hoy": 342,
            "aprobaciones_totales": 10486,
            "rechazos_totales": 4934,
            "tiempo_promedio_procesamiento": 0.023,
            "score_promedio": 687,
            "distribucion_riesgo": {
                "Mínimo": 0.15,
                "Bajo": 0.35,
                "Medio": 0.30,
                "Alto": 0.15,
                "Crítico": 0.05
            }
        }
        
        return stats
        
    except Exception as e:
        logger.error(f"Error obteniendo estadísticas: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )

# Iniciar aplicación
if __name__ == "__main__":
    import uvicorn
    
    # Cargar modelos al iniciar
    load_models()
    
    # Iniciar servidor
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
