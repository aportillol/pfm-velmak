#!/usr/bin/env python3
"""
Modelos Baseline para PFM Velmak Scoring
===========================================

Este módulo contiene modelos baseline para evaluación crediticia
incluyendo regresión logística, random forest y XGBoost.

Autor: PFM Velmak Team
Fecha: Marzo 2026
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report,
    roc_curve, precision_recall_curve
)
import xgboost as xgb
import shap
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Tuple, Any
import warnings
warnings.filterwarnings('ignore')

class BaselineScoringModel:
    """
    Clase base para modelos de scoring crediticio.
    """
    
    def __init__(self, model_name: str = "baseline"):
        self.model_name = model_name
        self.model = None
        self.feature_names = []
        self.is_fitted = False
        self.metrics = {}
        
    def train(self, X_train, y_train, X_val=None, y_val=None):
        """
        Método abstracto para entrenar el modelo.
        
        Args:
            X_train: Características de entrenamiento
            y_train: Target de entrenamiento
            X_val: Características de validación (opcional)
            y_val: Target de validación (opcional)
        """
        raise NotImplementedError("Subclass must implement train method")
    
    def predict(self, X):
        """
        Realizar predicciones.
        
        Args:
            X: Características para predicción
            
        Returns:
            np.array: Predicciones
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before prediction")
        return self.model.predict(X)
    
    def predict_proba(self, X):
        """
        Realizar predicciones de probabilidad.
        
        Args:
            X: Características para predicción
            
        Returns:
            np.array: Probabilidades predichas
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before prediction")
        return self.model.predict_proba(X)
    
    def evaluate(self, X_test, y_test):
        """
        Evaluar el modelo con métricas completas.
        
        Args:
            X_test: Características de prueba
            y_test: Target de prueba
            
        Returns:
            dict: Métricas de evaluación
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before evaluation")
        
        # Predicciones
        y_pred = self.predict(X_test)
        y_proba = self.predict_proba(X_test)[:, 1]
        
        # Calcular métricas
        self.metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred),
            'recall': recall_score(y_test, y_pred),
            'f1_score': f1_score(y_test, y_pred),
            'roc_auc': roc_auc_score(y_test, y_proba)
        }
        
        return self.metrics
    
    def get_feature_importance(self):
        """
        Obtener importancia de características.
        
        Returns:
            dict: Importancia de características
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before getting feature importance")
        
        if hasattr(self.model, 'feature_importances_'):
            importance_dict = dict(zip(self.feature_names, self.model.feature_importances_))
            # Ordenar por importancia
            return dict(sorted(importance_dict.items(), key=lambda x: x[1], reverse=True))
        else:
            return {}
    
    def explain_prediction(self, X_instance):
        """
        Explicar una predicción usando SHAP.
        
        Args:
            X_instance: Instancia a explicar
            
        Returns:
            shap.Explanation: Explicación SHAP
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before explanation")
        
        # Crear explainer SHAP
        explainer = shap.Explainer(self.model, X_instance, feature_names=self.feature_names)
        shap_values = explainer(X_instance)
        
        return shap_values


class LogisticRegressionModel(BaselineScoringModel):
    """
    Modelo de Regresión Logística para scoring crediticio.
    """
    
    def __init__(self):
        super().__init__("logistic_regression")
        self.model = LogisticRegression(
            random_state=42,
            max_iter=1000,
            class_weight='balanced',
            solver='liblinear'
        )
    
    def train(self, X_train, y_train, X_val=None, y_val=None):
        """
        Entrenar modelo de regresión logística.
        """
        print(f"Entrenando modelo: {self.model_name}")
        
        # Guardar nombres de características
        self.feature_names = X_train.columns.tolist()
        
        # Entrenar modelo
        self.model.fit(X_train, y_train)
        self.is_fitted = True
        
        # Calcular métricas de entrenamiento
        train_score = self.model.score(X_train, y_train)
        print(f"Entrenamiento completado. Accuracy train: {train_score:.4f}")
        
        # Validación si se proporcionan datos
        if X_val is not None and y_val is not None:
            val_score = self.model.score(X_val, y_val)
            print(f"Accuracy validacion: {val_score:.4f}")
            
            # Métricas completas de validación
            val_metrics = self.evaluate(X_val, y_val)
            print(f"Métricas de validación:")
            for metric, value in val_metrics.items():
                print(f"  • {metric}: {value:.4f}")
        
        return self


