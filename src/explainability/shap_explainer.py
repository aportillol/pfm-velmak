#!/usr/bin/env python3
"""
Módulo de Explicabilidad con SHAP para PFM Velmak Scoring
========================================================

Este módulo implementa explicabilidad de modelos usando SHAP para
interpretar por qué el algoritmo asignó un puntaje específico
a un cliente particular.

Autor: PFM Velmak Team
Fecha: Marzo 2026
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import shap
from typing import Dict, List, Any, Optional, Tuple
import warnings
warnings.filterwarnings('ignore')

# Configuración de visualización
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class SHAPScoringExplainer:
    """
    Clase para explicar predicciones de scoring crediticio usando SHAP.
    """
    
    def __init__(self, model, feature_names: List[str], background_data: pd.DataFrame = None):
        """
        Inicializar el explainer SHAP.
        
        Args:
            model: Modelo entrenado de scoring
            feature_names: Lista de nombres de características
            background_data: Datos de fondo para el explainer (opcional)
        """
        self.model = model
        self.feature_names = feature_names
        self.background_data = background_data
        self.explainer = None
        self.shap_values = None
        self.expected_value = None
        
    def initialize_explainer(self, background_data: pd.DataFrame = None):
        """
        Inicializar el explainer SHAP.
        
        Args:
            background_data: Datos de fondo para el explainer
        """
        try:
            # Usar datos de fondo proporcionados o los guardados
            bg_data = background_data or self.background_data
            
            if bg_data is None:
                raise ValueError("Se requieren datos de fondo para inicializar el explainer")
            
            # Crear explainer TreeSHAP (óptimo para modelos basados en árboles)
            self.explainer = shap.TreeExplainer(
                self.model, 
                bg_data, 
                feature_names=self.feature_names,
                model_output="probability"
            )
            
            # Calcular expected value
            self.expected_value = self.explainer.expected_value
            
            print(f"✅ Explainer SHAP inicializado")
            print(f"   Expected value: {self.expected_value:.4f}")
            print(f"   Background samples: {len(bg_data)}")
            
        except Exception as e:
            print(f"❌ Error inicializando explainer: {str(e)}")
            raise
    
    def explain_single_prediction(self, X_instance: pd.DataFrame) -> Dict[str, Any]:
        """
        Explicar una predicción individual.
        
        Args:
            X_instance: DataFrame con una sola instancia a explicar
            
        Returns:
            Dict: Explicación completa de la predicción
        """
        if self.explainer is None:
            raise ValueError("El explainer no está inicializado. Llama a initialize_explainer() primero.")
        
        try:
            # Calcular valores SHAP
            shap_values = self.explainer.shap_values(X_instance)
            
            # Para modelos binarios, shap_values es una lista [clase_0, clase_1]
            if isinstance(shap_values, list):
                shap_values_positive = shap_values[1]  # Valores para clase positiva (aprobado)
            else:
                shap_values_positive = shap_values
            
            # Predicción del modelo
            prediction = self.model.predict(X_instance)[0]
            prediction_proba = self.model.predict_proba(X_instance)[0, 1]
            
            # Crear explicación estructurada
            explanation = {
                "prediction": prediction,
                "prediction_probability": prediction_proba,
                "base_value": self.expected_value if isinstance(self.expected_value, (int, float)) else self.expected_value[1],
                "shap_values": shap_values_positive[0],
                "feature_names": self.feature_names,
                "feature_values": X_instance.iloc[0].values,
                "explanation_text": self._generate_explanation_text(shap_values_positive[0], X_instance.iloc[0]),
                "top_positive_features": self._get_top_features(shap_values_positive[0], X_instance.iloc[0], top_k=5, positive=True),
                "top_negative_features": self._get_top_features(shap_values_positive[0], X_instance.iloc[0], top_k=5, positive=False),
                "risk_factors": self._identify_risk_factors(shap_values_positive[0], X_instance.iloc[0]),
                "positive_factors": self._identify_positive_factors(shap_values_positive[0], X_instance.iloc[0])
            }
            
            return explanation
            
        except Exception as e:
            print(f"❌ Error explicando predicción: {str(e)}")
            raise
    
    def _generate_explanation_text(self, shap_values: np.ndarray, feature_values: pd.Series) -> str:
        """
        Generar texto explicativo legible.
        
        Args:
            shap_values: Valores SHAP
            feature_values: Valores de características
            
        Returns:
            str: Texto explicativo
        """
        try:
            # Obtener características más influyentes
            abs_shap = np.abs(shap_values)
            top_indices = np.argsort(abs_shap)[-5:][::-1]
            
            explanation_parts = []
            
            for idx in top_indices:
                feature_name = self.feature_names[idx]
                shap_val = shap_values[idx]
                feature_val = feature_values.iloc[idx]
                
                if shap_val > 0:
                    explanation_parts.append(
                        f"• {feature_name}={feature_val:.2f} contribuye positivamente (+{shap_val:.3f})"
                    )
                else:
                    explanation_parts.append(
                        f"• {feature_name}={feature_val:.2f} contribuye negativemente ({shap_val:.3f})"
                    )
            
            return "\n".join(explanation_parts)
            
        except Exception as e:
            return f"Error generando explicación: {str(e)}"
    
    def _get_top_features(self, shap_values: np.ndarray, feature_values: pd.Series, top_k: int = 5, positive: bool = True) -> List[Dict]:
        """
        Obtener las características más influyentes.
        
        Args:
            shap_values: Valores SHAP
            feature_values: Valores de características
            top_k: Número de características a retornar
            positive: True para positivas, False para negativas
            
        Returns:
            List[Dict]: Lista de características con sus valores SHAP
        """
        try:
            # Filtrar por signo
            if positive:
                indices = np.where(shap_values > 0)[0]
            else:
                indices = np.where(shap_values < 0)[0]
            
            # Ordenar por magnitud
            shap_magnitude = np.abs(shap_values[indices])
            sorted_indices = indices[np.argsort(shap_magnitude)][::-1]
            
            # Tomar top_k
            top_indices = sorted_indices[:top_k]
            
            features = []
            for idx in top_indices:
                features.append({
                    "feature": self.feature_names[idx],
                    "value": feature_values.iloc[idx],
                    "shap_value": shap_values[idx],
                    "impact": "positive" if shap_values[idx] > 0 else "negative",
                    "magnitude": abs(shap_values[idx])
                })
            
            return features
            
        except Exception as e:
            print(f"Error obteniendo top features: {str(e)}")
            return []
    
    def _identify_risk_factors(self, shap_values: np.ndarray, feature_values: pd.Series) -> List[str]:
        """
        Identificar factores de riesgo basados en valores SHAP negativos.
        
        Args:
            shap_values: Valores SHAP
            feature_values: Valores de características
            
        Returns:
            List[str]: Lista de factores de riesgo identificados
        """
        risk_factors = []
        
        # Características con impacto negativo significativo
        negative_indices = np.where(shap_values < -0.01)[0]
        
        for idx in negative_indices:
            feature_name = self.feature_names[idx]
            feature_val = feature_values.iloc[idx]
            shap_val = shap_values[idx]
            
            # Generar descripción del factor de riesgo
            if feature_name == "impagos_previos":
                if feature_val > 0:
                    risk_factors.append(f"Antecedentes de impagos ({feature_val})")
            elif feature_name == "consultas_recientes":
                if feature_val > 2:
                    risk_factors.append(f"Múltiples consultas de crédito recientes ({feature_val})")
            elif feature_name == "tarjetas_credito":
                if feature_val > 3:
                    risk_factors.append(f"Excesivo número de tarjetas ({feature_val})")
            elif feature_name == "ratio_deuda_ingresos":
                if feature_val > 0.5:
                    risk_factors.append(f"Alta ratio deuda/ingresos ({feature_val:.2%})")
            elif feature_name == "score_bureau":
                if feature_val < 600:
                    risk_factors.append(f"Score bureau bajo ({feature_val})")
            elif feature_name == "edad":
                if feature_val < 25:
                    risk_factors.append(f"Edad joven ({feature_val} años)")
            elif feature_name == "antiguedad_laboral":
                if feature_val < 2:
                    risk_factors.append(f"Baja antigüedad laboral ({feature_val} años)")
            elif feature_name == "deuda_existente":
                if feature_val > 1000:
                    risk_factors.append(f"Deuda existente elevada (€{feature_val})")
        
        return risk_factors
    
    def _identify_positive_factors(self, shap_values: np.ndarray, feature_values: pd.Series) -> List[str]:
        """
        Identificar factores positivos basados en valores SHAP positivos.
        
        Args:
            shap_values: Valores SHAP
            feature_values: Valores de características
            
        Returns:
            List[str]: Lista de factores positivos identificados
        """
        positive_factors = []
        
        # Características con impacto positivo significativo
        positive_indices = np.where(shap_values > 0.01)[0]
        
        for idx in positive_indices:
            feature_name = self.feature_names[idx]
            feature_val = feature_values.iloc[idx]
            shap_val = shap_values[idx]
            
            # Generar descripción del factor positivo
            if feature_name == "score_bureau":
                if feature_val > 750:
                    positive_factors.append(f"Score bureau excelente ({feature_val})")
            elif feature_name == "edad":
                if feature_val > 40:
                    positive_factors.append(f"Edad madura y estable ({feature_val} años)")
            elif feature_name == "ingresos_mensuales":
                if feature_val > 4000:
                    positive_factors.append(f"Ingresos elevados (€{feature_val})")
            elif feature_name == "antiguedad_laboral":
                if feature_val > 5:
                    positive_factors.append(f"Buena estabilidad laboral ({feature_val} años)")
            elif feature_name == "tiene_propiedad":
                if feature_val == 1:
                    positive_factors.append("Posee propiedades")
            elif feature_name == "tipo_contrato_encoded":
                if feature_val == 3:  # permanente
                    positive_factors.append("Contrato permanente")
            elif feature_name == "ratio_deuda_ingresos":
                if feature_val < 0.3:
                    positive_factors.append(f"Baja ratio deuda/ingresos ({feature_val:.2%})")
            elif feature_name == "indice_salud_financiera":
                if feature_val > 0.7:
                    positive_factors.append(f"Excelente salud financiera ({feature_val:.2%})")
        
        return positive_factors
    
    def create_waterfall_plot(self, X_instance: pd.DataFrame, save_path: str = None) -> plt.Figure:
        """
        Crear gráfico waterfall para una predicción.
        
        Args:
            X_instance: DataFrame con una sola instancia
            save_path: Ruta para guardar el gráfico (opcional)
            
        Returns:
            plt.Figure: Figura del gráfico waterfall
        """
        try:
            # Calcular valores SHAP
            shap_values = self.explainer.shap_values(X_instance)
            
            if isinstance(shap_values, list):
                shap_values_positive = shap_values[1]
            else:
                shap_values_positive = shap_values
            
            # Crear gráfico waterfall
            fig = plt.figure(figsize=(12, 8))
            
            shap.waterfall_plot(
                shap.Explanation(
                    values=shap_values_positive[0],
                    base_values=self.expected_value if isinstance(self.expected_value, (int, float)) else self.expected_value[1],
                    data=X_instance.iloc[0],
                    feature_names=self.feature_names
                ),
                max_display=10,
                show=False
            )
            
            plt.title("Explicación SHAP - Predicción de Scoring", fontsize=14, fontweight='bold')
            plt.tight_layout()
            
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                print(f"📊 Gráfico waterfall guardado en {save_path}")
            
            return fig
            
        except Exception as e:
            print(f"❌ Error creando gráfico waterfall: {str(e)}")
            raise
    
    def create_force_plot(self, X_instance: pd.DataFrame, save_path: str = None) -> plt.Figure:
        """
        Crear gráfico force plot para una predicción.
        
        Args:
            X_instance: DataFrame con una sola instancia
            save_path: Ruta para guardar el gráfico (opcional)
            
        Returns:
            plt.Figure: Figura del gráfico force
        """
        try:
            # Calcular valores SHAP
            shap_values = self.explainer.shap_values(X_instance)
            
            if isinstance(shap_values, list):
                shap_values_positive = shap_values[1]
            else:
                shap_values_positive = shap_values
            
            # Crear gráfico force
            fig = plt.figure(figsize=(12, 6))
            
            shap.force_plot(
                self.expected_value if isinstance(self.expected_value, (int, float)) else self.expected_value[1],
                shap_values_positive[0],
                X_instance.iloc[0],
                feature_names=self.feature_names,
                matplotlib=True,
                show=False
            )
            
            plt.title("Explicación SHAP - Fuerza de Características", fontsize=14, fontweight='bold')
            plt.tight_layout()
            
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                print(f"📊 Gráfico force guardado en {save_path}")
            
            return fig
            
        except Exception as e:
            print(f"❌ Error creando gráfico force: {str(e)}")
            raise
    
    def create_summary_plot(self, background_data: pd.DataFrame, save_path: str = None) -> plt.Figure:
        """
        Crear gráfico summary para múltiples instancias.
        
        Args:
            background_data: DataFrame con múltiples instancias
            save_path: Ruta para guardar el gráfico (opcional)
            
        Returns:
            plt.Figure: Figura del gráfico summary
        """
        try:
            # Calcular valores SHAP para múltiples instancias
            shap_values = self.explainer.shap_values(background_data)
            
            if isinstance(shap_values, list):
                shap_values_positive = shap_values[1]
            else:
                shap_values_positive = shap_values
            
            # Crear gráfico summary
            fig = plt.figure(figsize=(12, 8))
            
            shap.summary_plot(
                shap_values_positive,
                background_data,
                feature_names=self.feature_names,
                plot_type="bar",
                show=False
            )
            
            plt.title("Importancia Global de Características", fontsize=14, fontweight='bold')
            plt.tight_layout()
            
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                print(f"📊 Gráfico summary guardado en {save_path}")
            
            return fig
            
        except Exception as e:
            print(f"❌ Error creando gráfico summary: {str(e)}")
            raise
    
    def generate_explanation_report(self, X_instance: pd.DataFrame, customer_id: str = None) -> Dict[str, Any]:
        """
        Generar un reporte completo de explicación para un cliente.
        
        Args:
            X_instance: DataFrame con datos del cliente
            customer_id: ID del cliente (opcional)
            
        Returns:
            Dict: Reporte completo de explicación
        """
        try:
            # Obtener explicación detallada
            explanation = self.explain_single_prediction(X_instance)
            
            # Generar reporte estructurado
            report = {
                "customer_id": customer_id or "unknown",
                "timestamp": pd.Timestamp.now().isoformat(),
                "prediction": {
                    "decision": "APROBADO" if explanation["prediction"] == 1 else "RECHAZADO",
                    "probability": explanation["prediction_probability"],
                    "confidence": "ALTA" if explanation["prediction_probability"] > 0.8 else "MEDIA" if explanation["prediction_probability"] > 0.6 else "BAJA"
                },
                "explanation": {
                    "base_score": explanation["base_value"],
                    "final_score": explanation["base_value"] + np.sum(explanation["shap_values"]),
                    "summary": explanation["explanation_text"]
                },
                "key_factors": {
                    "positive": explanation["top_positive_features"],
                    "negative": explanation["top_negative_factors"],
                    "risk_factors": explanation["risk_factors"],
                    "positive_factors": explanation["positive_factors"]
                },
                "recommendations": self._generate_recommendations(explanation)
            }
            
            return report
            
        except Exception as e:
            print(f"❌ Error generando reporte: {str(e)}")
            raise
    
    def _generate_recommendations(self, explanation: Dict[str, Any]) -> List[str]:
        """
        Generar recomendaciones basadas en la explicación.
        
        Args:
            explanation: Explicación SHAP
            
        Returns:
            List[str]: Lista de recomendaciones
        """
        recommendations = []
        
        # Basado en factores de riesgo
        risk_factors = explanation["risk_factors"]
        
        if "impagos" in str(risk_factors):
            recommendations.append("Revisar historial de pagos y establecer plan de regularización")
        
        if "consultas" in str(risk_factors):
            recommendations.append("Evitar múltiples solicitudes de crédito en corto período")
        
        if "tarjetas" in str(risk_factors):
            recommendations.append("Consolidar deudas de tarjetas y reducir número de tarjetas")
        
        if "deuda" in str(risk_factors):
            recommendations.append("Reducir ratio deuda/ingresos por debajo del 30%")
        
        if "score bureau" in str(risk_factors):
            recommendations.append("Mejorar score bureau pagando puntualmente todas las deudas")
        
        # Basado en factores positivos
        positive_factors = explanation["positive_factors"]
        
        if len(positive_factors) > 0:
            recommendations.append("Mantener los factores positivos actuales")
        
        # Recomendaciones generales
        if explanation["prediction_probability"] < 0.5:
            recommendations.append("Considerar esperar 3-6 meses y mejorar perfil crediticio")
            recommendations.append("Buscar garantías o co-deudores para mejorar aprobación")
        
        return recommendations
    
    def save_explanation(self, explanation: Dict[str, Any], filepath: str):
        """
        Guardar explicación en archivo JSON.
        
        Args:
            explanation: Explicación a guardar
            filepath: Ruta del archivo
        """
        try:
            import json
            
            # Convertir arrays numpy a listas para JSON
            explanation_copy = explanation.copy()
            if "shap_values" in explanation_copy:
                explanation_copy["shap_values"] = explanation_copy["shap_values"].tolist()
            
            with open(filepath, 'w') as f:
                json.dump(explanation_copy, f, indent=2, default=str)
            
            print(f"💾 Explicación guardada en {filepath}")
            
        except Exception as e:
            print(f"❌ Error guardando explicación: {str(e)}")

# Función de utilidad para crear explainer
def create_shap_explainer(model, X_train: pd.DataFrame) -> SHAPScoringExplainer:
    """
    Crear explainer SHAP para un modelo de scoring.
    
    Args:
        model: Modelo entrenado
        X_train: Datos de entrenamiento
        
    Returns:
        SHAPScoringExplainer: Explainer configurado
    """
    feature_names = X_train.columns.tolist()
    
    # Usar muestra de datos de fondo para eficiencia
    background_sample = X_train.sample(min(100, len(X_train)), random_state=42)
    
    explainer = SHAPScoringExplainer(model, feature_names, background_sample)
    explainer.initialize_explainer()
    
    return explainer

# Ejemplo de uso
def example_usage():
    """
    Ejemplo de uso del módulo SHAP.
    """
    from src.models.baseline_models import XGBoostModel
    from src.data.preprocessing import ScoringPreprocessor
    import pandas as pd
    
    # Cargar datos y preprocesar
    df = pd.read_csv("data/raw/datos.csv")
    preprocessor = ScoringPreprocessor()
    X_train, X_test, y_train, y_test = preprocessor.prepare_data(df)
    
    # Entrenar modelo
    model = XGBoostModel()
    model.train(X_train, y_train, X_test, y_test)
    
    # Crear explainer
    explainer = create_shap_explainer(model.model, X_train)
    
    # Explicar una predicción
    sample_customer = X_test.iloc[[0]]  # Primera muestra
    explanation = explainer.explain_single_prediction(sample_customer)
    
    # Generar reporte completo
    report = explainer.generate_explanation_report(sample_customer, "customer_001")
    
    # Crear visualizaciones
    explainer.create_waterfall_plot(sample_customer, "waterfall_customer_001.png")
    explainer.create_force_plot(sample_customer, "force_customer_001.png")
    
    # Guardar explicación
    explainer.save_explanation(explanation, "explanation_customer_001.json")
    
    print("✅ Ejemplo completado exitosamente")
    return explainer, explanation, report

if __name__ == "__main__":
    explainer, explanation, report = example_usage()
