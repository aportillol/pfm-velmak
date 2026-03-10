"""
PFM: SISTEMA DE SCORING CREDITICIO BASADO EN HÁBITOS DIGITALES
Script: API REST de Producción
"""
from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field
import joblib
import pandas as pd
import numpy as np

app = FastAPI(
    title="Plataforma de Scoring Crediticio Alternativo",
    description="API para la evaluación de riesgo basada en comportamiento digital. Proyecto Fin de Máster.",
    version="3.0.0",
    contact={"name": "VGNP - Especialista en Datos", "email": "victor.gabriel.np@gmail.com"}
)

#Configuración de seguridad
header_seguridad = APIKeyHeader(name="X-Auth-Token", auto_error=False)
CLAVES_AUTORIZADAS = {"vgnp_pfm_secret": "vgnp_admin_user"}

def validar_token(api_key: str = Security(header_seguridad)):
    if api_key not in CLAVES_AUTORIZADAS:
        raise HTTPException(status_code=403, detail="No autorizado")
    return CLAVES_AUTORIZADAS[api_key]

class InputUsuario(BaseModel):
    #Definimos el esquema
    uid: str = Field(..., example="CLIENTE_PFM_01")
    edad: int = Field(35, ge=18, example=35)
    antiguedad_dias: int = Field(500, example=500)
    punc_glovo: float 
    gasto_glovo: float 
    punc_cabify: float 
    gasto_cabify: float 
    punc_movistar: float 
    gasto_movistar: float 
    punc_zara: float 
    gasto_zara: float 
    inc_A: int 
    inc_B: int 
    inc_C: int 

#Carga de artefactos
try:
    modelo = joblib.load('models/scoring_model.pkl')
    scaler = joblib.load('models/standard_scaler.pkl')
except:
    modelo, scaler = None, None

@app.post("/v1/predict", tags=["Scoring Real-Time"])
def predecir(datos: InputUsuario, token=Depends(validar_token)):
    if not modelo or not scaler: 
        raise HTTPException(status_code=503, detail="Modelo o Escalador no cargados")
    
    try:
        #Lógica de agregación multiapp
        punc_global = (datos.punc_glovo + datos.punc_cabify + datos.punc_movistar + datos.punc_zara) / 4
        gasto_total = datos.gasto_glovo + datos.gasto_cabify + datos.gasto_movistar + datos.gasto_zara
        
        #Mapeo de columnas para el modelo
        columnas = ['edad', 'antiguedad_dias', 'punc_global', 'gasto_total', 'inc_A', 'inc_B', 'inc_C']
        input_data = pd.DataFrame([[
            datos.edad, datos.antiguedad_dias, punc_global, gasto_total,
            datos.inc_A, datos.inc_B, datos.inc_C
        ]], columns=columnas)
        
        #Inferencia
        X_scaled = scaler.transform(input_data)
        probs = modelo.predict_proba(X_scaled)[0]
        score = int((1 - probs[2]) * 1000)
        
        return {
            "uid": datos.uid,
            "score": score,
            "riesgo": ["Bajo", "Moderado", "Alto"][int(np.argmax(probs))],
            "decision": "APROBADO" if score > 680 else "RECHAZADO"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    print("Servidor activo, cargado en: http://localhost:8000/docs")
    uvicorn.run(app, host="127.0.0.1", port=8000)