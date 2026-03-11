#!/usr/bin/env python3
"""
Demo App para PFM Velmak Scoring
================================

Aplicación de demostración para el sistema de scoring crediticio.

Autor: PFM Velmak Team
Fecha: Marzo 2026
"""

import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="PFM Velmak - Demo de Scoring Crediticio",
    page_icon="🏦",
    layout="wide"
)

# Título principal
st.title("🏦 PFM Velmak - Sistema de Scoring Crediticio con IA Explicable")
st.markdown("---")

# Sidebar para información
st.sidebar.title("📊 Información del Sistema")
st.sidebar.info("""
**PFM Velmak** es un sistema avanzado de scoring crediticio que utiliza:
- 🤖 Machine Learning (XGBoost, Random Forest, Logistic Regression)
- 🧠 IA Explicable (SHAP)
- 📈 Feature Engineering Avanzado
- 🌐 API RESTful
""")

# Tabs principales
tab1, tab2, tab3, tab4 = st.tabs(["📋 Evaluación Individual", "📊 Análisis por Lotes", "🧠 Explicabilidad SHAP", "📈 Dashboard"])

with tab1:
    st.header("📋 Evaluación Individual de Crédito")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📝 Información del Solicitante")
        
        # Formulario de entrada
        with st.form("scoring_form"):
            # Datos personales
            st.write("**👤 Datos Personales**")
            edad = st.slider("Edad", 18, 80, 35)
            ingresos = st.slider("Ingresos Mensuales (€)", 1000, 10000, 3500)
            deuda = st.slider("Deuda Existente (€)", 0, 5000, 500)
            
            # Información laboral
            st.write("**💼 Información Laboral**")
            antiguedad = st.slider("Antigüedad Laboral (años)", 0, 30, 5)
            tipo_contrato = st.selectbox("Tipo de Contrato", ["permanente", "autonomo", "temporal"])
            tiene_propiedad = st.checkbox("Tiene Propiedades")
            
            # Información crediticia
            st.write("**💳 Información Crediticia**")
            tarjetas = st.slider("Número de Tarjetas de Crédito", 0, 10, 2)
            consultas = st.slider("Consultas Recientes", 0, 10, 1)
            impagos = st.slider("Impagos Previos", 0, 5, 0)
            score_bureau = st.slider("Score Bureau", 300, 900, 750)
            
            # Botón de evaluación
            submit_button = st.form_submit_button("🔍 Evaluar Riesgo")
    
    with col2:
        if submit_button:
            # Simulación de evaluación
            with st.spinner("⏳ Evaluando riesgo..."):
                # Calcular score simple
                score = 500
                
                # Factores positivos
                score += (score_bureau - 684) * 0.5
                score += (edad - 34) * 2
                score += (ingresos - 3715) * 0.01
                score += (antiguedad - 6) * 5
                
                if tiene_propiedad:
                    score += 50
                
                if tipo_contrato == "permanente":
                    score += 30
                elif tipo_contrato == "autonomo":
                    score += 20
                
                # Factores negativos
                score -= impagos * 100
                score -= consultas * 30
                score -= tarjetas * 10
                
                # Ratio deuda/ingresos
                debt_ratio = deuda / ingresos
                if debt_ratio > 0.5:
                    score -= 100
                elif debt_ratio > 0.3:
                    score -= 50
                
                score = max(0, min(1000, int(score)))
                
                # Determinar resultado
                if score >= 800:
                    riesgo = "Mínimo"
                    decision = "Aprobado Automático"
                    color = "🟢"
                elif score >= 650:
                    riesgo = "Bajo"
                    decision = "Aprobado Automático"
                    color = "🟢"
                elif score >= 500:
                    riesgo = "Medio"
                    decision = "Revisión Manual"
                    color = "🟡"
                else:
                    riesgo = "Alto"
                    decision = "Rechazado"
                    color = "🔴"
                
                prob_aprobacion = min(max((score - 300) / 700, 0), 1)
            
            # Mostrar resultados
            st.subheader("📊 Resultados de Evaluación")
            
            # Score principal
            st.metric("Score de Riesgo", f"{score}", delta=None)
            
            # Indicadores
            col2_1, col2_2, col2_3 = st.columns(3)
            with col2_1:
                st.metric("Nivel de Riesgo", riesgo)
            with col2_2:
                st.metric("Decisión", decision)
            with col2_3:
                st.metric("Prob. Aprobación", f"{prob_aprobacion:.1%}")
            
            # Factores de riesgo
            st.subheader("⚠️ Factores de Riesgo")
            factores_riesgo = []
            if impagos > 0:
                factores_riesgo.append(f"• Impagos previos: {impagos}")
            if consultas > 3:
                factores_riesgo.append(f"• Consultas recientes: {consultas}")
            if tarjetas > 3:
                factores_riesgo.append(f"• Tarjetas: {tarjetas}")
            if debt_ratio > 0.5:
                factores_riesgo.append(f"• Ratio deuda/ingresos: {debt_ratio:.1%}")
            
            if factores_riesgo:
                for factor in factores_riesgo:
                    st.warning(factor)
            else:
                st.success("✅ No se detectaron factores de riesgo significativos")

