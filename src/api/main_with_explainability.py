#!/usr/bin/env python3
"""
API FastAPI con Explicabilidad para PFM Velmak Scoring
======================================================

Esta API proporciona endpoints para evaluación de riesgo crediticio
y explicación detallada de decisiones usando SHAP.

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

# Importar módulos de explicabilidad
from explainability_endpoints import add_explainability_endpoints

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar aplicación FastAPI
app = FastAPI(
    title="PFM Velmak Scoring API con Explicabilidad",
    description="API para evaluación de riesgo crediticio con IA Explicable (SHAP)",
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

# Importar endpoints existentes
from main import (
    ScoringRequest, ScoringResponse, BatchScoringRequest,
    HealthResponse, calculate_score, calculate_batch_score,
    get_model_info, get_general_stats, get_current_user
)

# Añadir endpoints de explicabilidad
add_explainability_endpoints(app)

# Mantener endpoints existentes
@app.get("/", tags=["General"])
async def root():
    """Endpoint raíz."""
    return {
        "message": "PFM Velmak Scoring API con Explicabilidad",
        "version": "1.0.0",
        "features": ["Scoring", "SHAP Explainability", "Visualization"],
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health", response_model=HealthResponse, tags=["General"])
async def health_check():
    """Verificar salud del servicio."""
    uptime = (datetime.now() - datetime(2024, 1, 1)).total_seconds()
    
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="1.0.0",
        uptime=uptime
    )

@app.post("/score", response_model=ScoringResponse, tags=["Scoring"])
async def calculate_score_endpoint(
    request: ScoringRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Calcular score de riesgo crediticio.
    
    Args:
        request: Datos del solicitante
        current_user: Usuario autenticado
    """
    return calculate_score(request, current_user)

@app.post("/score/batch", tags=["Scoring"])
async def calculate_batch_score_endpoint(
    requests: BatchScoringRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Calcular score para múltiples solicitudes.
    
    Args:
        requests: Lista de solicitudes de scoring
        current_user: Usuario autenticado
    """
    return calculate_batch_score(requests, current_user)

@app.get("/models/info", tags=["Modelos"])
async def get_model_info_endpoint():
    """
    Obtener información sobre los modelos cargados.
    """
    return get_model_info()

@app.get("/stats/general", tags=["Estadísticas"])
async def get_general_stats_endpoint():
    """
    Obtener estadísticas generales del sistema.
    """
    return get_general_stats()

# Nuevo endpoint de demostración de explicabilidad
@app.get("/demo/explainability", tags=["Demo"])
async def demo_explainability():
    """
    Demostración de capacidades de explicabilidad.
    
    Retorna un ejemplo completo de cómo funciona la explicabilidad SHAP.
    """
    try:
        # Importar módulos necesarios
        from src.explainability.shap_explainer import create_shap_explainer
        from src.models.baseline_models import XGBoostModel
        from src.data.preprocessing import ScoringPreprocessor
        import pandas as pd
        import base64
        import io
        import matplotlib.pyplot as plt
        
        # Cargar y preparar datos
        df = pd.read_csv("data/raw/datos.csv")
        preprocessor = ScoringPreprocessor()
        X_train, X_test, y_train, y_test = preprocessor.prepare_data(df)
        
        # Entrenar modelo
        model = XGBoostModel()
        model.train(X_train, y_train, X_test, y_test)
        
        # Crear explainer
        explainer = create_shap_explainer(model.model, X_train)
        
        # Tomar una muestra para demostración
        sample_customer = X_test.iloc[[0]]
        explanation = explainer.explain_single_prediction(sample_customer)
        
        # Generar visualización
        fig = explainer.create_waterfall_plot(sample_customer)
        
        # Convertir a base64
        buffer = io.BytesIO()
        fig.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
        buffer.seek(0)
        plot_base64 = base64.b64encode(buffer.getvalue()).decode()
        buffer.close()
        plt.close(fig)
        
        # Generar reporte completo
        report = explainer.generate_explanation_report(sample_customer, "demo_customer")
        
        return {
            "demo_info": {
                "customer_id": "demo_customer",
                "model_type": "XGBoost",
                "explanation_method": "SHAP",
                "features_analyzed": len(explainer.feature_names)
            },
            "prediction": report["prediction"],
            "explanation": {
                "base_score": report["explanation"]["base_score"],
                "final_score": report["explanation"]["final_score"],
                "summary": report["explanation"]["summary"]
            },
            "key_factors": {
                "top_positive": report["key_factors"]["positive"][:3],
                "top_negative": report["key_factors"]["negative"][:3],
                "risk_factors": report["key_factors"]["risk_factors"],
                "positive_factors": report["key_factors"]["positive_factors"]
            },
            "recommendations": report["recommendations"],
            "visualization": {
                "plot_type": "waterfall",
                "plot_data": plot_base64,
                "description": "Gráfico waterfall mostrando contribución de cada característica"
            },
            "timestamp": report["timestamp"]
        }
        
    except Exception as e:
        logger.error(f"Error en demo de explicabilidad: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error en demo de explicabilidad: {str(e)}"
        )

# Iniciar aplicación
if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Iniciando API con Explicabilidad SHAP")
    print("📊 Endpoints disponibles:")
    print("  • Scoring: /score, /score/batch")
    print("  • Explicabilidad: /explain, /explain/visualize, /explain/batch")
    print("  • Demo: /demo/explainability")
    print("  • Documentación: /docs")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
