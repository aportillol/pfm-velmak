import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
import random
from datetime import datetime, timedelta
import json

# Configuración de la página
st.set_page_config(
    page_title="PFM VELMAK - Scoring Financiero Inteligente",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
def load_css():
    st.markdown("""
    <style>
    :root {
        --primary-color: #1e3a8a;
        --secondary-color: #64748b;
        --accent-color: #059669;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --danger-color: #ef4444;
        --background-color: #f8fafc;
        --card-background: #ffffff;
        --text-primary: #1e293b;
        --text-secondary: #64748b;
        --border-color: #e2e8f0;
        --shadow-sm: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }

    .main {
        background-color: var(--background-color);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .stSidebar {
        background-color: var(--card-background);
        border-right: 1px solid var(--border-color);
        box-shadow: var(--shadow-sm);
    }

    .card {
        background-color: var(--card-background);
        border-radius: 12px;
        padding: 24px;
        box-shadow: var(--shadow-md);
        border: 1px solid var(--border-color);
        margin-bottom: 20px;
    }

    .kpi-card {
        background: linear-gradient(135deg, var(--card-background) 0%, #f1f5f9 100%);
        border-radius: 16px;
        padding: 20px;
        box-shadow: var(--shadow-lg);
        border: 1px solid var(--border-color);
        text-align: center;
        transition: transform 0.2s ease;
    }

    .kpi-card:hover {
        transform: translateY(-2px);
    }

    .kpi-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--primary-color);
        margin: 8px 0;
    }

    .kpi-label {
        font-size: 0.875rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 600;
    }

    .kpi-change {
        font-size: 0.875rem;
        font-weight: 600;
        margin-top: 8px;
        padding: 4px 8px;
        border-radius: 6px;
        display: inline-block;
    }

    .positive {
        color: var(--success-color);
        background-color: rgba(16, 185, 129, 0.1);
    }

    .negative {
        color: var(--danger-color);
        background-color: rgba(239, 68, 68, 0.1);
    }

    .score-display {
        text-align: center;
        padding: 40px;
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        border-radius: 20px;
        box-shadow: var(--shadow-lg);
        border: 2px solid var(--success-color);
    }

    .score-value {
        font-size: 4rem;
        font-weight: 800;
        color: var(--primary-color);
        line-height: 1;
    }

    .decision-badge {
        display: inline-block;
        padding: 12px 24px;
        border-radius: 50px;
        font-weight: 700;
        font-size: 1.25rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin: 20px 0;
    }

    .approved {
        background-color: var(--success-color);
        color: white;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
    }

    .rejected {
        background-color: var(--danger-color);
        color: white;
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.3);
    }

    .shap-plot {
        background-color: var(--card-background);
        border-radius: 12px;
        padding: 20px;
        box-shadow: var(--shadow-md);
        border: 1px solid var(--border-color);
    }

    .loading-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 40px;
        background-color: var(--card-background);
        border-radius: 12px;
        box-shadow: var(--shadow-md);
    }

    .stSelectbox > div > div {
        background-color: var(--card-background);
        border-radius: 8px;
    }

    .stNumberInput > div > div > input {
        border-radius: 8px;
        border-color: var(--border-color);
    }

    .stButton > button {
        background-color: var(--primary-color);
        color: white;
        border-radius: 8px;
        font-weight: 600;
        padding: 12px 24px;
        border: none;
        box-shadow: var(--shadow-sm);
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        background-color: var(--secondary-color);
        transform: translateY(-1px);
        box-shadow: var(--shadow-md);
    }

    .plot-container {
        background-color: var(--card-background);
        border-radius: 12px;
        padding: 20px;
        box-shadow: var(--shadow-md);
        border: 1px solid var(--border-color);
    }

    .section-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 24px;
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .form-section {
        background-color: var(--card-background);
        border-radius: 12px;
        padding: 24px;
        box-shadow: var(--shadow-md);
        border: 1px solid var(--border-color);
        margin-bottom: 20px;
    }

    .form-section h3 {
        color: var(--text-primary);
        font-size: 1.125rem;
        font-weight: 600;
        margin-bottom: 16px;
        padding-bottom: 8px;
        border-bottom: 2px solid var(--accent-color);
    }
    </style>
    """, unsafe_allow_html=True)

# Funciones de datos simulados
def generate_dashboard_data():
    """Genera datos simulados para el dashboard"""
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    
    # KPIs actuales
    kpis = {
        'approval_rate': {'value': 87.5, 'change': 2.3, 'unit': '%'},
        'npl_rate': {'value': 3.2, 'change': -0.8, 'unit': '%'},
        'api_volume': {'value': 15420, 'change': 12.5, 'unit': 'peticiones'},
        'psi_score': {'value': 0.08, 'change': -0.02, 'unit': 'PSI'}
    }
    
    # Datos temporales para gráficos
    approval_data = pd.DataFrame({
        'date': dates,
        'approval_rate': np.random.normal(85, 5, 30),
        'npl_rate': np.random.normal(3.5, 0.8, 30),
        'risk_score': np.random.normal(720, 50, 30)
    })
    
    # Datos de distribución de riesgo
    risk_dist = pd.DataFrame({
        'category': ['Bajo Riesgo', 'Riesgo Medio-Bajo', 'Riesgo Medio', 'Riesgo Medio-Alto', 'Alto Riesgo'],
        'count': [350, 280, 180, 90, 45],
        'percentage': [35, 28, 18, 9, 4.5]
    })
    
    return kpis, approval_data, risk_dist

def simulate_scoring(traditional_data, alternative_data):
    """Simula proceso de scoring con explicabilidad"""
    # Simular procesamiento con delay
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    steps = [
        "Validando datos de entrada...",
        "Analizando datos tradicionales...",
        "Procesando datos alternativos...",
        "Ejecutando modelo de IA...",
        "Generando explicaciones...",
        "Finalizando evaluación..."
    ]
    
    for i, step in enumerate(steps):
        progress_bar.progress((i + 1) / len(steps))
        status_text.text(f"🤖 {step}")
        time.sleep(0.8)
    
    # Calcular score simulado
    base_score = 600
    
    # Contribución datos tradicionales
    income_score = min(200, traditional_data['monthly_income'] / 20)
    employment_score = 100 if traditional_data['employment_verified'] else 0
    credit_history_score = 150 if traditional_data['credit_history'] == 'Bueno' else 50
    
    # Contribución datos alternativos
    transaction_score = min(100, alternative_data['transaction_count'] * 2)
    digital_activity_score = min(80, alternative_data['digital_score'] / 10)
    stability_score = min(70, alternative_data['stability_months'] * 2)
    
    final_score = base_score + income_score + employment_score + credit_history_score + \
                 transaction_score + digital_activity_score + stability_score
    
    final_score = min(1000, max(0, final_score))
    
    # Decisión
    approved = final_score >= 650
    
    # Explicación SHAP simulada
    shap_explanation = {
        'account_balance': {'value': alternative_data.get('account_balance', 2000), 'impact': 85, 'direction': 'positive'},
        'monthly_income': {'value': traditional_data['monthly_income'], 'impact': 120, 'direction': 'positive'},
        'transaction_count': {'value': alternative_data['transaction_count'], 'impact': 45, 'direction': 'positive'},
        'employment_verified': {'value': traditional_data['employment_verified'], 'impact': 100, 'direction': 'positive'},
        'credit_utilization': {'value': alternative_data.get('credit_utilization', 0.3), 'impact': -30, 'direction': 'negative'},
        'digital_activity': {'value': alternative_data['digital_score'], 'impact': 35, 'direction': 'positive'},
        'stability_months': {'value': alternative_data['stability_months'], 'impact': 25, 'direction': 'positive'}
    }
    
    progress_bar.empty()
    status_text.empty()
    
    return final_score, approved, shap_explanation

def create_kpi_card(title, value, change, unit, icon):
    """Crea una tarjeta KPI"""
    change_class = "positive" if change > 0 else "negative"
    change_symbol = "↑" if change > 0 else "↓"
    
    return f"""
    <div class="kpi-card">
        <div class="kpi-label">{icon} {title}</div>
        <div class="kpi-value">{value:,}{unit}</div>
        <div class="kpi-change {change_class}">
            {change_symbol} {abs(change)}{unit}
        </div>
    </div>
    """

def create_shap_plot(shap_data):
    """Crea gráfico de explicación SHAP"""
    features = list(shap_data.keys())
    values = [shap_data[feature]['impact'] for feature in features]
    colors = ['#059669' if shap_data[feature]['direction'] == 'positive' else '#ef4444' for feature in features]
    
    fig = go.Figure(go.Bar(
        x=values,
        y=features,
        orientation='h',
        marker_color=colors,
        text=[f"{abs(v):.0f}" for v in values],
        textposition='auto',
    ))
    
    fig.update_layout(
        title="Contribución de Variables al Score de Crédito",
        xaxis_title="Impacto en Score",
        yaxis_title="Variables",
        height=400,
        margin=dict(l=20, r=20, t=40, b=20),
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

# Sidebar Navigation
st.sidebar.markdown("""
# 🏦 PFM VELMAK
### Scoring Financiero Inteligente
""", unsafe_allow_html=True)

page = st.sidebar.selectbox(
    "Navegación",
    ["📊 Dashboard Directivo", "🔍 Evaluador de Crédito", "📈 Análisis de Riesgos"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
**Versión:** 2.1.0  
**Última actualización:** Marzo 2024  
**Estado:** Producción
""")

# Vista 1: Dashboard Directivo
if page == "📊 Dashboard Directivo":
    st.markdown('<div class="section-title">📊 Dashboard Directivo</div>', unsafe_allow_html=True)
    
    # Generar datos
    kpis, approval_data, risk_dist = generate_dashboard_data()
    
    # KPIs principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(create_kpi_card(
            "Tasa de Aprobación", 
            kpis['approval_rate']['value'], 
            kpis['approval_rate']['change'],
            kpis['approval_rate']['unit'],
            "✅"
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_kpi_card(
            "Tasa de Morosidad (NPL)",
            kpis['npl_rate']['value'],
            kpis['npl_rate']['change'],
            kpis['npl_rate']['unit'],
            "⚠️"
        ), unsafe_allow_html=True)
    
    with col3:
        st.markdown(create_kpi_card(
            "Volumen API (MTD)",
            kpis['api_volume']['value'],
            kpis['api_volume']['change'],
            kpis['api_volume']['unit'],
            "📡"
        ), unsafe_allow_html=True)
    
    with col4:
        st.markdown(create_kpi_card(
            "Population Stability Index",
            kpis['psi_score']['value'],
            kpis['psi_score']['change'],
            kpis['psi_score']['unit'],
            "📊"
        ), unsafe_allow_html=True)
    
    # Gráficos principales
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="plot-container">', unsafe_allow_html=True)
        fig_trend = go.Figure()
        
        fig_trend.add_trace(go.Scatter(
            x=approval_data['date'],
            y=approval_data['approval_rate'],
            mode='lines+markers',
            name='Tasa de Aprobación',
            line=dict(color='#059669', width=3),
            marker=dict(size=6, color='#059669')
        ))
        
        fig_trend.add_trace(go.Scatter(
            x=approval_data['date'],
            y=approval_data['npl_rate'] * 10,  # Escalar para visualización
            mode='lines+markers',
            name='NPL Rate (x10)',
            line=dict(color='#ef4444', width=3, dash='dash'),
            marker=dict(size=6, color='#ef4444')
        ))
        
        fig_trend.update_layout(
            title="Evolución de Métricas Clave",
            xaxis_title="Fecha",
            yaxis_title="Porcentaje (%)",
            height=350,
            margin=dict(l=20, r=20, t=40, b=20),
            legend=dict(x=0, y=1, bgcolor='rgba(255,255,255,0.8)'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_trend, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="plot-container">', unsafe_allow_html=True)
        fig_risk = go.Figure(data=[go.Pie(
            labels=risk_dist['category'],
            values=risk_dist['count'],
            hole=0.4,
            marker_colors=['#059669', '#10b981', '#f59e0b', '#f97316', '#ef4444'],
            textinfo='label+percent',
            textposition='outside'
        )])
        
        fig_risk.update_layout(
            title="Distribución de Nivel de Riesgo",
            height=350,
            margin=dict(l=20, r=20, t=40, b=20),
            showlegend=True,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_risk, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Vista 2: Evaluador de Crédito
elif page == "🔍 Evaluador de Crédito":
    st.markdown('<div class="section-title">🔍 Evaluador de Crédito con IA Explicable</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Formulario de datos tradicionales
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown('<h3>📋 Datos Tradicionales</h3>', unsafe_allow_html=True)
        
        traditional_data = {
            'monthly_income': st.number_input("Ingreso Mensual (€)", min_value=0, max_value=20000, value=3000, step=100),
            'employment_verified': st.checkbox("Verificación de Empleo", value=True),
            'credit_history': st.selectbox("Historial Crediticio", ["Excelente", "Bueno", "Regular", "Malo"], index=1),
            'existing_debts': st.number_input("Deudas Existentes (€)", min_value=0, max_value=50000, value=5000, step=500),
            'age': st.number_input("Edad", min_value=18, max_value=100, value=35, step=1)
        }
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Formulario de datos alternativos
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown('<h3>📱 Datos Alternativos</h3>', unsafe_allow_html=True)
        
        alternative_data = {
            'account_balance': st.number_input("Saldo en Cuenta (€)", min_value=0, max_value=100000, value=5000, step=100),
            'transaction_count': st.number_input("Transacciones Mensuales", min_value=0, max_value=200, value=45, step=1),
            'digital_score': st.number_input("Score Digital (0-100)", min_value=0, max_value=100, value=75, step=1),
            'stability_months': st.number_input("Meses de Estabilidad", min_value=0, max_value=120, value=24, step=1),
            'credit_utilization': st.slider("Utilización de Crédito", 0.0, 1.0, 0.35, 0.05),
            'social_media_activity': st.selectbox("Actividad Redes Sociales", ["Baja", "Media", "Alta"], index=1)
        }
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Botón de evaluación
        if st.button("🚀 Evaluar Cliente", type="primary", use_container_width=True):
            score, approved, shap_explanation = simulate_scoring(traditional_data, alternative_data)
            
            # Guardar resultados en session state
            st.session_state.score = score
            st.session_state.approved = approved
            st.session_state.shap_explanation = shap_explanation
            st.session_state.traditional_data = traditional_data
            st.session_state.alternative_data = alternative_data
    
    with col2:
        # Resultados
        if 'score' in st.session_state:
            # Score principal
            st.markdown('<div class="score-display">', unsafe_allow_html=True)
            st.markdown(f'<div class="score-value">{st.session_state.score}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="score-value" style="font-size: 1.2rem; color: var(--text-secondary);">Score de Crédito (0-1000)</div>', unsafe_allow_html=True)
            
            if st.session_state.approved:
                st.markdown('<div class="decision-badge approved">✅ CRÉDITO APROBADO</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="decision-badge rejected">❌ CRÉDITO DENEGADO</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Explicación SHAP
            st.markdown('<div class="shap-plot">', unsafe_allow_html=True)
            st.markdown('<h4 style="color: var(--text-primary); margin-bottom: 16px;">🔍 Explicación de la Decisión (IA Explicable)</h4>', unsafe_allow_html=True)
            
            shap_fig = create_shap_plot(st.session_state.shap_explanation)
            st.plotly_chart(shap_fig, use_container_width=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Detalles de contribución
            st.markdown('<div class="form-section">', unsafe_allow_html=True)
            st.markdown('<h4>📊 Análisis Detallado de Variables</h4>', unsafe_allow_html=True)
            
            for feature, data in st.session_state.shap_explanation.items():
                direction_icon = "↗️" if data['direction'] == 'positive' else "↘️"
                direction_color = "#059669" if data['direction'] == 'positive' else "#ef4444"
                
                st.markdown(f"""
                <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 0; border-bottom: 1px solid var(--border-color);">
                    <span style="font-weight: 600;">{feature.replace('_', ' ').title()}</span>
                    <span style="color: {direction_color}; font-weight: 600;">
                        {direction_icon} {data['impact']:+.0f} pts
                    </span>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

# Vista 3: Análisis de Riesgos
elif page == "📈 Análisis de Riesgos":
    st.markdown('<div class="section-title">📈 Análisis Avanzado de Riesgos</div>', unsafe_allow_html=True)
    
    # Filtros de análisis
    col1, col2, col3 = st.columns(3)
    
    with col1:
        risk_segment = st.selectbox("Segmento de Riesgo", ["Todos", "Bajo", "Medio", "Alto"])
    
    with col2:
        time_period = st.selectbox("Período de Tiempo", ["Últimos 7 días", "Últimos 30 días", "Últimos 90 días"])
    
    with col3:
        model_version = st.selectbox("Versión del Modelo", ["v2.1.0 (Actual)", "v2.0.3", "v1.9.0"])
    
    # Análisis de drift
    st.markdown('<div class="plot-container">', unsafe_allow_html=True)
    st.markdown('<h4>📊 Population Stability Index (PSI) por Variable</h4>', unsafe_allow_html=True)
    
    # Datos simulados de PSI
    psi_data = pd.DataFrame({
        'variable': ['account_balance', 'monthly_income', 'transaction_count', 'credit_utilization', 'digital_score'],
        'psi_current': [0.08, 0.12, 0.05, 0.15, 0.09],
        'psi_threshold': [0.10, 0.10, 0.10, 0.10, 0.10],
        'status': ['Estable', 'Advertencia', 'Estable', 'Crítico', 'Estable']
    })
    
    fig_psi = go.Figure()
    
    # Barras de PSI actual
    fig_psi.add_trace(go.Bar(
        x=psi_data['variable'],
        y=psi_data['psi_current'],
        name='PSI Actual',
        marker_color=['#059669' if psi <= 0.10 else '#f59e0b' if psi <= 0.25 else '#ef4444' for psi in psi_data['psi_current']]
    ))
    
    # Línea de umbral
    fig_psi.add_trace(go.Scatter(
        x=psi_data['variable'],
        y=psi_data['psi_threshold'],
        mode='lines',
        name='Umbral Crítico',
        line=dict(color='#ef4444', width=2, dash='dash')
    ))
    
    fig_psi.update_layout(
        title="Monitoreo de Data Drift",
        xaxis_title="Variables del Modelo",
        yaxis_title="Population Stability Index",
        height=400,
        margin=dict(l=20, r=20, t=40, b=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig_psi, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Métricas de rendimiento
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="plot-container">', unsafe_allow_html=True)
        
        # Datos simulados de rendimiento
        performance_data = pd.DataFrame({
            'metric': ['Precisión', 'Recall', 'F1-Score', 'ROC-AUC'],
            'current': [0.89, 0.87, 0.88, 0.92],
            'baseline': [0.85, 0.83, 0.84, 0.88],
            'target': [0.90, 0.90, 0.90, 0.95]
        })
        
        fig_perf = go.Figure()
        
        fig_perf.add_trace(go.Bar(
            x=performance_data['metric'],
            y=performance_data['current'],
            name='Actual',
            marker_color='#059669'
        ))
        
        fig_perf.add_trace(go.Bar(
            x=performance_data['metric'],
            y=performance_data['baseline'],
            name='Línea Base',
            marker_color='#64748b'
        ))
        
        fig_perf.add_trace(go.Scatter(
            x=performance_data['metric'],
            y=performance_data['target'],
            mode='lines+markers',
            name='Objetivo',
            line=dict(color='#f59e0b', width=3),
            marker=dict(size=8, color='#f59e0b')
        ))
        
        fig_perf.update_layout(
            title="Métricas de Rendimiento del Modelo",
            xaxis_title="Métricas",
            yaxis_title="Valor",
            height=350,
            margin=dict(l=20, r=20, t=40, b=20),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_perf, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="plot-container">', unsafe_allow_html=True)
        
        # Análisis de sesgos
        bias_data = pd.DataFrame({
            'segment': ['18-25 años', '26-35 años', '36-45 años', '46-55 años', '56+ años'],
            'approval_rate': [82.5, 87.3, 89.1, 85.6, 78.9],
            'avg_score': [680, 720, 750, 690, 640],
            'sample_size': [450, 680, 520, 380, 290]
        })
        
        fig_bias = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Tasa de Aprobación por Edad', 'Score Promedio por Edad'),
            vertical_spacing=0.1
        )
        
        fig_bias.add_trace(
            go.Bar(x=bias_data['segment'], y=bias_data['approval_rate'], name='Tasa Aprobación', marker_color='#059669'),
            row=1, col=1
        )
        
        fig_bias.add_trace(
            go.Bar(x=bias_data['segment'], y=bias_data['avg_score'], name='Score Promedio', marker_color='#64748b'),
            row=2, col=1
        )
        
        fig_bias.update_layout(
            title="Análisis de Equidad Algorítmica",
            height=500,
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_bias, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: var(--text-secondary); padding: 20px;'>
    <strong>PFM VELMAK</strong> - Scoring Financiero con IA Explicable<br>
    <small>Desarrollado con ❤️ usando Streamlit | Cumplimiento GDPR & AI Act</small>
</div>
""", unsafe_allow_html=True)

# Cargar CSS
load_css()
