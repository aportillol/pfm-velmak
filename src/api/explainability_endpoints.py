#!/usr/bin/env python3
"""
Endpoints de Explicabilidad para API PFM Velmak Scoring
=====================================================

Este módulo añade endpoints a la API para proporcionar explicaciones
detalladas de por qué el algoritmo asignó un puntaje específico
a un cliente usando SHAP.

Autor: PFM Velmak Team
Fecha: Marzo 2026
"""

from fastapi import HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import pandas as pd
import numpy as np
from datetime import datetime
import logging
import base64
import io
import matplotlib
matplotlib.use('Agg')  # Usar backend non-interactive
import matplotlib.pyplot as plt

# Importar módulos de explicabilidad
from src.explainability.shap_explainer import SHAPScoringExplainer, create_shap_explainer

logger = logging.getLogger(__name__)

# Modelos Pydantic para endpoints de explicabilidad
class ExplainabilityRequest(BaseModel):
    """Modelo para solicitud de explicación."""
    
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
    customer_id: Optional[str] = Field(None, description="ID del cliente")

class ExplainabilityResponse(BaseModel):
    """Modelo para respuesta de explicación."""
    
    customer_id: str = Field(..., description="ID del cliente")
    prediction: Dict[str, Any] = Field(..., description="Predicción y probabilidad")
    explanation: Dict[str, Any] = Field(..., description="Explicación detallada")
    key_factors: Dict[str, List[Dict[str, Any]]] = Field(..., description="Factores clave")
    recommendations: List[str] = Field(..., description="Recomendaciones")
    timestamp: str = Field(..., description="Timestamp de la explicación")

class VisualizationRequest(BaseModel):
    """Modelo para solicitud de visualización."""
    
    explanation_request: ExplainabilityRequest = Field(..., description="Datos del cliente")
    plot_type: str = Field(..., description="Tipo de gráfico: 'waterfall', 'force', 'summary'")

class VisualizationResponse(BaseModel):
    """Modelo para respuesta de visualización."""
    
    plot_type: str = Field(..., description="Tipo de gráfico generado")
    plot_data: str = Field(..., description="Gráfico en base64")
    explanation: str = Field(..., description="Descripción del gráfico")
    timestamp: str = Field(..., description="Timestamp de generación")

class BatchExplainabilityRequest(BaseModel):
    """Modelo para solicitud de explicación por lotes."""
    
    customers: List[ExplainabilityRequest] = Field(..., description="Lista de clientes a explicar")

# Variables globales para el explainer
shap_explainer: Optional[SHAPScoringExplainer] = None
model_loaded = False

def load_explainer():
    """
    Cargar el explainer SHAP y el modelo.
    """
    global shap_explainer, model_loaded
    
    if model_loaded:
        return True
    
    try:
        # Importar aquí para evitar importaciones circulares
        from src.models.baseline_models import XGBoostModel
        from src.data.preprocessing import ScoringPreprocessor
        import pandas as pd
        
        # Cargar y preprocesar datos para el explainer
        data_path = "data/raw/datos.csv"
        df = pd.read_csv(data_path)
        
        preprocessor = ScoringPreprocessor()
        X_train, X_test, y_train, y_test = preprocessor.prepare_data(df)
        
        # Cargar modelo entrenado (o crear uno temporal)
        model = XGBoostModel()
        model.train(X_train, y_train, X_test, y_test)
        
        # Crear explainer
        shap_explainer = create_shap_explainer(model.model, X_train)
        model_loaded = True
        
        logger.info("Explainer SHAP cargado exitosamente")
        return True
        
    except Exception as e:
        logger.error(f"Error cargando explainer: {str(e)}")
        return False

def prepare_customer_data(request: ExplainabilityRequest) -> pd.DataFrame:
    """
    Preparar datos del cliente para el explainer.
    
    Args:
        request: Solicitud con datos del cliente
        
    Returns:
        pd.DataFrame: Datos preparados
    """
    try:
        # Crear DataFrame con los datos del cliente
        customer_data = {
            'edad': request.edad,
            'ingresos_mensuales': request.ingresos_mensuales,
            'deuda_existente': request.deuda_existente,
            'antiguedad_laboral': request.antiguedad_laboral,
            'tiene_propiedad': 1 if request.tiene_propiedad else 0,
            'tarjetas_credito': request.tarjetas_credito,
            'consultas_recientes': request.consultas_recientes,
            'impagos_previos': request.impagos_previos,
            'score_bureau': request.score_bureau
        }
        
        # Añadir tipo_contrato codificado
        contract_mapping = {'permanente': 3, 'autonomo': 2, 'temporal': 1}
        customer_data['tipo_contrato_encoded'] = contract_mapping.get(request.tipo_contrato, 1)
        
        # Crear características engineered (simuladas para el ejemplo)
        customer_data.update({
            'ratio_deuda_ingresos': customer_data['deuda_existente'] / customer_data['ingresos_mensuales'],
            'ratio_consulta_edad': customer_data['consultas_recientes'] / customer_data['edad'],
            'ratio_tarjetas_ingresos': customer_data['tarjetas_credito'] / customer_data['ingresos_mensuales'],
            'score_estabilidad_laboral': customer_data['antiguedad_laboral'] * contract_mapping.get(request.tipo_contrato, 1),
            'score_capacidad_financiera': (customer_data['ingresos_mensuales'] - customer_data['deuda_existente']) / customer_data['ingresos_mensuales'],
            'score_riesgo_combinado': customer_data['score_bureau'] * 0.4 + (1 - customer_data['ratio_deuda_ingresos']) * 100 * 0.3 + (1 - customer_data['impagos_previos'] / 2) * 100 * 0.3,
            'indice_salud_financiera': (customer_data['score_bureau'] / 100 + customer_data['score_capacidad_financiera'] + 0.5) / 3
        })
        
        df = pd.DataFrame([customer_data])
        
        # Asegurar que todas las características necesarias estén presentes
        if shap_explainer:
            for feature in shap_explainer.feature_names:
                if feature not in df.columns:
                    df[feature] = 0  # Valor por defecto
        
        # Seleccionar solo las características del explainer
        if shap_explainer:
            df = df[shap_explainer.feature_names]
        
        return df
        
    except Exception as e:
        logger.error(f"Error preparando datos del cliente: {str(e)}")
        raise

