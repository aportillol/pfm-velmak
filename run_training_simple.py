#!/usr/bin/env python3
"""
Pipeline de Entrenamiento Simplificado para PFM Velmak Scoring
==============================================================

Este script ejecuta el pipeline completo de entrenamiento con correcciones:
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

# Importar módulos del proyecto
from src.data.preprocessing_fixed import ScoringPreprocessor

# Importar modelos directamente
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb

class SimpleTrainingPipeline:
    """
    Pipeline simplificado de entrenamiento para modelos de scoring.
    """
    
    def __init__(self):
        self.preprocessor = None
        self.models = {}
        self.results = {}
        self.best_model_name = None
        self.best_model = None
        self.training_timestamp = datetime.now()
        
    def load_data(self, data_path: str) -> pd.DataFrame:
        """Cargar datos desde archivo CSV."""
        try:
            logger.info(f"Cargando datos desde {data_path}")
            df = pd.read_csv(data_path)
            logger.info(f"Datos cargados: {df.shape}")
            return df
        except Exception as e:
            logger.error(f"Error cargando datos: {str(e)}")
            raise
    
    def preprocess_data(self, df: pd.DataFrame):
        """Preprocesar datos para entrenamiento."""
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
        """Entrenar y comparar modelos baseline."""
        try:
            logger.info("Iniciando entrenamiento de modelos")
            
            # 1. Regresión Logística
            print("Entrenando modelo: logistic_regression")
            self.models['logistic_regression'] = LogisticRegression(
                random_state=42,
                max_iter=1000,
                class_weight='balanced',
                solver='liblinear'
            )
            self.models['logistic_regression'].fit(X_train, y_train)
            
            # 2. Random Forest
            print("Entrenando modelo: random_forest")
            self.models['random_forest'] = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                class_weight='balanced',
                n_jobs=-1
            )
            self.models['random_forest'].fit(X_train, y_train)
            
            # 3. XGBoost (sin early_stopping)
            print("Entrenando modelo: xgboost")
            self.models['xgboost'] = xgb.XGBClassifier(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                random_state=42,
                eval_metric='logloss',
                use_label_encoder=False,
                n_jobs=-1
            )
            self.models['xgboost'].fit(X_train, y_train)
            
            # Evaluar todos los modelos
            self.evaluate_models(X_test, y_test)
            
            # Obtener mejor modelo
            self.find_best_model()
            
            logger.info(f"Mejor modelo: {self.best_model_name}")
            
        except Exception as e:
            logger.error(f"Error en entrenamiento: {str(e)}")
            raise
    
    def evaluate_models(self, X_test, y_test):
        """Evaluar todos los modelos en datos de prueba."""
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
        
        print(f"\nComparando modelos en datos de prueba...")
        
        comparison_results = {}
        
        for name, model in self.models.items():
            # Predicciones
            y_pred = model.predict(X_test)
            y_proba = model.predict_proba(X_test)[:, 1]
            
            # Calcular métricas
            metrics = {
                'accuracy': accuracy_score(y_test, y_pred),
                'precision': precision_score(y_test, y_pred),
                'recall': recall_score(y_test, y_pred),
                'f1_score': f1_score(y_test, y_pred),
                'roc_auc': roc_auc_score(y_test, y_proba)
            }
            
            comparison_results[name] = metrics
            
            print(f"\n{name.upper()}:")
            for metric, value in metrics.items():
                print(f"  • {metric}: {value:.4f}")
        
        # Crear DataFrame de comparación
        self.results = pd.DataFrame(comparison_results).T
        
        print(f"\nMejor modelo por métrica:")
        for metric in self.results.columns:
            best_model = self.results[metric].idxmax()
            best_score = self.results[metric].max()
            print(f"  • {metric}: {best_model} ({best_score:.4f})")
    
    def find_best_model(self):
        """Encontrar el mejor modelo según ROC AUC."""
        if 'roc_auc' not in self.results.columns:
            raise ValueError("No se encontró métrica ROC AUC")
        
        self.best_model_name = self.results['roc_auc'].idxmax()
        self.best_model = self.models[self.best_model_name]
        
        print(f"\nMejor modelo: {self.best_model_name} (ROC AUC: {self.results.loc[self.best_model_name, 'roc_auc']:.4f})")
    
    def generate_reports(self, X_test, y_test):
        """Generar reportes y visualizaciones."""
        try:
            logger.info("Generando reportes y visualizaciones")
            
            # Crear directorio de reportes
            reports_dir = Path("reports")
            reports_dir.mkdir(exist_ok=True)
            
            # 1. Reporte de comparación de modelos
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
            
            # 2. Importancia de características del mejor modelo
            if hasattr(self.best_model, 'feature_importances_'):
                importance_dict = dict(zip(self.preprocessor.feature_names, self.best_model.feature_importances_))
                importance_dict = dict(sorted(importance_dict.items(), key=lambda x: x[1], reverse=True))
                
                plt.figure(figsize=(12, 8))
                top_features = dict(list(importance_dict.items())[:15])
                
                features = list(top_features.keys())
                scores = list(top_features.values())
                
                bars = plt.barh(features, scores)
                plt.xlabel('Importancia')
                plt.title(f'Top 15 Características Importantes - {self.best_model_name}')
                plt.gca().invert_yaxis()
                
                for i, bar in enumerate(bars):
                    width = bar.get_width()
                    plt.text(bar.get_x() + width + 0.01, bar.get_y() + bar.get_height()/2,
                            f'{scores[i]:.3f}', ha='left', va='center')
                
                plt.tight_layout()
                plt.savefig(reports_dir / "feature_importance.png", dpi=300, bbox_inches='tight')
                plt.close()
                
                # Guardar importancia en JSON
                with open(reports_dir / "feature_importance.json", "w") as f:
                    json.dump(importance_dict, f, indent=2)
            
            # 3. Matriz de confusión
            from sklearn.metrics import confusion_matrix
            
            y_pred = self.best_model.predict(X_test)
            cm = confusion_matrix(y_test, y_pred)
            
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
            
            # 4. Curva ROC
            from sklearn.metrics import roc_curve, auc
            
            y_proba = self.best_model.predict_proba(X_test)[:, 1]
            fpr, tpr, thresholds = roc_curve(y_test, y_proba)
            roc_auc = auc(fpr, tpr)
            
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
            
            # 5. Guardar resultados en JSON
            report_data = {
                "training_timestamp": self.training_timestamp.isoformat(),
                "best_model": {
                    "name": self.best_model_name,
                    "metrics": self.results.loc[self.best_model_name].to_dict()
                },
                "all_results": self.results.to_dict(),
                "dataset_info": {
                    "total_records": len(self.results),
                    "models_compared": list(self.results.index),
                    "metrics": list(self.results.columns)
                }
            }
            
            with open(reports_dir / "training_summary.json", "w") as f:
                json.dump(report_data, f, indent=2, default=str)
            
            logger.info("Reportes generados exitosamente")
            
        except Exception as e:
            logger.error(f"Error generando reportes: {str(e)}")
            raise
    
    def save_models(self):
        """Guardar modelos entrenados y preprocesador."""
        try:
            models_dir = Path("models")
            models_dir.mkdir(exist_ok=True)
            
            # Guardar preprocesador
            if self.preprocessor:
                import pickle
                with open(models_dir / "preprocessor.pkl", "wb") as f:
                    pickle.dump(self.preprocessor, f)
                print(f"Preprocesador guardado en {models_dir / 'preprocessor.pkl'}")
            
            # Guardar mejor modelo
            if self.best_model:
                import pickle
                with open(models_dir / f"{self.best_model_name}_model.pkl", "wb") as f:
                    pickle.dump(self.best_model, f)
                print(f"Modelo guardado: {self.best_model_name}_model.pkl")
            
        except Exception as e:
            logger.error(f"Error guardando modelos: {str(e)}")
    
    def run_training_pipeline(self, data_path: str):
        """Ejecutar pipeline completo de entrenamiento."""
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
            self.print_summary()
            
            logger.info("="*60)
            logger.info("PIPELINE DE ENTRENAMIENTO COMPLETADO")
            logger.info("="*60)
            
        except Exception as e:
            logger.error(f"Error en pipeline de entrenamiento: {str(e)}")
            raise
    
    def print_summary(self):
        """Imprimir resumen del entrenamiento."""
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
        print("  • reports/model_comparison.png")
        print("  • reports/feature_importance.png")
        print("  • reports/confusion_matrix.png")
        print("  • reports/roc_curve.png")
        print("  • reports/training_summary.json")
        print("  • models/preprocessor.pkl")
        print(f"  • models/{self.best_model_name}_model.pkl")
        
        print("="*60)

# Función principal
def main():
    """Función principal para ejecutar el pipeline de entrenamiento."""
    # Configurar paths
    data_path = "data/raw/datos.csv"
    
    # Crear pipeline
    pipeline = SimpleTrainingPipeline()
    
    # Ejecutar pipeline
    pipeline.run_training_pipeline(data_path)

if __name__ == "__main__":
    main()