class RandomForestModel(BaselineScoringModel):
    """
    Modelo Random Forest para scoring crediticio.
    """
    
    def __init__(self, n_estimators=100, max_depth=10):
        super().__init__("random_forest")
        self.model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=42,
            class_weight='balanced',
            n_jobs=-1
        )
    
    def train(self, X_train, y_train, X_val=None, y_val=None):
        """
        Entrenar modelo Random Forest.
        """
        print(f"Entrenando modelo: {self.model_name}")
        
        # Guardar nombres de características
        self.feature_names = X_train.columns.tolist()
        
        # Entrenar modelo
        self.model.fit(X_train, y_train)
        self.is_fitted = True
        
        # Calcular métricas de entrenamiento
        train_score = self.model.score(X_train, y_train)
        print(f"Entrenamiento completado. Accuracy train: {train_score:.4f}")
        
        # Importancia de características
        importance = self.get_feature_importance()
        print(f"Top 5 características importantes:")
        for i, (feature, score) in enumerate(list(importance.items())[:5]):
            print(f"  {i+1}. {feature}: {score:.4f}")
        
        # Validación si se proporcionan datos
        if X_val is not None and y_val is not None:
            val_score = self.model.score(X_val, y_val)
            print(f"Accuracy validacion: {val_score:.4f}")
            
            # Métricas completas de validación
            val_metrics = self.evaluate(X_val, y_val)
            print(f"Métricas de validación:")
            for metric, value in val_metrics.items():
                print(f"  • {metric}: {value:.4f}")
        
        return self


class XGBoostModel(BaselineScoringModel):
    """
    Modelo XGBoost para scoring crediticio.
    """
    
    def __init__(self, n_estimators=100, max_depth=6, learning_rate=0.1):
        super().__init__("xgboost")
        self.model = xgb.XGBClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            learning_rate=learning_rate,
            random_state=42,
            eval_metric='logloss',
            use_label_encoder=False,
            n_jobs=-1
        )
    
    def train(self, X_train, y_train, X_val=None, y_val=None):
        """
        Entrenar modelo XGBoost.
        """
        print(f"Entrenando modelo: {self.model_name}")
        
        # Guardar nombres de características
        self.feature_names = X_train.columns.tolist()
        
        if X_val is not None and y_val is not None:
            # Entrenar con validación temprana
            eval_set = [(X_train, y_train), (X_val, y_val)]
            self.model.fit(
                X_train, y_train,
                eval_set=eval_set,
                verbose=False,
                early_stopping_rounds=10
            )
        else:
            # Entrenar sin validación
            self.model.fit(X_train, y_train)
        
        self.is_fitted = True
        
        # Calcular métricas de entrenamiento
        train_score = self.model.score(X_train, y_train)
        print(f"Entrenamiento completado. Accuracy train: {train_score:.4f}")
        
        # Importancia de características
        importance = self.get_feature_importance()
        print(f"Top 5 características importantes:")
        for i, (feature, score) in enumerate(list(importance.items())[:5]):
            print(f"  {i+1}. {feature}: {score:.4f}")
        
        # Validación si se proporcionan datos
        if X_val is not None and y_val is not None:
            val_score = self.model.score(X_val, y_val)
            print(f"Accuracy validacion: {val_score:.4f}")
            
            # Métricas completas de validación
            val_metrics = self.evaluate(X_val, y_val)
            print(f"Métricas de validación:")
            for metric, value in val_metrics.items():
                print(f"  • {metric}: {value:.4f}")
        
        return self