def create_plot_base64(fig) -> str:
    """
    Convertir figura de matplotlib a base64.
    
    Args:
        fig: Figura de matplotlib
        
    Returns:
        str: Imagen en base64
    """
    try:
        # Guardar figura en buffer
        buffer = io.BytesIO()
        fig.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
        buffer.seek(0)
        
        # Convertir a base64
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        # Cerrar buffer
        buffer.close()
        plt.close(fig)
        
        return image_base64
        
    except Exception as e:
        logger.error(f"Error convirtiendo gráfico a base64: {str(e)}")
        raise

# Endpoints de explicabilidad
def explain_scoring_endpoint(request: ExplainabilityRequest):
    """
    Endpoint principal para explicar scoring.
    
    Args:
        request: Solicitud de explicación
        
    Returns:
        ExplainabilityResponse: Explicación detallada
    """
    try:
        # Cargar explainer si no está cargado
        if not load_explainer():
            raise HTTPException(
                status_code=500,
                detail="Error cargando el modelo de explicación"
            )
        
        # Preparar datos del cliente
        customer_data = prepare_customer_data(request)
        
        # Generar explicación
        explanation = shap_explainer.explain_single_prediction(customer_data)
        
        # Generar reporte completo
        report = shap_explainer.generate_explanation_report(
            customer_data, 
            request.customer_id or "unknown"
        )
        
        # Formatear respuesta
        response = ExplainabilityResponse(
            customer_id=report["customer_id"],
            prediction=report["prediction"],
            explanation={
                "base_score": report["explanation"]["base_score"],
                "final_score": report["explanation"]["final_score"],
                "summary": report["explanation"]["summary"]
            },
            key_factors={
                "positive": report["key_factors"]["positive"],
                "negative": report["key_factors"]["negative"],
                "risk_factors": report["key_factors"]["risk_factors"],
                "positive_factors": report["key_factors"]["positive_factors"]
            },
            recommendations=report["recommendations"],
            timestamp=report["timestamp"]
        )
        
        logger.info(f"Explicación generada para cliente: {request.customer_id}")
        return response
        
    except Exception as e:
        logger.error(f"Error en endpoint de explicación: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generando explicación: {str(e)}"
        )

def explain_visualization_endpoint(request: VisualizationRequest):
    """
    Endpoint para generar visualizaciones de explicación.
    
    Args:
        request: Solicitud de visualización
        
    Returns:
        VisualizationResponse: Visualización en base64
    """
    try:
        # Cargar explainer si no está cargado
        if not load_explainer():
            raise HTTPException(
                status_code=500,
                detail="Error cargando el modelo de explicación"
            )
        
        # Preparar datos del cliente
        customer_data = prepare_customer_data(request.explanation_request)
        
        # Generar visualización según el tipo solicitado
        if request.plot_type == "waterfall":
            fig = shap_explainer.create_waterfall_plot(customer_data)
            explanation = "Gráfico waterfall mostrando cómo cada característica contribuye a la predicción final"
            
        elif request.plot_type == "force":
            fig = shap_explainer.create_force_plot(customer_data)
            explanation = "Gráfico force mostrando las fuerzas que empujan la predicción hacia arriba o abajo"
            
        elif request.plot_type == "summary":
            # Para summary, necesitamos más datos de fondo
            from src.data.preprocessing import ScoringPreprocessor
            import pandas as pd
            
            df = pd.read_csv("data/raw/datos.csv")
            preprocessor = ScoringPreprocessor()
            X_train, X_test, y_train, y_test = preprocessor.prepare_data(df)
            
            fig = shap_explainer.create_summary_plot(X_test.sample(50))
            explanation = "Gráfico summary mostrando la importancia global de características"
            
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Tipo de gráfico no soportado: {request.plot_type}"
            )
        
        # Convertir a base64
        plot_base64 = create_plot_base64(fig)
        
        response = VisualizationResponse(
            plot_type=request.plot_type,
            plot_data=plot_base64,
            explanation=explanation,
            timestamp=datetime.now().isoformat()
        )
        
        logger.info(f"Visualización {request.plot_type} generada para cliente: {request.explanation_request.customer_id}")
        return response
        
    except Exception as e:
        logger.error(f"Error generando visualización: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generando visualización: {str(e)}"
        )

