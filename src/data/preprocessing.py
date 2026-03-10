#!/usr/bin/env python3
"""
Pipeline de Preprocesamiento para PFM Velmak Scoring
=====================================================

Este módulo contiene funciones para preprocesar los datos de scoring crediticio
incluyendo limpieza, feature engineering y preparación para modelos ML.

Autor: PFM Velmak Team
Fecha: Marzo 2026
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

class ScoringPreprocessor:
    """
    Clase para preprocesar datos de scoring crediticio.
    """
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.feature_names = []
        self.categorical_mappings = {}
        
    def create_features(self, df):
        """
        Crear nuevas características basadas en el análisis EDA.
        
        Args:
            df (pd.DataFrame): DataFrame original
            
        Returns:
            pd.DataFrame: DataFrame con nuevas características
        """
        df_processed = df.copy()
        
        # 1. Ratio deuda/ingresos (muy importante para scoring)
        df_processed['ratio_deuda_ingresos'] = df_processed['deuda_existente'] / df_processed['ingresos_mensuales']
        
        # 2. Ratio consulta/edad (indicador de comportamiento)
        df_processed['ratio_consulta_edad'] = df_processed['consultas_recientes'] / df_processed['edad']
        
        # 3. Ratio tarjetas/ingresos (nivel de endeudamiento)
        df_processed['ratio_tarjetas_ingresos'] = df_processed['tarjetas_credito'] / df_processed['ingresos_mensuales']
        
        # 4. Score de estabilidad laboral
        df_processed['score_estabilidad_laboral'] = np.where(
            df_processed['tipo_contrato'] == 'permanente',
            df_processed['antiguedad_laboral'] * 2,
            np.where(
                df_processed['tipo_contrato'] == 'autonomo',
                df_processed['antiguedad_laboral'] * 1.5,
                df_processed['antiguedad_laboral'] * 0.5
            )
        )
        
        # 5. Score de capacidad financiera
        df_processed['score_capacidad_financiera'] = (
            (df_processed['ingresos_mensuales'] - df_processed['deuda_existente']) / 
            df_processed['ingresos_mensuales']
        )
        
        # 6. Score de riesgo combinado
        df_processed['score_riesgo_combinado'] = (
            df_processed['score_bureau'] * 0.4 +
            (1 - df_processed['ratio_deuda_ingresos']) * 100 * 0.3 +
            (1 - df_processed['impagos_previos'] / 2) * 100 * 0.3
        )
        
        # 7. Categorías de edad
        df_processed['categoria_edad'] = pd.cut(
            df_processed['edad'],
            bins=[0, 25, 35, 45, 60, 100],
            labels=['joven', 'adulto_joven', 'adulto', 'adulto_mayor', 'senior']
        )
        
        # 8. Categorías de ingresos
        df_processed['categoria_ingresos'] = pd.cut(
            df_processed['ingresos_mensuales'],
            bins=[0, 2000, 3500, 5000, 10000],
            labels=['bajos', 'medios', 'altos', 'muy_altos']
        )
        
        # 9. Score de comportamiento financiero
        df_processed['score_comportamiento'] = (
            (df_processed['tiene_propiedad'] * 20) +
            (df_processed['antiguedad_laboral'] * 2) +
            (2 - df_processed['impagos_previos']) * 10 +
            (2 - df_processed['consultas_recientes']) * 5
        )
        
        # 10. Índice de salud financiera
        df_processed['indice_salud_financiera'] = (
            df_processed['score_bureau'] / 100 +
            df_processed['score_capacidad_financiera'] +
            df_processed['score_comportamiento'] / 100
        ) / 3
        
        return df_processed
    
    def encode_categorical(self, df):
        """
        Codificar variables categóricas.
        
        Args:
            df (pd.DataFrame): DataFrame con características
            
        Returns:
            pd.DataFrame: DataFrame con variables codificadas
        """
        df_encoded = df.copy()
        
        # Codificar tipo_contrato
        if 'tipo_contrato' in df_encoded.columns:
            # Guardar mapeo para referencia futura
            contract_mapping = {
                'permanente': 3,
                'autonomo': 2,
                'temporal': 1
            }
            self.categorical_mappings['tipo_contrato'] = contract_mapping
            df_encoded['tipo_contrato_encoded'] = df_encoded['tipo_contrato'].map(contract_mapping)
        
        # Codificar categoria_edad
        if 'categoria_edad' in df_encoded.columns:
            age_mapping = {
                'joven': 1,
                'adulto_joven': 2,
                'adulto': 3,
                'adulto_mayor': 4,
                'senior': 5
            }
            self.categorical_mappings['categoria_edad'] = age_mapping
            df_encoded['categoria_edad_encoded'] = df_encoded['categoria_edad'].map(age_mapping)
        
        # Codificar categoria_ingresos
        if 'categoria_ingresos' in df_encoded.columns:
            income_mapping = {
                'bajos': 1,
                'medios': 2,
                'altos': 3,
                'muy_altos': 4
            }
            self.categorical_mappings['categoria_ingresos'] = income_mapping
            df_encoded['categoria_ingresos_encoded'] = df_encoded['categoria_ingresos'].map(income_mapping)
        
        return df_encoded
    
    def select_features(self, df):
        """
        Seleccionar características más importantes basadas en el EDA.
        
        Args:
            df (pd.DataFrame): DataFrame con todas las características
            
        Returns:
            pd.DataFrame: DataFrame con características seleccionadas
        """
        # Características base del EDA (más importantes)
        base_features = [
            'edad', 'ingresos_mensuales', 'deuda_existente', 'antiguedad_laboral',
            'tiene_propiedad', 'tarjetas_credito', 'consultas_recientes',
            'impagos_previos', 'score_bureau'
        ]
        
        # Características engineered
        engineered_features = [
            'ratio_deuda_ingresos', 'ratio_consulta_edad', 'ratio_tarjetas_ingresos',
            'score_estabilidad_laboral', 'score_capacidad_financiera',
            'score_riesgo_combinado', 'score_comportamiento',
            'indice_salud_financiera'
        ]
        
        # Características categóricas codificadas
        categorical_features = [
            'tipo_contrato_encoded', 'categoria_edad_encoded', 'categoria_ingresos_encoded'
        ]
        
        # Combinar todas las características
        all_features = base_features + engineered_features + categorical_features
        
        # Filtrar solo las que existen en el DataFrame
        selected_features = [col for col in all_features if col in df.columns]
        
        self.feature_names = selected_features
        
        return df[selected_features]
    
    def scale_features(self, X_train, X_test=None):
        """
        Escalar características numéricas.
        
        Args:
            X_train (pd.DataFrame): Datos de entrenamiento
            X_test (pd.DataFrame): Datos de prueba (opcional)
            
        Returns:
            tuple: Datos escalados
        """
        # Identificar columnas numéricas (no codificadas)
        numeric_cols = X_train.select_dtypes(include=[np.number]).columns.tolist()
        
        # Escalar datos de entrenamiento
        X_train_scaled = X_train.copy()
        X_train_scaled[numeric_cols] = self.scaler.fit_transform(X_train[numeric_cols])
        
        # Escalar datos de prueba si se proporcionan
        X_test_scaled = None
        if X_test is not None:
            X_test_scaled = X_test.copy()
            X_test_scaled[numeric_cols] = self.scaler.transform(X_test[numeric_cols])
        
        return X_train_scaled, X_test_scaled
    
    def prepare_data(self, df, target_col='aprobado', test_size=0.2, random_state=42):
        """
        Pipeline completo de preprocesamiento.
        
        Args:
            df (pd.DataFrame): DataFrame original
            target_col (str): Nombre de la columna objetivo
            test_size (float): Proporción para datos de prueba
            random_state (int): Semilla aleatoria
            
        Returns:
            tuple: (X_train, X_test, y_train, y_test)
        """
        print("Iniciando pipeline de preprocesamiento...")
        
        # 1. Crear nuevas características
        df_features = self.create_features(df)
        print(f"✅ Features creadas: {df_features.shape[1]} columnas")
        
        # 2. Codificar variables categóricas
        df_encoded = self.encode_categorical(df_features)
        print(f"✅ Variables categóricas codificadas")
        
        # 3. Seleccionar características
        df_selected = self.select_features(df_encoded)
        print(f"✅ Características seleccionadas: {len(self.feature_names)}")
        
        # 4. Separar features y target
        X = df_selected
        y = df[target_col]
        
        # 5. Dividir en train/test
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        # 6. Escalar características
        X_train_scaled, X_test_scaled = self.scale_features(X_train, X_test)
        print(f"✅ Características escaladas")
        
        # 7. Mostrar información del preprocesamiento
        print(f"\n📊 Resumen del preprocesamiento:")
        print(f"  • Datos de entrenamiento: {X_train_scaled.shape}")
        print(f"  • Datos de prueba: {X_test_scaled.shape}")
        print(f"  • Características finales: {len(self.feature_names)}")
        print(f"  • Balance de clases (train): {y_train.value_counts().to_dict()}")
        print(f"  • Balance de clases (test): {y_test.value_counts().to_dict()}")
        
        return X_train_scaled, X_test_scaled, y_train, y_test
    
    def get_feature_importance_eda(self):
        """
        Obtener importancia de características basada en el EDA.
        
        Returns:
            dict: Diccionario con importancia de características
        """
        importance_scores = {
            'impagos_previos': 0.920,
            'consultas_recientes': 0.880,
            'score_bureau': 0.866,
            'tarjetas_credito': 0.855,
            'edad': 0.772,
            'ingresos_mensuales': 0.756,
            'deuda_existente': 0.665,
            'antiguedad_laboral': 0.597,
            'tiene_propiedad': 0.526,
            'ratio_deuda_ingresos': 0.900,  # Estimado
            'ratio_consulta_edad': 0.850,  # Estimado
            'score_riesgo_combinado': 0.950,  # Estimado
            'indice_salud_financiera': 0.980  # Estimado
        }
        
        # Filtrar solo las características seleccionadas
        filtered_importance = {
            k: v for k, v in importance_scores.items() 
            if k in self.feature_names
        }
        
        return filtered_importance
    
    def transform_new_data(self, df):
        """
        Transformar nuevos datos usando el pipeline aprendido.
        
        Args:
            df (pd.DataFrame): Nuevos datos a transformar
            
        Returns:
            pd.DataFrame: Datos transformados listos para predicción
        """
        # Aplicar mismo pipeline que en entrenamiento
        df_features = self.create_features(df)
        df_encoded = self.encode_categorical(df_features)
        df_selected = self.select_features(df_encoded)
        
        # Escalar usando el scaler ya entrenado
        numeric_cols = df_selected.select_dtypes(include=[np.number]).columns.tolist()
        df_scaled = df_selected.copy()
        df_scaled[numeric_cols] = self.scaler.transform(df_selected[numeric_cols])
        
        return df_scaled
    
    def save_preprocessor(self, filepath):
        """
        Guardar el preprocesador para uso futuro.
        
        Args:
            filepath (str): Ruta para guardar el objeto
        """
        import pickle
        with open(filepath, 'wb') as f:
            pickle.dump(self, f)
        print(f"✅ Preprocesador guardado en {filepath}")
    
    def load_preprocessor(self, filepath):
        """
        Cargar preprocesador guardado.
        
        Args:
            filepath (str): Ruta del archivo guardado
        """
        import pickle
        with open(filepath, 'rb') as f:
            preprocessor = pickle.load(f)
        print(f"✅ Preprocesador cargado desde {filepath}")
        return preprocessor

# Funciones de utilidad
def validate_preprocessing(X_train, X_test, y_train, y_test):
    """
    Validar el resultado del preprocesamiento.
    
    Args:
        X_train, X_test, y_train, y_test: Datos procesados
    """
    print("\n🔍 Validación del preprocesamiento:")
    
    # Verificar que no haya valores nulos
    null_train = X_train.isnull().sum().sum()
    null_test = X_test.isnull().sum().sum()
    
    print(f"  • Valores nulos (train): {null_train}")
    print(f"  • Valores nulos (test): {null_test}")
    
    # Verificar dimensionalidades
    print(f"  • Dimensiones train: {X_train.shape}")
    print(f"  • Dimensiones test: {X_test.shape}")
    
    # Verificar tipos de datos
    numeric_cols_train = X_train.select_dtypes(include=[np.number]).columns.tolist()
    numeric_cols_test = X_test.select_dtypes(include=[np.number]).columns.tolist()
    
    print(f"  • Columnas numéricas (train): {len(numeric_cols_train)}")
    print(f"  • Columnas numéricas (test): {len(numeric_cols_test)}")
    
    # Verificar balance de clases
    balance_train = y_train.value_counts(normalize=True)
    balance_test = y_test.value_counts(normalize=True)
    
    print(f"  • Balance clases (train): {dict(balance_train)}")
    print(f"  • Balance clases (test): {dict(balance_test)}")
    
    # Validación final
    issues = []
    if null_train > 0 or null_test > 0:
        issues.append("Valores nulos detectados")
    if X_train.shape[1] != X_test.shape[1]:
        issues.append("Dimensiones inconsistentes")
    if len(numeric_cols_train) != len(numeric_cols_test):
        issues.append("Tipos de datos inconsistentes")
    
    if issues:
        print(f"  ⚠️ Problemas detectados: {', '.join(issues)}")
        return False
    else:
        print("  ✅ Validación exitosa")
        return True

if __name__ == "__main__":
    # Ejemplo de uso
    from pathlib import Path
    
    # Cargar datos
    data_path = Path(__file__).parent.parent.parent / "data" / "raw" / "datos.csv"
    df = pd.read_csv(data_path)
    
    # Crear preprocesador
    preprocessor = ScoringPreprocessor()
    
    # Preparar datos
    X_train, X_test, y_train, y_test = preprocessor.prepare_data(df)
    
    # Validar
    validate_preprocessing(X_train, X_test, y_train, y_test)
    
    # Guardar preprocesador
    preprocessor.save_preprocessor("preprocessor.pkl")
