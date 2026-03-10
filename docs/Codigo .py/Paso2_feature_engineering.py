"""
PFM: SISTEMA DE SCORING CREDITICIO BASADO EN HÁBITOS DIGITALES
Script: Ingeniería de Variables (Feature Engineering)
"""
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler

def procesar():
    """Consolida las 4 apps y guarda el objeto de escalado (standard_scaler.pkl)."""
    data_usuarios = pd.read_csv('data/raw_data.csv')
    
    #Agregación multiapp
    data_usuarios['punc_global'] = data_usuarios[['punc_glovo', 'punc_cabify', 'punc_movistar', 'punc_zara']].mean(axis=1)
    data_usuarios['gasto_total'] = data_usuarios[['gasto_glovo', 'gasto_cabify', 'gasto_movistar', 'gasto_zara']].sum(axis=1)
    data_usuarios = pd.get_dummies(data_usuarios, columns=['nivel_renta'], prefix='inc')
    
    variables = ['edad', 'antiguedad_dias', 'punc_global', 'gasto_total', 'inc_A', 'inc_B', 'inc_C']
    X, y = data_usuarios[variables], data_usuarios['target_riesgo']
    
    #ARTEFACTO 1: Escalador 
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    joblib.dump(scaler, 'models/standard_scaler.pkl')
    pd.DataFrame(X_scaled, columns=variables).to_csv('data/X_processed.csv', index=False)
    y.to_csv('data/y_labels.csv', index=False)
    print("Fase 2: Feature Engineering y Normalización completadas.")

if __name__ == "__main__":
    procesar()