class ModelComparison:
    """
    Clase para comparar múltiples modelos de scoring.
    """
    
    def __init__(self):
        self.models = {}
        self.results = {}
        
    def add_model(self, name: str, model: BaselineScoringModel):
        """
        Añadir un modelo a la comparación.
        
        Args:
            name: Nombre del modelo
            model: Instancia del modelo
        """
        self.models[name] = model
    
    def train_all(self, X_train, y_train, X_val=None, y_val=None):
        """
        Entrenar todos los modelos.
        
        Args:
            X_train, y_train: Datos de entrenamiento
            X_val, y_val: Datos de validación (opcional)
        """
        print(f"Entrenando {len(self.models)} modelos...")
        
        for name, model in self.models.items():
            print(f"\n{'='*50}")
            model.train(X_train, y_train, X_val, y_val)
            self.results[name] = model.evaluate(X_val, y_val) if X_val is not None else {}
    
    def compare_models(self, X_test, y_test):
        """
        Comparar todos los modelos en datos de prueba.
        
        Args:
            X_test, y_test: Datos de prueba
            
        Returns:
            pd.DataFrame: Resultados comparativos
        """
        print(f"\nComparando modelos en datos de prueba...")
        
        comparison_results = {}
        
        for name, model in self.models.items():
            metrics = model.evaluate(X_test, y_test)
            comparison_results[name] = metrics
            
            print(f"\n{name.upper()}:")
            for metric, value in metrics.items():
                print(f"  • {metric}: {value:.4f}")
        
        # Crear DataFrame de comparación
        comparison_df = pd.DataFrame(comparison_results).T
        
        print(f"\nMejor modelo por métrica:")
        for metric in comparison_df.columns:
            best_model = comparison_df[metric].idxmax()
            best_score = comparison_df[metric].max()
            print(f"  • {metric}: {best_model} ({best_score:.4f})")
        
        return comparison_df
    
    def plot_comparison(self, comparison_df):
        """
        Visualizar comparación de modelos.
        
        Args:
            comparison_df: DataFrame con resultados comparativos
        """
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        axes = axes.flatten()
        
        metrics = comparison_df.columns
        
        for i, metric in enumerate(metrics):
            if i < len(axes):
                comparison_df[metric].plot(kind='bar', ax=axes[i], color=['skyblue', 'lightcoral', 'lightgreen'])
                axes[i].set_title(f'{metric.upper()}')
                axes[i].set_ylabel('Score')
                axes[i].tick_params(axis='x', rotation=45)
                axes[i].legend()
        
        # Ocultar subplots vacíos
        for i in range(len(metrics), len(axes)):
            axes[i].set_visible(False)
        
        plt.tight_layout()
        plt.savefig('model_comparison.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def get_best_model(self, metric='roc_auc'):
        """
        Obtener el mejor modelo según una métrica específica.
        
        Args:
            metric: Métrica para comparar
            
        Returns:
            tuple: (nombre del mejor modelo, instancia del modelo, score)
        """
        if not self.results:
            raise ValueError("No results available. Run train_all() first.")
        
        best_model_name = max(self.results.keys(), key=lambda k: self.results[k].get(metric, 0))
        best_score = self.results[best_model_name].get(metric, 0)
        best_model = self.models[best_model_name]
        
        return best_model_name, best_model, best_score


def create_baseline_models():
    """
    Crear instancias de modelos baseline.
    
    Returns:
        ModelComparison: Comparador de modelos con modelos baseline
    """
    comparison = ModelComparison()
    
    # Añadir modelos
    comparison.add_model('logistic_regression', LogisticRegressionModel())
    comparison.add_model('random_forest', RandomForestModel())
    comparison.add_model('xgboost', XGBoostModel())
    
    return comparison


# Función principal para prueba
def main():
    """
    Función principal para probar los modelos baseline.
    """
    from pathlib import Path
    from src.data.preprocessing_fixed import ScoringPreprocessor
    
    # Cargar y preprocesar datos
    data_path = Path(__file__).parent.parent.parent / "data" / "raw" / "datos.csv"
    df = pd.read_csv(data_path)
    
    preprocessor = ScoringPreprocessor()
    X_train, X_test, y_train, y_test = preprocessor.prepare_data(df)
    
    # Crear y entrenar modelos
    models = create_baseline_models()
    models.train_all(X_train, y_train, X_test, y_test)
    
    # Comparar modelos
    comparison_results = models.compare_models(X_test, y_test)
    models.plot_comparison(comparison_results)
    
    # Obtener mejor modelo
    best_name, best_model, best_score = models.get_best_model('roc_auc')
    print(f"\nMejor modelo: {best_name} (ROC AUC: {best_score:.4f})")
    
    return models, best_model


if __name__ == "__main__":
    models, best_model = main()
