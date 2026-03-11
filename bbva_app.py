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

# Configuración de la página PFM VELMAK
st.set_page_config(
    page_title="PFM VELMAK - Algoritmo de la Confianza",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS PFM VELMAK Design System
def load_bbva_css():
    st.markdown("""
    <style>
    :root {
        /* Colores Corporativos PFM VELMAK */
        --bbva-core-blue: #004481;
        --bbva-navy: #072146;
        --bbva-aqua: #028484;
        --bbva-light-aqua: #2DCCCD;
        --bbva-background: #F4F4F4;
        --bbva-white: #FFFFFF;
        
        /* Colores Semánticos */
        --bbva-success: #48AE64;
        --bbva-warning: #F7893B;
        --bbva-danger: #DA3851;
        --bbva-text-secondary: #666666;
        
        /* Sombras y Bordes */
        --bbva-shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.08);
        --bbva-shadow-md: 0 4px 12px rgba(0, 0, 0, 0.12);
        --bbva-border-radius: 8px;
        --bbva-border-light: #E8E8E8;
    }

    .main {
        background-color: var(--bbva-background);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        color: var(--bbva-navy);
    }

    .stSidebar {
        background-color: var(--bbva-navy);
        color: white;
        border-right: none;
        box-shadow: var(--bbva-shadow-md);
    }

    .stSidebar .stSelectbox > div > div {
        background-color: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: var(--bbva-border-radius);
        color: white;
    }

    .stSidebar .stNumberInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: var(--bbva-border-radius);
        color: white;
    }

    .stSidebar .stCheckbox > label {
        color: white;
    }

    .bbva-card {
        background-color: var(--bbva-white);
        border-radius: var(--bbva-border-radius);
        padding: 24px;
        box-shadow: var(--bbva-shadow-sm);
        border: 1px solid var(--bbva-border-light);
        margin-bottom: 20px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .bbva-card:hover {
        transform: translateY(-2px);
        box-shadow: var(--bbva-shadow-md);
    }

    .bbva-kpi-card {
        background: linear-gradient(135deg, var(--bbva-white) 0%, #FAFAFA 100%);
        border-radius: var(--bbva-border-radius);
        padding: 24px;
        box-shadow: var(--bbva-shadow-md);
        border: 1px solid var(--bbva-border-light);
        text-align: center;
        transition: all 0.3s ease;
    }

    .bbva-kpi-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(0, 71, 133, 0.15);
    }

    .bbva-kpi-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--bbva-core-blue);
        margin: 12px 0;
        line-height: 1;
    }

    .bbva-kpi-label {
        font-size: 0.875rem;
        color: var(--bbva-text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 600;
        margin-bottom: 8px;
    }

    .bbva-kpi-change {
        font-size: 0.875rem;
        font-weight: 600;
        margin-top: 12px;
        padding: 6px 12px;
        border-radius: 6px;
        display: inline-block;
    }

    .bbva-positive {
        color: var(--bbva-success);
        background-color: rgba(72, 174, 100, 0.1);
        border: 1px solid rgba(72, 174, 100, 0.2);
    }

    .bbva-negative {
        color: var(--bbva-danger);
        background-color: rgba(218, 56, 81, 0.1);
        border: 1px solid rgba(218, 56, 81, 0.2);
    }

    .bbva-score-display {
        text-align: center;
        padding: 48px;
        background: linear-gradient(135deg, var(--bbva-white) 0%, #F8F9FA 100%);
        border-radius: var(--bbva-border-radius);
        box-shadow: var(--bbva-shadow-md);
        border: 3px solid var(--bbva-aqua);
        position: relative;
        overflow: hidden;
    }

    .bbva-score-display::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--bbva-aqua), var(--bbva-light-aqua));
    }

    .bbva-score-value {
        font-size: 4.5rem;
        font-weight: 800;
        color: var(--bbva-core-blue);
        line-height: 1;
        margin: 16px 0;
    }

    .bbva-decision-badge {
        display: inline-block;
        padding: 16px 32px;
        border-radius: 50px;
        font-weight: 700;
        font-size: 1.25rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin: 24px 0;
        transition: all 0.3s ease;
    }

    .bbva-approved {
        background-color: var(--bbva-success);
        color: white;
        box-shadow: 0 6px 20px rgba(72, 174, 100, 0.4);
    }

    .bbva-approved:hover {
        background-color: #3A8F52;
        transform: translateY(-2px);
    }

    .bbva-rejected {
        background-color: var(--bbva-danger);
        color: white;
        box-shadow: 0 6px 20px rgba(218, 56, 81, 0.4);
    }

    .bbva-rejected:hover {
        background-color: #C52F41;
        transform: translateY(-2px);
    }

    .bbva-shap-plot {
        background-color: var(--bbva-white);
        border-radius: var(--bbva-border-radius);
        padding: 24px;
        box-shadow: var(--bbva-shadow-sm);
        border: 1px solid var(--bbva-border-light);
    }

    .bbva-loading {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 48px;
        background-color: var(--bbva-white);
        border-radius: var(--bbva-border-radius);
        box-shadow: var(--bbva-shadow-sm);
        border: 2px solid var(--bbva-aqua);
    }

    .bbva-spinner {
        width: 48px;
        height: 48px;
        border: 4px solid var(--bbva-border-light);
        border-top: 4px solid var(--bbva-aqua);
        border-radius: 50%;
        animation: bbva-spin 1s linear infinite;
    }

    @keyframes bbva-spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    .bbva-loading-text {
        margin-left: 16px;
        color: var(--bbva-navy);
        font-weight: 600;
        font-size: 1.125rem;
    }

    .bbva-section-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--bbva-navy);
        margin-bottom: 24px;
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .bbva-form-section {
        background-color: var(--bbva-white);
        border-radius: var(--bbva-border-radius);
        padding: 24px;
        box-shadow: var(--bbva-shadow-sm);
        border: 1px solid var(--bbva-border-light);
        margin-bottom: 20px;
    }

    .bbva-form-section h3 {
        color: var(--bbva-navy);
        font-size: 1.125rem;
        font-weight: 600;
        margin-bottom: 16px;
        padding-bottom: 8px;
        border-bottom: 2px solid var(--bbva-aqua);
    }

    .bbva-plot-container {
        background-color: var(--bbva-white);
        border-radius: var(--bbva-border-radius);
        padding: 24px;
        box-shadow: var(--bbva-shadow-sm);
        border: 1px solid var(--bbva-border-light);
    }

    .stButton > button {
        background-color: var(--bbva-aqua);
        color: white;
        border-radius: var(--bbva-border-radius);
        font-weight: 600;
        padding: 14px 28px;
        border: none;
        box-shadow: var(--bbva-shadow-sm);
        transition: all 0.2s ease;
        font-size: 1rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .stButton > button:hover {
        background-color: var(--bbva-core-blue);
        transform: translateY(-1px);
        box-shadow: var(--bbva-shadow-md);
    }

    .bbva-data-table {
        width: 100%;
        border-collapse: collapse;
        margin: 16px 0;
        font-size: 0.875rem;
    }

    .bbva-data-table th,
    .bbva-data-table td {
        padding: 12px;
        text-align: left;
        border-bottom: 1px solid var(--bbva-border-light);
    }

    .bbva-data-table th {
        background-color: rgba(0, 71, 133, 0.05);
        font-weight: 600;
        color: var(--bbva-navy);
    }

    /* Sin bordes en tablas para Data-Ink Ratio óptimo */
    .dataframe {
        border: none;
    }

    .dataframe th {
        border: none;
        background-color: rgba(0, 71, 133, 0.05);
    }

    .dataframe td {
        border: none;
        border-bottom: 1px solid var(--bbva-border-light);
    }
    </style>
    """, unsafe_allow_html=True)

# Funciones de datos simulados
def generate_bbva_dashboard_data():
    """Genera datos simulados para dashboard BBVA"""
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    
    # KPIs actuales con estilo BBVA
    kpis = {
        'approval_rate': {'value': 91.2, 'change': 3.1, 'unit': '%'},
        'npl_rate': {'value': 2.8, 'change': -1.2, 'unit': '%'},
        'api_volume': {'value': 18750, 'change': 15.3, 'unit': 'peticiones'},
        'psi_score': {'value': 0.06, 'change': -0.03, 'unit': 'PSI'}
    }
    
    # Datos temporales para gráficos
    approval_data = pd.DataFrame({
        'date': dates,
        'approval_rate': np.random.normal(89, 4, 30),
        'npl_rate': np.random.normal(3.2, 0.6, 30),
        'risk_score': np.random.normal(740, 45, 30)
    })
    
    # Datos de distribución de riesgo
    risk_dist = pd.DataFrame({
        'category': ['Riesgo Bajo', 'Riesgo Medio-Bajo', 'Riesgo Medio', 'Riesgo Medio-Alto', 'Riesgo Alto'],
        'count': [420, 310, 195, 65, 25],
        'percentage': [38.2, 28.2, 17.7, 5.9, 2.3]
    })
    
    return kpis, approval_data, risk_dist

def simulate_bbva_scoring(traditional_data, alternative_data):
    """Simula proceso de scoring con experiencia BBVA"""
    # Simular procesamiento con loading BBVA
    progress_bar = st.progress(0)
    loading_container = st.container()
    
    with loading_container:
        st.markdown("""
        <div class="bbva-loading">
            <div class="bbva-spinner"></div>
            <div class="bbva-loading-text">Analizando con Algoritmo de Confianza...</div>
        </div>
        """, unsafe_allow_html=True)
    
    steps = [
        "Validando identidad del cliente...",
        "Consultando historial crediticio BBVA...",
        "Analizando datos alternativos...",
        "Ejecutando modelo de IA explicable...",
        "Generando explicación detallada...",
        "Verificando cumplimiento normativo..."
    ]
    
    for i, step in enumerate(steps):
        progress_bar.progress((i + 1) / len(steps))
        time.sleep(0.6)
    
    # Calcular score BBVA
    base_score = 650
    
    # Contribución datos tradicionales (peso mayor)
    income_score = min(180, traditional_data['monthly_income'] / 25)
    employment_score = 120 if traditional_data['employment_verified'] else 0
    credit_history_score = 130 if traditional_data['credit_history'] == 'Excelente' else 70
    
    # Contribución datos alternativos
    transaction_score = min(80, alternative_data['transaction_count'] * 1.8)
    digital_score = min(60, alternative_data['digital_score'] / 10)
    stability_score = min(50, alternative_data['stability_months'] * 2)
    
    final_score = base_score + income_score + employment_score + credit_history_score + \
                 transaction_score + digital_score + stability_score
    
    final_score = min(1000, max(0, final_score))
    
    # Decisión BBVA
    approved = final_score >= 700
    
    # Explicación SHAP BBVA
    shap_explanation = {
        'account_balance': {'value': alternative_data.get('account_balance', 3000), 'impact': 75, 'direction': 'positive'},
        'monthly_income': {'value': traditional_data['monthly_income'], 'impact': 110, 'direction': 'positive'},
        'transaction_count': {'value': alternative_data['transaction_count'], 'impact': 40, 'direction': 'positive'},
        'employment_verified': {'value': traditional_data['employment_verified'], 'impact': 120, 'direction': 'positive'},
        'credit_utilization': {'value': alternative_data.get('credit_utilization', 0.25), 'impact': -25, 'direction': 'negative'},
        'digital_activity': {'value': alternative_data['digital_score'], 'impact': 30, 'direction': 'positive'},
        'stability_months': {'value': alternative_data['stability_months'], 'impact': 20, 'direction': 'positive'}
    }
    
    # Limpiar loading
    loading_container.empty()
    progress_bar.empty()
    
    return final_score, approved, shap_explanation

def create_bbva_kpi_card(title, value, change, unit, icon):
    """Crea tarjeta KPI estilo BBVA"""
    change_class = "bbva-positive" if change > 0 else "bbva-negative"
    change_symbol = "↑" if change > 0 else "↓"
    
    return f"""
    <div class="bbva-kpi-card">
        <div class="bbva-kpi-label">{icon} {title}</div>
        <div class="bbva-kpi-value">{value:,}{unit}</div>
        <div class="bbva-kpi-change {change_class}">
            {change_symbol} {abs(change)}{unit}
        </div>
    </div>
    """

def create_bbva_shap_plot(shap_data):
    """Crea gráfico SHAP estilo BBVA"""
    features = list(shap_data.keys())
    values = [shap_data[feature]['impact'] for feature in features]
    colors = ['#48AE64' if shap_data[feature]['direction'] == 'positive' else '#DA3851' for feature in features]
    
    fig = go.Figure(go.Bar(
        x=values,
        y=features,
        orientation='h',
        marker_color=colors,
        text=[f"{abs(v):.0f}" for v in values],
        textposition='auto',
    ))
    
    fig.update_layout(
        title="Explicación Algoritmo de Confianza BBVA",
        xaxis_title="Impacto en Score",
        yaxis_title="Variables Analizadas",
        height=450,
        margin=dict(l=20, r=20, t=40, b=20),
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#072146')
    )
    
    return fig

# Sidebar PFM VELMAK
st.sidebar.markdown("""
# 🏦 PFM VELMAK
## Scoring Financiero Inteligente
""", unsafe_allow_html=True)

page = st.sidebar.selectbox(
    "Navegación",
    ["📊 Dashboard Directivo", "🔍 Evaluador de Crédito"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
**Versión:** 3.0.0  
**Entorno:** Producción  
**Estado:** Activo  
**Cumplimiento:** GDPR & AI Act
""")

# Vista 1: Dashboard Directivo PFM VELMAK
if page == "📊 Dashboard Directivo":
    st.markdown('<div class="bbva-section-title">📊 Dashboard Directivo PFM VELMAK</div>', unsafe_allow_html=True)
    
    # Generar datos PFM VELMAK
    kpis, approval_data, risk_dist = generate_bbva_dashboard_data()
    
    # KPIs principales PFM VELMAK
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(create_bbva_kpi_card(
            "Tasa de Aprobación", 
            kpis['approval_rate']['value'], 
            kpis['approval_rate']['change'],
            kpis['approval_rate']['unit'],
            "✅"
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_bbva_kpi_card(
            "Tasa de Morosidad",
            kpis['npl_rate']['value'],
            kpis['npl_rate']['change'],
            kpis['npl_rate']['unit'],
            "⚠️"
        ), unsafe_allow_html=True)
    
    with col3:
        st.markdown(create_bbva_kpi_card(
            "Volumen API",
            kpis['api_volume']['value'],
            kpis['api_volume']['change'],
            kpis['api_volume']['unit'],
            "📡"
        ), unsafe_allow_html=True)
    
    with col4:
        st.markdown(create_bbva_kpi_card(
            "Population Stability",
            kpis['psi_score']['value'],
            kpis['psi_score']['change'],
            kpis['psi_score']['unit'],
            "📊"
        ), unsafe_allow_html=True)
    
    # Gráficos BBVA
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="bbva-plot-container">', unsafe_allow_html=True)
        fig_trend = go.Figure()
        
        fig_trend.add_trace(go.Scatter(
            x=approval_data['date'],
            y=approval_data['approval_rate'],
            mode='lines+markers',
            name='Tasa de Aprobación',
            line=dict(color='#004481', width=3),
            marker=dict(size=6, color='#004481')
        ))
        
        fig_trend.add_trace(go.Scatter(
            x=approval_data['date'],
            y=approval_data['npl_rate'] * 10,
            mode='lines+markers',
            name='NPL Rate (x10)',
            line=dict(color='#DA3851', width=3, dash='dash'),
            marker=dict(size=6, color='#DA3851')
        ))
        
        fig_trend.update_layout(
            title="Evolución Métricas BBVA",
            xaxis_title="Fecha",
            yaxis_title="Porcentaje (%)",
            height=350,
            margin=dict(l=20, r=20, t=40, b=20),
            legend=dict(x=0, y=1, bgcolor='rgba(255,255,255,0.9)'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#072146')
        )
        
        st.plotly_chart(fig_trend, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="bbva-plot-container">', unsafe_allow_html=True)
        fig_risk = go.Figure(data=[go.Pie(
            labels=risk_dist['category'],
            values=risk_dist['count'],
            hole=0.4,
            marker_colors=['#48AE64', '#028484', '#F7893B', '#F4F4F4', '#DA3851'],
            textinfo='label+percent',
            textposition='outside'
        )])
        
        fig_risk.update_layout(
            title="Distribución Nivel de Riesgo",
            height=350,
            margin=dict(l=20, r=20, t=40, b=20),
            showlegend=True,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#072146')
        )
        
        st.plotly_chart(fig_risk, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Vista 2: Evaluador PFM VELMAK
elif page == "🔍 Evaluador de Crédito":
    st.markdown('<div class="bbva-section-title">🔍 Algoritmo de Confianza PFM VELMAK</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Formulario PFM VELMAK
        st.markdown('<div class="bbva-form-section">', unsafe_allow_html=True)
        st.markdown('<h3>📋 Datos Tradicionales PFM VELMAK</h3>', unsafe_allow_html=True)
        
        traditional_data = {
            'monthly_income': st.number_input("Ingreso Mensual (€)", min_value=0, max_value=25000, value=4500, step=100),
            'employment_verified': st.checkbox("Verificación de Empleo PFM VELMAK", value=True),
            'credit_history': st.selectbox("Historial Crediticio PFM VELMAK", ["Excelente", "Bueno", "Regular", "Malo"], index=0),
            'existing_debts': st.number_input("Deudas Existentes (€)", min_value=0, max_value=100000, value=8000, step=500),
            'age': st.number_input("Edad", min_value=18, max_value=100, value=38, step=1)
        }
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="bbva-form-section">', unsafe_allow_html=True)
        st.markdown('<h3>📋 Datos Alternativos PFM VELMAK</h3>', unsafe_allow_html=True)
        
        alternative_data = {
            'account_balance': st.number_input("Saldo en Cuenta PFM VELMAK (€)", min_value=0, max_value=150000, value=7500, step=100),
            'transaction_count': st.number_input("Transacciones Mensuales", min_value=0, max_value=300, value=52, step=1),
            'digital_score': st.number_input("Score Digital PFM VELMAK (0-100)", min_value=0, max_value=100, value=82, step=1),
            'stability_months': st.number_input("Meses de Estabilidad PFM VELMAK", min_value=0, max_value=120, value=30, step=1),
            'credit_utilization': st.slider("Utilización de Crédito PFM VELMAK", 0.0, 1.0, 0.28, 0.05),
            'velmak_products': st.multiselect("Productos PFM VELMAK", ["Cuenta Corriente", "Tarjeta Crédito", "Préstamo Personal", "Hipoteca"], default=["Cuenta Corriente", "Tarjeta Crédito"])
        }
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Botón PFM VELMAK
        if st.button("🚀 Evaluar con Algoritmo PFM VELMAK", type="primary", use_container_width=True):
            score, approved, shap_explanation = simulate_bbva_scoring(traditional_data, alternative_data)
            
            st.session_state.score = score
            st.session_state.approved = approved
            st.session_state.shap_explanation = shap_explanation
            st.session_state.traditional_data = traditional_data
            st.session_state.alternative_data = alternative_data
    
    with col2:
        # Resultados PFM VELMAK
        if 'score' in st.session_state:
            # Score BBVA
            st.markdown('<div class="bbva-score-display">', unsafe_allow_html=True)
            st.markdown(f'<div class="bbva-score-value">{st.session_state.score}</div>', unsafe_allow_html=True)
            st.markdown(f'<div style="font-size: 1.2rem; color: var(--bbva-text-secondary); margin-bottom: 16px;">Algoritmo de Confianza PFM VELMAK (0-1000)</div>', unsafe_allow_html=True)
            
            if st.session_state.approved:
                st.markdown('<div class="bbva-decision-badge bbva-approved">✅ CRÉDITO APROBADO</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="bbva-decision-badge bbva-rejected">❌ CRÉDITO DENEGADO</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Explicación SHAP BBVA
            st.markdown('<div class="bbva-shap-plot">', unsafe_allow_html=True)
            st.markdown('<h4 style="color: var(--bbva-navy); margin-bottom: 16px;">🔍 Explicación Detallada IA Explicable PFM VELMAK</h4>', unsafe_allow_html=True)
            
            shap_fig = create_bbva_shap_plot(st.session_state.shap_explanation)
            st.plotly_chart(shap_fig, use_container_width=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Resumen decisión BBVA
            st.markdown('<div class="bbva-form-section">', unsafe_allow_html=True)
            st.markdown('<h4>📊 Resumen Decisión BBVA</h4>', unsafe_allow_html=True)
            
            # Tabla de factores BBVA
            factors_data = []
            for feature, data in st.session_state.shap_explanation.items():
                direction_icon = "↗️" if data['direction'] == 'positive' else "↘️"
                direction_color = "#48AE64" if data['direction'] == 'positive' else "#DA3851"
                
                factors_data.append({
                    'Variable': feature.replace('_', ' ').title(),
                    'Valor': f"{data['value']:,.2f}",
                    'Impacto': f"{data['impact']:+.0f} pts",
                    'Dirección': f"{direction_icon} {data['direction'].title()}"
                })
            
            factors_df = pd.DataFrame(factors_data)
            st.dataframe(factors_df, hide_index=True, use_container_width=True)
            
            # Explicación en texto
            if st.session_state.approved:
                st.markdown("""
                <div style="background-color: rgba(72, 174, 100, 0.1); padding: 16px; border-radius: 8px; border-left: 4px solid #48AE64; margin: 16px 0;">
                    <strong>✅ Decisión Favorable:</strong> El perfil cumple con los estándares de BBVA para aprobación de crédito. 
                    Los factores positivos superan significativamente a los factores de riesgo.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="background-color: rgba(218, 56, 81, 0.1); padding: 16px; border-radius: 8px; border-left: 4px solid #DA3851; margin: 16px 0;">
                    <strong>❌ Decisión Desfavorable:</strong> El perfil no cumple actualmente con los criterios de aprobación.
                    Se recomienda mejorar los aspectos identificados antes de una nueva evaluación.
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

# Footer PFM VELMAK
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: var(--bbva-text-secondary); padding: 24px; border-top: 1px solid var(--bbva-border-light);'>
    <strong>PFM VELMAK Algoritmo de Confianza</strong><br>
    <small> 2024 PFM VELMAK | Desarrollado con IA Explicable</small><br>
    <small style="color: var(--bbva-aqua);">Cumplimiento GDPR & AI Act</small>
</div>
""", unsafe_allow_html=True)

# Cargar CSS BBVA
load_bbva_css()