def explain_batch_endpoint(request: BatchExplainabilityRequest):
    """
    Endpoint para explicación por lotes.
    
    Args:
        request: Solicitud de explicación por lotes
        
    Returns:
        Dict: Explicaciones para todos los clientes
    """
    try:
        # Cargar explainer si no está cargado
        if not load_explainer():
            raise HTTPException(
                status_code=500,
                detail="Error cargando el modelo de explicación"
            )
        
        results = []
        
        for i, customer_request in enumerate(request.customers):
            try:
                # Generar explicación individual
                explanation = explain_scoring_endpoint(customer_request)
                
                # Añadir información adicional
                result = {
                    "customer_id": customer_request.customer_id or f"customer_{i+1}",
                    "prediction": explanation.prediction,
                    "risk_factors": explanation.key_factors["risk_factors"],
                    "positive_factors": explanation.key_factors["positive_factors"],
                    "recommendations": explanation.recommendations
                }
                
                results.append(result)
                
            except Exception as e:
                logger.error(f"Error explicando cliente {i+1}: {str(e)}")
                results.append({
                    "customer_id": customer_request.customer_id or f"customer_{i+1}",
                    "error": str(e),
                    "prediction": None,
                    "risk_factors": [],
                    "positive_factors": [],
                    "recommendations": []
                })
        
        # Estadísticas del batch
        total_customers = len(results)
        successful_explanations = len([r for r in results if "error" not in r])
        approved_customers = len([r for r in results if r.get("prediction", {}).get("decision") == "APROBADO"])
        
        return {
            "results": results,
            "statistics": {
                "total_customers": total_customers,
                "successful_explanations": successful_explanations,
                "approved_customers": approved_customers,
                "approval_rate": approved_customers / total_customers if total_customers > 0 else 0
            }
        }
        
    except Exception as e:
        logger.error(f"Error en explicación por lotes: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error en explicación por lotes: {str(e)}"
        )

def get_explainability_info_endpoint():
    """
    Endpoint para obtener información sobre capacidades de explicabilidad.
    
    Returns:
        Dict: Información sobre capacidades
    """
    try:
        info = {
            "explainability_methods": ["SHAP"],
            "supported_plot_types": ["waterfall", "force", "summary"],
            "features_available": shap_explainer.feature_names if shap_explainer else [],
            "model_type": "Tree-based (XGBoost)",
            "explanation_types": [
                "individual_predictions",
                "feature_importance",
                "risk_factors",
                "recommendations",
                "visual_explanations"
            ],
            "capabilities": {
                "local_explanations": True,
                "global_explanations": True,
                "feature_attribution": True,
                "counterfactuals": False,
                "rule_based": False
            }
        }
        
        return info
        
    except Exception as e:
        logger.error(f"Error obteniendo información de explicabilidad: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error obteniendo información: {str(e)}"
        )

# Función para añadir endpoints a la API principal
def add_explainability_endpoints(app):
    """
    Añadir endpoints de explicabilidad a la aplicación FastAPI.
    
    Args:
        app: Aplicación FastAPI
    """
    
    @app.post("/explain", response_model=ExplainabilityResponse, tags=["Explicabilidad"])
    async def explain_scoring(request: ExplainabilityRequest):
        """
        Explicar por qué el algoritmo asignó un puntaje específico a un cliente.
        
        Este endpoint utiliza SHAP para proporcionar una explicación detallada
        de cómo cada característica contribuyó a la decisión de scoring.
        """
        return explain_scoring_endpoint(request)
    
    @app.post("/explain/visualize", response_model=VisualizationResponse, tags=["Explicabilidad"])
    async def explain_visualization(request: VisualizationRequest):
        """
        Generar visualizaciones explicativas de la decisión de scoring.
        
        Proporciona gráficos interactivos (waterfall, force, summary) que
        muestran visualmente cómo cada característica afecta la predicción.
        """
        return explain_visualization_endpoint(request)
    
    @app.post("/explain/batch", tags=["Explicabilidad"])
    async def explain_batch(request: BatchExplainabilityRequest):
        """
        Generar explicaciones para múltiples clientes simultáneamente.
        
        Útil para análisis por lotes y reportes de auditoría.
        """
        return explain_batch_endpoint(request)
    
    @app.get("/explain/info", tags=["Explicabilidad"])
    async def get_explainability_info():
        """
        Obtener información sobre las capacidades de explicabilidad del sistema.
        
        Proporciona detalles sobre los métodos de explicación disponibles
        y las características que pueden ser explicadas.
        """
        return get_explainability_info_endpoint()
    
    logger.info("Endpoints de explicabilidad añadidos a la API")
