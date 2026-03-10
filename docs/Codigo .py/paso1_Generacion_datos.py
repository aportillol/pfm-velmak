"""
PFM: SISTEMA DE SCORING CREDITICIO BASADO EN HÁBITOS DIGITALES
Script: Generación de Datos Sintéticos Realistas
"""
import pandas as pd
import numpy as np
import os

def preparar_entorno():
    """Crea la estructura de directorios del proyecto para cualquier usuario, hace que sea portable."""
    for carpeta in ['data', 'models', 'entregables']:
        if not os.path.exists(carpeta): os.makedirs(carpeta)

def simular_poblacion(n=1200):
    """Genera datos de 4 apps con ruido estratégico para realismo académico, ya que no contamos con ingesta de datos reales."""
    np.random.seed(42)
    datos_generados = []
    
    for i in range(n):
        p = np.random.random()
        riesgo = 0 if p < 0.35 else (1 if p < 0.80 else 2)
        
        #Aplicamos ruido en etiquetas para asegurar que el modelo sea creíble
        riesgo_final = np.random.choice([0, 1, 2]) if np.random.random() < 0.15 else riesgo

        prob_base = 0.92 if riesgo == 0 else (0.76 if riesgo == 1 else 0.55)
        def aplicar_ruido(v): return np.clip(v + np.random.normal(0, 0.15), 0, 1)
        datos_generados.append({
            'user_id': f'FIN_{i:04d}',
            'target_riesgo': riesgo_final,
            'edad': int(np.clip(np.random.normal(35, 12), 18, 75)),
            'antiguedad_dias': np.random.randint(15, 1100),
            'punc_glovo': aplicar_ruido(prob_base),
            'gasto_glovo': round(np.random.gamma(2, 40), 2),
            'punc_cabify': aplicar_ruido(prob_base),
            'gasto_cabify': round(np.random.gamma(2, 50), 2),
            'punc_movistar': aplicar_ruido(prob_base + 0.02),
            'gasto_movistar': round(np.random.normal(60, 12), 2),
            'punc_zara': aplicar_ruido(prob_base - 0.05),
            'gasto_zara': round(np.random.gamma(1, 120), 2),
            'nivel_renta': 'A' if riesgo == 0 else ('B' if riesgo == 1 else 'C')
        })
    return pd.DataFrame(datos_generados)

if __name__ == "__main__":
    preparar_entorno()
    simular_poblacion().to_csv('data/raw_data.csv', index=False)
    print("Fase 1: Dataset generado con éxito.")