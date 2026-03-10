#!/usr/bin/env python3
"""
Analisis Exploratorio de Datos (EDA) - PFM Velmak Scoring
Version simplificada sin emojis para evitar problemas de codificacion
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Configuracion de visualizacion
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

class ScoringEDA:
    def __init__(self, data_path):
        self.data_path = data_path
        self.df = None
        self.numeric_cols = []
        self.categorical_cols = []
        
    def load_data(self):
        print("Cargando dataset...")
        try:
            self.df = pd.read_csv(self.data_path)
            print(f"Dataset cargado exitosamente: {self.df.shape[0]} filas, {self.df.shape[1]} columnas")
            return True
        except Exception as e:
            print(f"Error al cargar el dataset: {e}")
            return False
    
    def basic_info(self):
        print("\n" + "="*60)
        print("INFORMACION BASICA DEL DATASET")
        print("="*60)
        
        print(f"\nDimensiones: {self.df.shape[0]} filas × {self.df.shape[1]} columnas")
        print(f"Tamaño en memoria: {self.df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        
        print("\nColumnas del dataset:")
        for i, col in enumerate(self.df.columns, 1):
            print(f"  {i:2d}. {col}")
        
        print("\nPrimeras 5 filas:")
        print(self.df.head())
        
        print("\nInformacion de tipos de datos:")
        self.df.info()
        
        # Identificar columnas numericas y categoricas
        self.numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        self.categorical_cols = self.df.select_dtypes(include=['object']).columns.tolist()
        
        print(f"\nColumnas numericas ({len(self.numeric_cols)}): {self.numeric_cols}")
        print(f"Columnas categoricas ({len(self.categorical_cols)}): {self.categorical_cols}")
    
    def missing_values_analysis(self):
        print("\n" + "="*60)
        print("ANALISIS DE VALORES NULOS")
        print("="*60)
        
        # Contar valores nulos
        null_counts = self.df.isnull().sum()
        null_percentages = (null_counts / len(self.df)) * 100
        
        # Crear DataFrame con resultados
        null_analysis = pd.DataFrame({
            'Valores Nulos': null_counts,
            'Porcentaje': null_percentages.round(2)
        })
        
        # Filtrar solo columnas con valores nulos
        null_with_values = null_analysis[null_analysis['Valores Nulos'] > 0]
        
        if len(null_with_values) > 0:
            print(f"\nSe encontraron valores nulos en {len(null_with_values)} columnas:")
            print(null_with_values)
        else:
            print("\nNo se encontraron valores nulos en el dataset")
        
        return null_with_values
    
    def descriptive_statistics(self):
        print("\n" + "="*60)
        print("ESTADISTICAS DESCRIPTIVAS")
        print("="*60)
        
        # Estadisticas para variables numericas
        print("\nEstadisticas de Variables Numericas:")
        print(self.df[self.numeric_cols].describe().round(2))
        
        # Estadisticas para variables categoricas
        if self.categorical_cols:
            print("\nEstadisticas de Variables Categoricas:")
            for col in self.categorical_cols:
                print(f"\n{col}:")
                print(f"  Valores unicos: {self.df[col].nunique()}")
                print(f"  Moda: {self.df[col].mode().iloc[0]}")
                print(f"  Frecuencia:\n{self.df[col].value_counts()}")
    
    def correlation_analysis(self):
        print("\n" + "="*60)
        print("ANALISIS DE CORRELACIONES")
        print("="*60)
        
        # Matriz de correlacion
        correlation_matrix = self.df[self.numeric_cols].corr()
        
        print("\nMatriz de Correlacion:")
        print(correlation_matrix.round(3))
        
        # Correlaciones con la variable objetivo (aprobado)
        if 'aprobado' in self.numeric_cols:
            target_correlations = correlation_matrix['aprobado'].sort_values(ascending=False)
            print(f"\nCorrelaciones con Variable Objetivo (aprobado):")
            print(target_correlations.round(3))
            
            return target_correlations
        
        return correlation_matrix
    
    def categorical_analysis(self):
        if not self.categorical_cols:
            print("\nNo hay variables categoricas para analizar")
            return
        
        print("\n" + "="*60)
        print("ANALISIS DE VARIABLES CATEGORICAS")
        print("="*60)
        
        # Analisis de variables categoricas vs aprobacion
        if 'aprobado' in self.df.columns:
            print("\nAnalisis de Variables Categoricas vs Aprobacion:")
            
            for col in self.categorical_cols:
                if col != 'aprobado':
                    crosstab = pd.crosstab(self.df[col], self.df['aprobado'], normalize='index') * 100
                    print(f"\n{col}:")
                    print(crosstab.round(2))
    
    def outlier_detection(self):
        print("\n" + "="*60)
        print("DETECCION DE OUTLIERS")
        print("="*60)
        
        # Metodo IQR para deteccion de outliers
        outliers_info = {}
        
        for col in self.numeric_cols:
            if col != 'id':  # Excluir ID
                Q1 = self.df[col].quantile(0.25)
                Q3 = self.df[col].quantile(0.75)
                IQR = Q3 - Q1
                
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                outliers = self.df[(self.df[col] < lower_bound) | (self.df[col] > upper_bound)]
                
                outliers_info[col] = {
                    'count': len(outliers),
                    'percentage': (len(outliers) / len(self.df)) * 100,
                    'lower_bound': lower_bound,
                    'upper_bound': upper_bound
                }
        
        # Mostrar informacion de outliers
        outliers_df = pd.DataFrame(outliers_info).T
        print("\nResumen de Outliers (Metodo IQR):")
        print(outliers_df.round(2))
        
        return outliers_df
    
    def feature_importance_analysis(self):
        print("\n" + "="*60)
        print("ANALISIS DE IMPORTANCIA DE CARACTERISTICAS")
        print("="*60)
        
        if 'aprobado' not in self.df.columns:
            print("No se encuentra la variable objetivo 'aprobado'")
            return
        
        # Preparar datos para analisis
        X = self.df.drop(['id', 'aprobado'], axis=1, errors='ignore')
        y = self.df['aprobado']
        
        # Convertir variables categoricas a numericas
        X_encoded = pd.get_dummies(X, drop_first=True)
        
        # Calcular correlaciones con la variable objetivo
        correlations = X_encoded.corrwith(y).abs().sort_values(ascending=False)
        
        print("\nImportancia de Caracteristicas (Basado en Correlacion):")
        print(correlations.round(3))
        
        return correlations
    
    def generate_summary_report(self):
        print("\n" + "="*60)
        print("RESUMEN EJECUTIVO DEL ANALISIS EDA")
        print("="*60)
        
        summary = {
            'dataset_shape': self.df.shape,
            'total_records': len(self.df),
            'total_features': len(self.df.columns),
            'numeric_features': len(self.numeric_cols),
            'categorical_features': len(self.categorical_cols),
            'missing_values': self.df.isnull().sum().sum(),
            'target_variable': 'aprobado' if 'aprobado' in self.df.columns else None,
            'approval_rate': self.df['aprobado'].mean() if 'aprobado' in self.df.columns else None
        }
        
        print(f"\nResumen del Dataset:")
        print(f"  • Registros totales: {summary['total_records']:,}")
        print(f"  • Caracteristicas totales: {summary['total_features']}")
        print(f"  • Variables numericas: {summary['numeric_features']}")
        print(f"  • Variables categoricas: {summary['categorical_features']}")
        print(f"  • Valores nulos: {summary['missing_values']}")
        
        if summary['approval_rate'] is not None:
            print(f"  • Tasa de aprobacion: {summary['approval_rate']:.2%}")
        
        # Conclusiones clave
        print(f"\nConclusiones Clave:")
        
        # Calcular correlaciones mas importantes
        if 'aprobado' in self.df.columns:
            correlations = self.df[self.numeric_cols].corr()['aprobado'].abs().sort_values(ascending=False)
            top_features = correlations.head(3)
            
            print(f"  • Caracteristicas mas influyentes en aprobacion:")
            for feature, corr in top_features.items():
                if feature != 'aprobado':
                    print(f"    - {feature}: {corr:.3f}")
        
        # Verificar balance de clases
        if 'aprobado' in self.df.columns:
            approval_counts = self.df['aprobado'].value_counts()
            print(f"  • Balance de clases (Aprobado):")
            print(f"    - No aprobados: {approval_counts[0]:,} ({approval_counts[0]/len(self.df)*100:.1f}%)")
            print(f"    - Aprobados: {approval_counts[1]:,} ({approval_counts[1]/len(self.df)*100:.1f}%)")
        
        return summary
    
    def run_complete_eda(self):
        print("INICIANDO ANALISIS EXPLORATORIO DE DATOS COMPLETO")
        print("="*60)
        
        # Cargar datos
        if not self.load_data():
            return
        
        # Ejecutar todos los analisis
        self.basic_info()
        self.missing_values_analysis()
        self.descriptive_statistics()
        self.correlation_analysis()
        self.categorical_analysis()
        self.outlier_detection()
        self.feature_importance_analysis()
        self.generate_summary_report()
        
        print("\n" + "="*60)
        print("ANALISIS EDA COMPLETADO EXITOSAMENTE")
        print("="*60)
        print("Listo para continuar con el desarrollo del modelo de scoring!")

# Funcion principal
def main():
    # Ruta al dataset
    data_path = '../../data/raw/datos.csv'
    
    # Crear instancia del analizador
    eda_analyzer = ScoringEDA(data_path)
    
    # Ejecutar analisis completo
    eda_analyzer.run_complete_eda()

if __name__ == "__main__":
    main()
