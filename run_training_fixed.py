#!/usr/bin/env python3
"""
Pipeline de Entrenamiento para PFM Velmak Scoring
==================================================

Este script ejecuta el pipeline completo de entrenamiento:
1. Carga y preprocesa datos
2. Entrena modelos baseline
3. Compara rendimiento
4. Guarda el mejor modelo
5. Genera reportes

Autor: PFM Velmak Team
Fecha: Marzo 2026
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
import json
from datetime import datetime
import logging

# Configuración
warnings.filterwarnings('ignore')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Importar módulos del proyecto corregidos
from src.data.preprocessing_fixed import ScoringPreprocessor
from src.models.baseline_models import create_baseline_models, ModelComparison

class TrainingPipeline:
    """
    Pipeline completo de entrenamiento para modelos de scoring.
    """
    
    def __init__(self):
        self.preprocessor = None
        self.models = None
        self.best_model = None
        self.best_model_name = None
        self.results = None
        self.training_timestamp = datetime.now()
        
    def load_data(self, data_path: str) -> pd.DataFrame:
        """
        Cargar datos desde archivo CSV.
        
        Args:
            data_path: Ruta al archivo CSV
            
        Returns:
            pd.DataFrame: DataFrame cargado
        """
        try:
            logger.info(f"Cargando datos desde {data_path}")
            df = pd.read_csv(data_path)
            logger.info(f"Datos cargados: {df.shape}")
            return df
        except Exception as e:
            logger.error(f"Error cargando datos: {str(e)}")
            raise
    
    def preprocess_data(self, df: pd.DataFrame):
        """
        Preprocesar datos para entrenamiento.
        
        Args:
            df: DataFrame original
            
        Returns:
            tuple: (X_train, X_test, y_train, y_test)
        """
        try:
            logger.info("Iniciando preprocesamiento de datos")
            
            self.preprocessor = ScoringPreprocessor()
            X_train, X_test, y_train, y_test = self.preprocessor.prepare_data(df)
            
            logger.info(f"Preprocesamiento completado:")
            logger.info(f"  • Train: {X_train.shape}")
            logger.info(f"  • Test: {X_test.shape}")
            logger.info(f"  • Features: {len(self.preprocessor.feature_names)}")
            
            return X_train, X_test, y_train, y_test
            
        except Exception as e:
            logger.error(f"Error en preprocesamiento: {str(e)}")
            raise
    
    def train_models(self, X_train, X_test, y_train, y_test):
        """
        Entrenar y comparar modelos baseline.
        
        Args:
            X_train, X_test, y_train, y_test: Datos de entrenamiento y prueba
            
        Returns:
            ModelComparison: Objeto con modelos entrenados y resultados
        """
        try:
            logger.info("Iniciando entrenamiento de modelos")
            
            # Crear y entrenar modelos
            self.models = create_baseline_models()
            self.models.train_all(X_train, y_train, X_test, y_test)
            
            # Comparar modelos en test
            self.results = self.models.compare_models(X_test, y_test)
            
            # Obtener mejor modelo
            self.best_model_name, self.best_model, best_score = self.models.get_best_model('roc_auc')
            
            logger.info(f"Mejor modelo: {self.best_model_name} (ROC AUC: {best_score:.4f})")
            
            return self.models
            
        except Exception as e:
            logger.error(f"Error en entrenamiento: {str(e)}")
            raise
    
    def generate_reports(self, X_test, y_test):
        """
        Generar reportes y visualizaciones.
        
        Args:
            X_test, y_test: Datos de prueba
        """
        try:
            logger.info("Generando reportes y visualizaciones")
            
            # 1. Reporte de comparación de modelos
            self.generate_model_comparison_report()
            
            # 2. Visualización de importancia de características
            self.generate_feature_importance_plot()
            
            # 3. Matriz de confusión del mejor modelo
            self.generate_confusion_matrix(X_test, y_test)
            
            # 4. Curva ROC del mejor modelo
            self.generate_roc_curve(X_test, y_test)
            
            # 5. Reporte de características
            self.generate_feature_report()
            
            logger.info("Reportes generados exitosamente")
            
        except Exception as e:
            logger.error(f"Error generando reportes: {str(e)}")
            raise
    
    def generate_model_comparison_report(self):
        """
        Generar reporte de comparación de modelos.
        """
        if self.results is None:
            return
        
        # Crear directorio de reportes
        reports_dir = Path("reports")
        reports_dir.mkdir(exist_ok=True)
        
        # Guardar resultados en JSON
        results_dict = self.results.to_dict()
        
        # Agregar metadatos
        report_data = {
            "training_timestamp": self.training_timestamp.isoformat(),
            "dataset_info": {
                "total_records": len(self.results),
                "models_compared": list(self.results.index),
                "metrics": list(self.results.columns)
            },
            "results": results_dict,
            "best_model": {
                "name": self.best_model_name,
                "metrics": self.results.loc[self.best_model_name].to_dict()
            }
        }
        
        # Guardar reporte JSON
        with open(reports_dir / "model_comparison.json", "w") as f:
            json.dump(report_data, f, indent=2, default=str)
        
        # Crear reporte visual
        plt.figure(figsize=(12, 8))
        self.results.plot(kind='bar')
        plt.title('Comparación de Modelos - Métricas de Evaluación')
        plt.xlabel('Modelos')
        plt.ylabel('Score')
        plt.legend(title='Métricas')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(reports_dir / "model_comparison.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info("Reporte de comparación guardado")
    
    def generate_feature_importance_plot(self):
        """
        Generar visualización de importancia de características.
        """
        if self.best_model is None:
            return
        
        try:
            importance = self.best_model.get_feature_importance()
            
            if not importance:
                return
            
            # Crear directorio de reportes
            reports_dir = Path("reports")
            reports_dir.mkdir(exist_ok=True)
            
            # Visualización
            plt.figure(figsize=(12, 8))
            
            # Top 15 características
            top_features = dict(list(importance.items())[:15])
            
            features = list(top_features.keys())
            scores = list(top_features.values())
            
            bars = plt.barh(features, scores)
            plt.xlabel('Importancia')
            plt.title(f'Top 15 Características Importantes - {self.best_model_name}')
            plt.gca().invert_yaxis()
            
            # Añadir valores en las barras
            for i, bar in enumerate(bars):
                width = bar.get_width()
                plt.text(bar.get_x() + width + 0.01, bar.get_y() + bar.get_height()/2,
                        f'{scores[i]:.3f}', ha='left', va='center')
            
            plt.tight_layout()
            plt.savefig(reports_dir / "feature_importance.png", dpi=300, bbox_inches='tight')
            plt.close()
            
            # Guardar importancia en JSON
            with open(reports_dir / "feature_importance.json", "w") as f:
                json.dump(importance, f, indent=2)
            
            logger.info("Visualización de importancia de características guardada")
            
        except Exception as e:
            logger.error(f"Error generando visualización de importancia: {str(e)}")
    
    def generate_confusion_matrix(self, X_test, y_test):
        """
        Generar matriz de confusión del mejor modelo.
        """
        if self.best_model is None:
            return
        
        try:
            from sklearn.metrics import confusion_matrix
            
            # Crear directorio de reportes
            reports_dir = Path("reports")
            reports_dir.mkdir(exist_ok=True)
            
            # Predicciones
            y_pred = self.best_model.predict(X_test)
            
            # Matriz de confusión
            cm = confusion_matrix(y_test, y_pred)
            
            # Visualización
            plt.figure(figsize=(8, 6))
            sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                       xticklabels=['Rechazado', 'Aprobado'],
                       yticklabels=['Rechazado', 'Aprobado'])
            plt.title(f'Matriz de Confusión - {self.best_model_name}')
            plt.xlabel('Predicción')
            plt.ylabel('Real')
            plt.tight_layout()
            plt.savefig(reports_dir / "confusion_matrix.png", dpi=300, bbox_inches='tight')
            plt.close()
            
            # Guardar matriz en JSON
            cm_dict = {
                "matrix": cm.tolist(),
                "true_negatives": int(cm[0,0]),
                "false_positives": int(cm[0,1]),
                "false_negatives": int(cm[1,0]),
                "true_positives": int(cm[1,1])
            }
            
            with open(reports_dir / "confusion_matrix.json", "w") as f:
                json.dump(cm_dict, f, indent=2)
            
            logger.info("Matriz de confusión guardada")
            
        except Exception as e:
            logger.error(f"Error generando matriz de confusión: {str(e)}")
    
    def generate_roc_curve(self, X_test, y_test):
        """
        Generar curva ROC del mejor modelo.
        """
        if self.best_model is None:
            return
        
        try:
            from sklearn.metrics import roc_curve, auc
            
            # Crear directorio de reportes
            reports_dir = Path("reports")
            reports_dir.mkdir(exist_ok=True)
            
            # Predicciones de probabilidad
            y_proba = self.best_model.predict_proba(X_test)[:, 1]
            
            # Calcular curva ROC
            fpr, tpr, thresholds = roc_curve(y_test, y_proba)
            roc_auc = auc(fpr, tpr)
            
            # Visualización
            plt.figure(figsize=(8, 6))
            plt.plot(fpr, tpr, color='blue', lw=2, 
                    label=f'ROC curve (AUC = {roc_auc:.2f})')
            plt.plot([0, 1], [0, 1], color='red', lw=2, linestyle='--')
            plt.xlim([0.0, 1.0])
            plt.ylim([0.0, 1.05])
            plt.xlabel('False Positive Rate')
            plt.ylabel('True Positive Rate')
            plt.title(f'Curva ROC - {self.best_model_name}')
            plt.legend(loc="lower right")
            plt.grid(True)
            plt.tight_layout()
            plt.savefig(reports_dir / "roc_curve.png", dpi=300, bbox_inches='tight')
            plt.close()
            
            # Guardar datos de curva ROC
            roc_data = {
                "fpr": fpr.tolist(),
                "tpr": tpr.tolist(),
                "thresholds": thresholds.tolist(),
                "auc": roc_auc
            }
            
            with open(reports_dir / "roc_curve.json", "w") as f:
                json.dump(roc_data, f, indent=2)
            
            logger.info(f"Curva ROC guardada (AUC: {roc_auc:.4f})")
            
        except Exception as e:
            logger.error(f"Error generando curva ROC: {str(e)}")
    
    def generate_feature_report(self):
        """
        Generar reporte detallado de características.
        """
        if self.preprocessor is None:
            return
        
        try:
            reports_dir = Path("reports")
            reports_dir.mkdir(exist_ok=True)
            
            feature_report = {
                "total_features": len(self.preprocessor.feature_names),
                "feature_names": self.preprocessor.feature_names,
                "categorical_mappings": self.preprocessor.categorical_mappings,
                "feature_engineering_info": {
                    "ratio_deuda_ingresos": "Deuda existente / Ingresos mensuales",
                    "ratio_consulta_edad": "Consultas recientes / Edad",
                    "ratio_tarjetas_ingresos": "Tarjetas de crédito / Ingresos mensuales",
                    "score_estabilidad_laboral": "Basado en tipo_contrato y antigüedad",
                    "score_capacidad_financiera": "(Ingresos - Deuda) / Ingresos",
                    "score_riesgo_combinado": "Combinación ponderada de factores de riesgo",
                    "indice_salud_financiera": "Promedio de scores financieros"
                }
            }
            
            with open(reports_dir / "feature_report.json", "w") as f:
                json.dump(feature_report, f, indent=2)
            
            logger.info("Reporte de características guardado")
            
        except Exception as e:
            logger.error(f"Error generando reporte de características: {str(e)}")
    
    def save_models(self):
        """
        Guardar modelos entrenados y preprocesador.
        """
        try:
            models_dir = Path("models")
            models_dir.mkdir(exist_ok=True)
            
            # Guardar preprocesador
            if self.preprocessor:
                self.preprocessor.save_preprocessor(models_dir / "preprocessor.pkl")
            
            # Guardar mejor modelo
            if self.best_model:
                # Guardar modelo (implementar método save en la clase del modelo)
                import pickle
                with open(models_dir / f"{self.best_model_name}_model.pkl", "wb") as f:
                    pickle.dump(self.best_model, f)
                
                logger.info(f"Modelo guardado: {self.best_model_name}_model.pkl")
            
        except Exception as e:
            logger.error(f"Error guardando modelos: {str(e)}")
    
    def run_training_pipeline(self, data_path: str):
        """
        Ejecutar pipeline completo de entrenamiento.
        
        Args:
            data_path: Ruta al archivo de datos
        """
        try:
            logger.info("="*60)
            logger.info("INICIANDO PIPELINE DE ENTRENAMIENTO")
            logger.info("="*60)
            
            # 1. Cargar datos
            df = self.load_data(data_path)
            
            # 2. Preprocesar datos
            X_train, X_test, y_train, y_test = self.preprocess_data(df)
            
            # 3. Entrenar modelos
            self.train_models(X_train, X_test, y_train, y_test)
            
            # 4. Generar reportes
            self.generate_reports(X_test, y_test)
            
            # 5. Guardar modelos
            self.save_models()
            
            # 6. Resumen final
            self.generate_training_summary()
            
            logger.info("="*60)
            logger.info("PIPELINE DE ENTRENAMIENTO COMPLETADO")
            logger.info("="*60)
            
        except Exception as e:
            logger.error(f"Error en pipeline de entrenamiento: {str(e)}")
            raise
    
    def generate_training_summary(self):
        """
        Generar resumen del entrenamiento.
        """
        try:
            reports_dir = Path("reports")
            reports_dir.mkdir(exist_ok=True)
            
            summary = {
                "training_timestamp": self.training_timestamp.isoformat(),
                "best_model": {
                    "name": self.best_model_name,
                    "type": type(self.best_model).__name__,
                    "metrics": self.results.loc[self.best_model_name].to_dict() if self.results is not None else {}
                },
                "dataset_info": {
                    "total_records": len(self.results) if self.results is not None else 0,
                    "features": len(self.preprocessor.feature_names) if self.preprocessor else 0,
                    "models_compared": list(self.results.index) if self.results is not None else []
                },
                "files_generated": [
                    "reports/model_comparison.json",
                    "reports/model_comparison.png",
                    "reports/feature_importance.json",
                    "reports/feature_importance.png",
                    "reports/confusion_matrix.json",
                    "reports/confusion_matrix.png",
                    "reports/roc_curve.json",
                    "reports/roc_curve.png",
                    "reports/feature_report.json",
                    "models/preprocessor.pkl",
                    f"models/{self.best_model_name}_model.pkl"
                ]
            }
            
            with open(reports_dir / "training_summary.json", "w") as f:
                json.dump(summary, f, indent=2)
            
            # Imprimir resumen en consola
            print("\n" + "="*60)
            print("RESUMEN DEL ENTRENAMIENTO")
            print("="*60)
            print(f"Timestamp: {self.training_timestamp}")
            print(f"Mejor modelo: {self.best_model_name}")
            if self.results is not None:
                print(f"Métricas del mejor modelo:")
                for metric, value in self.results.loc[self.best_model_name].items():
                    print(f"  • {metric}: {value:.4f}")
            
            print(f"\nArchivos generados:")
            for file_path in summary["files_generated"]:
                print(f"  • {file_path}")
            
            print("="*60)
            
        except Exception as e:
            logger.error(f"Error generando resumen: {str(e)}")

# Función principal
def main():
    """
    Función principal para ejecutar el pipeline de entrenamiento.
    """
    # Configurar paths
    data_path = "data/raw/datos.csv"
    
    # Crear pipeline
    pipeline = TrainingPipeline()
    
    # Ejecutar pipeline
    pipeline.run_training_pipeline(data_path)

if __name__ == "__main__":
    main()