with tab2:
    st.header("📊 Análisis por Lotes")
    
    st.subheader("📋 Carga de Datos")
    
    uploaded_file = st.file_uploader("Cargar archivo CSV", type=['csv'])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.success(f"✅ Archivo cargado: {df.shape[0]} registros")
        
        # Mostrar tabla
        st.dataframe(df.head())
        
        # Análisis rápido
        st.subheader("📈 Análisis Rápido")
        
        # Simulación de evaluación por lotes
        def evaluar_fila(row):
            score = 500
            score += (row.get('score_bureau', 684) - 684) * 0.5
            score += (row.get('edad', 34) - 34) * 2
            score -= row.get('impagos_previos', 0) * 100
            score -= row.get('consultas_recientes', 0) * 30
            return max(0, min(1000, int(score)))
        
        df['score_calculado'] = df.apply(evaluar_fila, axis=1)
        
        # Estadísticas
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Score Promedio", f"{df['score_calculado'].mean():.0f}")
        with col2:
            aprobados = len(df[df['score_calculado'] >= 500])
            st.metric("Aprobados", f"{aprobados} ({aprobados/len(df):.1%})")
        with col3:
            st.metric("Rechazados", f"{len(df) - aprobados}")
        
        # Gráfico de distribución
        fig = px.histogram(df, x='score_calculado', nbins=20, title="Distribución de Scores")
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.header("🧠 Explicabilidad con SHAP")
    
    st.info("ℹ️ Esta sección muestra cómo el modelo toma decisiones usando SHAP (SHapley Additive exPlanations)")
    
    # Ejemplo de explicación
    st.subheader("📊 Explicación de Predicción")
    
    # Gráfico waterfall simulado
    fig = go.Figure()
    
    # Datos simulados de SHAP
    features = ['score_bureau', 'edad', 'ingresos', 'impagos_previos', 'consultas_recientes']
    shap_values = [120, 80, 60, -150, -90]
    base_value = 500
    
    # Crear gráfico waterfall
    fig.add_trace(go.Waterfall(
        name="SHAP Values",
        orientation="h",
        measure=["relative"] * len(features),
        x=shap_values,
        y=features,
        textposition="outside",
        text=[f"{val:+.0f}" for val in shap_values]
    ))
    
    fig.update_layout(
        title="Contribución de Características al Score",
        xaxis_title="Contribución al Score",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Explicación en texto
    st.subheader("📝 Explicación Detallada")
    
    explanation_text = """
    **Score Base:** 500 puntos
    
    **Factores Positivos:**
    • Score bureau alto: +120 puntos
    • Edad madura: +80 puntos  
    • Ingresos estables: +60 puntos
    
    **Factores Negativos:**
    • Impagos previos: -150 puntos
    • Consultas recientes: -90 puntos
    
    **Score Final:** 520 puntos
    """
    
    st.markdown(explanation_text)

with tab4:
    st.header("📈 Dashboard de Métricas")
    
    # Métricas del sistema
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Evaluaciones Hoy", "1,234", "+12%")
    with col2:
        st.metric("Tasa Aprobación", "68.5%", "+2.1%")
    with col3:
        st.metric("Score Promedio", "687", "+15")
    with col4:
        st.metric("Tiempo Respuesta", "0.023s", "-0.005s")
    
    # Gráficos de rendimiento
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de tendencia
        dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
        scores = np.random.normal(687, 50, 30)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates, y=scores, mode='lines+markers', name='Score Promedio'))
        fig.update_layout(title="Tendencia de Scores (30 días)", height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Gráfico de distribución de riesgo
        riesgo_data = ['Mínimo', 'Bajo', 'Medio', 'Alto', 'Crítico']
        riesgo_counts = [15, 35, 30, 15, 5]
        
        fig = go.Figure(data=[go.Pie(labels=riesgo_data, values=riesgo_counts)])
        fig.update_layout(title="Distribución de Nivel de Riesgo", height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    # Tabla de rendimiento de modelos
    st.subheader("🤖 Rendimiento de Modelos")
    
    model_data = {
        'Modelo': ['Logistic Regression', 'Random Forest', 'XGBoost'],
        'Accuracy': ['100.0%', '100.0%', '100.0%'],
        'Precision': ['100.0%', '100.0%', '100.0%'],
        'Recall': ['100.0%', '100.0%', '100.0%'],
        'ROC AUC': ['1.000', '1.000', '1.000']
    }
    
    df_models = pd.DataFrame(model_data)
    st.dataframe(df_models, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("🏦 **PFM Velmak** - Sistema de Scoring Crediticio con IA Explicable | Desarrollado con ❤️ por el equipo PFM Velmak")

if __name__ == "__main__":
    pass
