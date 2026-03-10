#!/usr/bin/env python3
"""
📊 Análisis Exploratorio de Datos (EDA) - PFM Velmak Scoring
=====================================================

Este script realiza un análisis exploratorio completo del dataset de scoring crediticio
para identificar patrones, valores nulos, correlaciones y características importantes
para el modelo de scoring.

Autor: PFM Velmak Team
Fecha: Marzo 2026
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Configuración de visualización
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

class ScoringEDA:
    """
    Clase para realizar análisis exploratorio de datos de scoring crediticio.
    """
    
    def __init__(self, data_path):
        """
        Inicializar el análisis EDA.
        
        Args:
            data_path (str): Ruta al archivo CSV de datos
        """
        self.data_path = data_path
        self.df = None
        self.numeric_cols = []
        self.categorical_cols = []
        
    def load_data(self):
        """
        Cargar el dataset desde el archivo CSV.
        """
        print("🔄 Cargando dataset...")
        try:
            self.df = pd.read_csv(self.data_path)
            print(f"✅ Dataset cargado exitosamente: {self.df.shape[0]} filas, {self.df.shape[1]} columnas")
            return True
        except Exception as e:
            print(f"❌ Error al cargar el dataset: {e}")
            return False
    
    def basic_info(self):
        """
        Mostrar información básica del dataset.
        """
        print("\n" + "="*60)
        print("📋 INFORMACIÓN BÁSICA DEL DATASET")
        print("="*60)
        
        print(f"\n📏 Dimensiones: {self.df.shape[0]} filas × {self.df.shape[1]} columnas")
        print(f"📊 Tamaño en memoria: {self.df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        
        print("\n📋 Columnas del dataset:")
        for i, col in enumerate(self.df.columns, 1):
            print(f"  {i:2d}. {col}")
        
        print("\n🔍 Primeras 5 filas:")
        print(self.df.head())
        
        print("\n📈 Información de tipos de datos:")
        print(self.df.info())
        
        # Identificar columnas numéricas y categóricas
        self.numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        self.categorical_cols = self.df.select_dtypes(include=['object']).columns.tolist()
        
        print(f"\n📊 Columnas numéricas ({len(self.numeric_cols)}): {self.numeric_cols}")
        print(f"📝 Columnas categóricas ({len(self.categorical_cols)}): {self.categorical_cols}")
    
    def missing_values_analysis(self):
        """
        Análisis de valores nulos y faltantes.
        """
        print("\n" + "="*60)
        print("🔍 ANÁLISIS DE VALORES NULOS")
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
            print(f"\n⚠️  Se encontraron valores nulos en {len(null_with_values)} columnas:")
            print(null_with_values)
            
            # Visualización de valores nulos
            plt.figure(figsize=(12, 6))
            null_with_values['Porcentaje'].plot(kind='bar', color='coral')
            plt.title('Porcentaje de Valores Nulos por Columna', fontsize=14, fontweight='bold')
            plt.xlabel('Columnas')
            plt.ylabel('Porcentaje de Nulos (%)')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig('missing_values_analysis.png', dpi=300, bbox_inches='tight')
            plt.show()
        else:
            print("\n✅ No se encontraron valores nulos en el dataset")
        
        return null_with_values
    
    def descriptive_statistics(self):
        """
        Estadísticas descriptivas de las variables numéricas.
        """
        print("\n" + "="*60)
        print("📈 ESTADÍSTICAS DESCRIPTIVAS")
        print("="*60)
        
        # Estadísticas para variables numéricas
        print("\n📊 Estadísticas de Variables Numéricas:")
        print(self.df[self.numeric_cols].describe().round(2))
        
        # Estadísticas para variables categóricas
        if self.categorical_cols:
            print("\n📝 Estadísticas de Variables Categóricas:")
            for col in self.categorical_cols:
                print(f"\n{col}:")
                print(f"  Valores únicos: {self.df[col].nunique()}")
                print(f"  Moda: {self.df[col].mode().iloc[0]}")
                print(f"  Frecuencia:\n{self.df[col].value_counts()}")
    
    def distribution_analysis(self):
        """
        Análisis de distribuciones de variables numéricas.
        """
        print("\n" + "="*60)
        print("📊 ANÁLISIS DE DISTRIBUCIONES")
        print("="*60)
        
        # Configurar subplots
        n_cols = 3
        n_rows = (len(self.numeric_cols) + n_cols - 1) // n_cols
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5*n_rows))
        axes = axes.flatten()
        
        for i, col in enumerate(self.numeric_cols):
            if i < len(axes):
                # Histograma
                axes[i].hist(self.df[col], bins=30, alpha=0.7, color='skyblue', edgecolor='black')
                axes[i].set_title(f'Distribución de {col}')
                axes[i].set_xlabel(col)
                axes[i].set_ylabel('Frecuencia')
                
                # Añadir línea de media
                mean_val = self.df[col].mean()
                axes[i].axvline(mean_val, color='red', linestyle='--', linewidth=2, label=f'Media: {mean_val:.2f}')
                axes[i].legend()
        
        # Ocultar subplots vacíos
        for i in range(len(self.numeric_cols), len(axes)):
            axes[i].set_visible(False)
        
        plt.tight_layout()
        plt.savefig('distributions_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # Test de normalidad para variables clave
        print("\n🔬 Test de Normalidad (Shapiro-Wilk) para variables clave:")
        key_vars = ['edad', 'ingresos_mensuales', 'deuda_existente', 'score_bureau']
        
        for var in key_vars:
            if var in self.numeric_cols:
                stat, p_value = stats.shapiro(self.df[var].sample(min(5000, len(self.df[var]))))
                print(f"  {var}:")
                print(f"    Estadístico: {stat:.4f}")
                print(f"    p-value: {p_value:.4f}")
                print(f"    Normal: {'✅' if p_value > 0.05 else '❌'}")
    
    def correlation_analysis(self):
        """
        Análisis de correlaciones entre variables numéricas.
        """
        print("\n" + "="*60)
        print("🔗 ANÁLISIS DE CORRELACIONES")
        print("="*60)
        
        # Matriz de correlación
        correlation_matrix = self.df[self.numeric_cols].corr()
        
        print("\n📊 Matriz de Correlación:")
        print(correlation_matrix.round(3))
        
        # Mapa de calor de correlaciones
        plt.figure(figsize=(12, 10))
        mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
        sns.heatmap(correlation_matrix, mask=mask, annot=True, cmap='coolwarm', center=0,
                    square=True, linewidths=0.5, cbar_kws={"shrink": .8})
        plt.title('Mapa de Calor de Correlaciones', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig('correlation_heatmap.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # Correlaciones con la variable objetivo (aprobado)
        if 'aprobado' in self.numeric_cols:
            target_correlations = correlation_matrix['aprobado'].sort_values(ascending=False)
            print(f"\n🎯 Correlaciones con Variable Objetivo (aprobado):")
            print(target_correlations.round(3))
            
            # Visualizar correlaciones con objetivo
            plt.figure(figsize=(10, 8))
            target_correlations.drop('aprobado').plot(kind='bar')
            plt.title('Correlación de Variables con Aprobación', fontsize=14, fontweight='bold')
            plt.xlabel('Variables')
            plt.ylabel('Correlación con Aprobación')
            plt.xticks(rotation=45)
            plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
            plt.tight_layout()
            plt.savefig('target_correlations.png', dpi=300, bbox_inches='tight')
            plt.show()
    
    def categorical_analysis(self):
        """
        Análisis de variables categóricas.
        """
        if not self.categorical_cols:
            print("\n⚠️ No hay variables categóricas para analizar")
            return
        
        print("\n" + "="*60)
        print("📝 ANÁLISIS DE VARIABLES CATEGÓRICAS")
        print("="*60)
        
        # Configurar subplots
        n_cols = 2
        n_rows = (len(self.categorical_cols) + n_cols - 1) // n_cols
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5*n_rows))
        axes = axes.flatten()
        
        for i, col in enumerate(self.categorical_cols):
            if i < len(axes):
                # Gráfico de barras
                value_counts = self.df[col].value_counts()
                axes[i].bar(value_counts.index, value_counts.values, color='lightblue', edgecolor='black')
                axes[i].set_title(f'Distribución de {col}')
                axes[i].set_xlabel(col)
                axes[i].set_ylabel('Frecuencia')
                axes[i].tick_params(axis='x', rotation=45)
                
                # Añadir etiquetas de valores
                for j, (idx, val) in enumerate(value_counts.items()):
                    axes[i].text(j, val + 0.5, str(val), ha='center', va='bottom')
        
        # Ocultar subplots vacíos
        for i in range(len(self.categorical_cols), len(axes)):
            axes[i].set_visible(False)
        
        plt.tight_layout()
        plt.savefig('categorical_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # Análisis de variables categóricas vs aprobación
        if 'aprobado' in self.df.columns:
            print("\n🎯 Análisis de Variables Categóricas vs Aprobación:")
            
            for col in self.categorical_cols:
                if col != 'aprobado':
                    crosstab = pd.crosstab(self.df[col], self.df['aprobado'], normalize='index') * 100
                    print(f"\n{col}:")
                    print(crosstab.round(2))
                    
                    # Visualizar
                    plt.figure(figsize=(8, 6))
                    crosstab.plot(kind='bar', stacked=True)
                    plt.title(f'Tasa de Aprobación por {col}', fontsize=12, fontweight='bold')
                    plt.xlabel(col)
                    plt.ylabel('Porcentaje')
                    plt.xticks(rotation=45)
                    plt.legend(title='Aprobado', labels=['No', 'Sí'])
                    plt.tight_layout()
                    plt.savefig(f'approval_by_{col}.png', dpi=300, bbox_inches='tight')
                    plt.show()
    
    def outlier_detection(self):
        """
        Detección de outliers en variables numéricas.
        """
        print("\n" + "="*60)
        print("🚨 DETECCIÓN DE OUTLIERS")
        print("="*60)
        
        # Método IQR para detección de outliers
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
        
        # Mostrar información de outliers
        outliers_df = pd.DataFrame(outliers_info).T
        print("\n📊 Resumen de Outliers (Método IQR):")
        print(outliers_df.round(2))
        
        # Visualizar outliers con boxplots
        n_cols = 3
        n_rows = (len(self.numeric_cols) + n_cols - 1) // n_cols
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5*n_rows))
        axes = axes.flatten()
        
        for i, col in enumerate(self.numeric_cols):
            if col != 'id' and i < len(axes):
                # Boxplot
                axes[i].boxplot(self.df[col])
                axes[i].set_title(f'Boxplot de {col}')
                axes[i].set_ylabel(col)
        
        # Ocultar subplots vacíos
        for i in range(len(self.numeric_cols), len(axes)):
            axes[i].set_visible(False)
        
        plt.tight_layout()
        plt.savefig('outliers_boxplots.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def feature_importance_analysis(self):
        """
        Análisis preliminar de importancia de características.
        """
        print("\n" + "="*60)
        print("🎯 ANÁLISIS DE IMPORTANCIA DE CARACTERÍSTICAS")
        print("="*60)
        
        if 'aprobado' not in self.df.columns:
            print("⚠️ No se encuentra la variable objetivo 'aprobado'")
            return
        
        # Preparar datos para análisis
        X = self.df.drop(['id', 'aprobado'], axis=1, errors='ignore')
        y = self.df['aprobado']
        
        # Convertir variables categóricas a numéricas
        X_encoded = pd.get_dummies(X, drop_first=True)
        
        # Calcular correlaciones con la variable objetivo
        correlations = X_encoded.corrwith(y).abs().sort_values(ascending=False)
        
        print("\n📊 Importancia de Características (Basado en Correlación):")
        print(correlations.round(3))
        
        # Visualizar importancia
        plt.figure(figsize=(12, 8))
        correlations.head(15).plot(kind='bar')
        plt.title('Top 15 Características por Correlación con Aprobación', fontsize=14, fontweight='bold')
        plt.xlabel('Características')
        plt.ylabel('Correlación Absoluta')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('feature_importance.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return correlations
    
    def generate_summary_report(self):
        """
        Generar un resumen ejecutivo del análisis EDA.
        """
        print("\n" + "="*60)
        print("📋 RESUMEN EJECUTIVO DEL ANÁLISIS EDA")
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
        
        print(f"\n📊 Resumen del Dataset:")
        print(f"  • Registros totales: {summary['total_records']:,}")
        print(f"  • Características totales: {summary['total_features']}")
        print(f"  • Variables numéricas: {summary['numeric_features']}")
        print(f"  • Variables categóricas: {summary['categorical_features']}")
        print(f"  • Valores nulos: {summary['missing_values']}")
        
        if summary['approval_rate'] is not None:
            print(f"  • Tasa de aprobación: {summary['approval_rate']:.2%}")
        
        # Conclusiones clave
        print(f"\n🔍 Conclusiones Clave:")
        
        # Calcular correlaciones más importantes
        if 'aprobado' in self.df.columns:
            correlations = self.df[self.numeric_cols].corr()['aprobado'].abs().sort_values(ascending=False)
            top_features = correlations.head(3)
            
            print(f"  • Características más influyentes en aprobación:")
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
        """
        Ejecutar el análisis exploratorio completo.
        """
        print("🚀 INICIANDO ANÁLISIS EXPLORATORIO DE DATOS COMPLETO")
        print("="*60)
        
        # Cargar datos
        if not self.load_data():
            return
        
        # Ejecutar todos los análisis
        self.basic_info()
        self.missing_values_analysis()
        self.descriptive_statistics()
        self.distribution_analysis()
        self.correlation_analysis()
        self.categorical_analysis()
        self.outlier_detection()
        self.feature_importance_analysis()
        self.generate_summary_report()
        
        print("\n" + "="*60)
        print("✅ ANÁLISIS EDA COMPLETADO EXITOSAMENTE")
        print("="*60)
        print("📊 Gráficos guardados en el directorio actual:")
        print("  • missing_values_analysis.png")
        print("  • distributions_analysis.png")
        print("  • correlation_heatmap.png")
        print("  • target_correlations.png")
        print("  • categorical_analysis.png")
        print("  • approval_by_*.png")
        print("  • outliers_boxplots.png")
        print("  • feature_importance.png")
        print("\n🎯 Listo para continuar con el desarrollo del modelo de scoring!")

# Función principal
def main():
    """
    Función principal para ejecutar el análisis EDA.
    """
    # Ruta al dataset
    data_path = '../data/raw/datos.csv'
    
    # Crear instancia del analizador
    eda_analyzer = ScoringEDA(data_path)
    
    # Ejecutar análisis completo
    eda_analyzer.run_complete_eda()

if __name__ == "__main__":
    main()
