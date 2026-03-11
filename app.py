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

# Configuración de página PFM VELMAK
st.set_page_config(
    page_title="PFM VELMAK - Sistema de Scoring Financiero",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado - Design System BBVA para PFM VELMAK
def load_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    :root {
        /* Colores Corporativos BBVA para PFM VELMAK */
        --bbva-core-blue: #004481;
        --bbva-navy: #072146;
        --bbva-aqua: #028484;
        --bbva-light-aqua: #2DCCCD;
        --bbva-background: #F4F4F4;
        --bbva-white: #FFFFFF;
        
        /* Colores Semánticos BBVA */
        --bbva-success: #48AE64;
        --bbva-warning: #F7893B;
        --bbva-danger: #DA3851;
        --bbva-text-secondary: #666666;
        
        /* Variables de diseño */
        --bbva-shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.08);
        --bbva-shadow-md: 0 4px 16px rgba(0, 0, 0, 0.12);
        --bbva-shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.16);
        --bbva-border-radius: 8px;
        --bbva-border-light: #E8E8E8;
    }

    /* Fuente global */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    }

    /* Fondo principal */
    .main {
        background-color: var(--bbva-background);
        color: var(--bbva-navy);
    }

    /* Sidebar personalizado */
    .stSidebar {
        background-color: var(--bbva-navy) !important;
        color: white !important;
        border-right: none !important;
        box-shadow: var(--bbva-shadow-md);
    }

    .stSidebar .stSelectbox > div > div {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: var(--bbva-border-radius) !important;
        color: white !important;
    }

    .stSidebar .stSelectbox > div > div > div {
        color: white !important;
    }

    .stSidebar .stNumberInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: var(--bbva-border-radius) !important;
        color: white !important;
    }

    .stSidebar .stCheckbox > label {
        color: white !important;
    }

    .stSidebar .stSlider > div > div > div {
        background-color: var(--bbva-aqua) !important;
    }

    .stSidebar .stSlider > div > div > div > div {
        background-color: white !important;
    }

    /* Tarjetas principales */
    .velmak-card {
        background-color: var(--bbva-white);
        border-radius: var(--bbva-border-radius);
        padding: 24px;
        box-shadow: var(--bbva-shadow-sm);
        border: 1px solid var(--bbva-border-light);
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }

    .velmak-card:hover {
        transform: translateY(-2px);
        box-shadow: var(--bbva-shadow-md);
    }

    /* Tarjetas KPI */
    .velmak-kpi-card {
        background: linear-gradient(135deg, var(--bbva-white) 0%, #FAFAFA 100%);
        border-radius: var(--bbva-border-radius);
        padding: 28px;
        box-shadow: var(--bbva-shadow-md);
        border: 1px solid var(--bbva-border-light);
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }

    .velmak-kpi-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(180deg, var(--bbva-core-blue), var(--bbva-aqua));
    }

    .velmak-kpi-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--bbva-shadow-lg);
    }

    .velmak-kpi-value {
        font-size: 2.75rem;
        font-weight: 800;
        color: var(--bbva-core-blue);
        margin: 12px 0;
        line-height: 1;
    }

    .velmak-kpi-label {
        font-size: 0.875rem;
        color: var(--bbva-text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 600;
        margin-bottom: 8px;
    }

    .velmak-kpi-change {
        font-size: 0.875rem;
        font-weight: 600;
        margin-top: 12px;
        padding: 6px 12px;
        border-radius: 6px;
        display: inline-block;
    }

    .velmak-positive {
        color: var(--bbva-success);
        background-color: rgba(72, 174, 100, 0.1);
        border: 1px solid rgba(72, 174, 100, 0.2);
    }

    .velmak-negative {
        color: var(--bbva-danger);
        background-color: rgba(218, 56, 81, 0.1);
        border: 1px solid rgba(218, 56, 81, 0.2);
    }

    /* Score Display */
    .velmak-score-display {
        text-align: center;
        padding: 48px;
        background: linear-gradient(135deg, var(--bbva-white) 0%, #F8F9FA 100%);
        border-radius: var(--bbva-border-radius);
        box-shadow: var(--bbva-shadow-md);
        border: 3px solid var(--bbva-aqua);
        position: relative;
        overflow: hidden;
    }

    .velmak-score-display::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--bbva-aqua), var(--bbva-light-aqua));
    }

    .velmak-score-value {
        font-size: 4.5rem;
        font-weight: 800;
        color: var(--bbva-core-blue);
        line-height: 1;
        margin: 16px 0;
    }

    /* Decision Badges */
    .velmak-decision-badge {
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

    .velmak-approved {
        background-color: var(--bbva-success);
        color: white;
        box-shadow: 0 6px 20px rgba(72, 174, 100, 0.4);
    }

    .velmak-approved:hover {
        background-color: #3A8F52;
        transform: translateY(-2px);
    }

    .velmak-rejected {
        background-color: var(--bbva-danger);
        color: white;
        box-shadow: 0 6px 20px rgba(218, 56, 81, 0.4);
    }

    .velmak-rejected:hover {
        background-color: #C52F41;
        transform: translateY(-2px);
    }

    /* SHAP Plot */
    .velmak-shap-plot {
        background-color: var(--bbva-white);
        border-radius: var(--bbva-border-radius);
        padding: 28px;
        box-shadow: var(--bbva-shadow-sm);
        border: 1px solid var(--bbva-border-light);
    }

    /* Form Sections */
    .velmak-form-section {
        background-color: var(--bbva-white);
        border-radius: var(--bbva-border-radius);
        padding: 28px;
        box-shadow: var(--bbva-shadow-sm);
        border: 1px solid var(--bbva-border-light);
        margin-bottom: 20px;
    }

    .velmak-form-section h3 {
        color: var(--bbva-navy);
        font-size: 1.25rem;
        font-weight: 600;
        margin-bottom: 20px;
        padding-bottom: 12px;
        border-bottom: 2px solid var(--bbva-aqua);
    }

    /* Plot Containers */
    .velmak-plot-container {
        background-color: var(--bbva-white);
        border-radius: var(--bbva-border-radius);
        padding: 28px;
        box-shadow: var(--bbva-shadow-sm);
        border: 1px solid var(--bbva-border-light);
    }

    /* Botones personalizados */
    .stButton > button {
        background-color: var(--bbva-core-blue) !important;
        color: white !important;
        border-radius: var(--bbva-border-radius) !important;
        font-weight: 600 !important;
        padding: 14px 28px !important;
        border: none !important;
        box-shadow: var(--bbva-shadow-sm) !important;
        transition: all 0.2s ease !important;
        font-size: 1rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }

    .stButton > button:hover {
        background-color: var(--bbva-aqua) !important;
        transform: translateY(-1px) !important;
        box-shadow: var(--bbva-shadow-md) !important;
    }

    /* Títulos de sección */
    .velmak-section-title {
        font-size: 1.75rem;
        font-weight: 700;
        color: var(--bbva-navy);
        margin-bottom: 32px;
        display: flex;
        align-items: center;
        gap: 16px;
        padding-bottom: 16px;
        border-bottom: 2px solid var(--bbva-aqua);
    }

    /* Spinner personalizado */
    .velmak-spinner {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 48px;
        background-color: var(--bbva-white);
        border-radius: var(--bbva-border-radius);
        box-shadow: var(--bbva-shadow-sm);
        border: 2px solid var(--bbva-aqua);
    }

    .velmak-spinner-animation {
        width: 48px;
        height: 48px;
        border: 4px solid var(--bbva-border-light);
        border-top: 4px solid var(--bbva-aqua);
        border-radius: 50%;
        animation: velmak-spin 1s linear infinite;
    }

    @keyframes velmak-spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    .velmak-spinner-text {
        margin-left: 16px;
        color: var(--bbva-navy);
        font-weight: 600;
        font-size: 1.125rem;
    }

    /* Tablas de datos */
    .velmak-data-table {
        width: 100%;
        border-collapse: collapse;
        margin: 16px 0;
        font-size: 0.875rem;
    }

    .velmak-data-table th,
    .velmak-data-table td {
        padding: 12px;
        text-align: left;
        border-bottom: 1px solid var(--bbva-border-light);
    }

    .velmak-data-table th {
        background-color: rgba(0, 71, 133, 0.05);
        font-weight: 600;
        color: var(--bbva-navy);
    }

    /* Ocultar elementos por defecto de Streamlit */
    .stDeployButton, .stHeader, .stToolbar {
        display: none !important;
    }

    /* Métricas personalizadas */
    .stMetric {
        background-color: var(--bbva-white) !important;
        border: 1px solid var(--bbva-border-light) !important;
        border-radius: var(--bbva-border-radius) !important;
        padding: 20px !important;
        box-shadow: var(--bbva-shadow-sm) !important;
        transition: all 0.3s ease !important;
    }

    .stMetric:hover {
        transform: translateY(-2px) !important;
        box-shadow: var(--bbva-shadow-md) !important;
    }

    .stMetric > div > div > div > div {
        color: var(--bbva-navy) !important;
        font-weight: 600 !important;
    }

    .stMetric > div > div > div > div > div {
        color: var(--bbva-core-blue) !important;
        font-weight: 800 !important;
    }

    /* Inputs personalizados */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > div,
    .stSlider > div > div > div {
        border-radius: var(--bbva-border-radius) !important;
        border: 1px solid var(--bbva-border-light) !important;
    }

    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div > div:focus {
        border-color: var(--bbva-aqua) !important;
        box-shadow: 0 0 0 2px rgba(2, 132, 132, 0.2) !important;
    }

    /* DataFrames */
    .dataframe {
        border: none !important;
    }

    .dataframe th {
        border: none !important;
        background-color: rgba(0, 71, 133, 0.05) !important;
        color: var(--bbva-navy) !important;
        font-weight: 600 !important;
    }

    .dataframe td {
        border: none !important;
        border-bottom: 1px solid var(--bbva-border-light) !important;
    }

    /* Footer */
    .velmak-footer {
        text-align: center;
        color: var(--bbva-text-secondary);
        padding: 32px 24px;
        border-top: 1px solid var(--bbva-border-light);
        margin-top: 48px;
        background-color: var(--bbva-white);
        border-radius: var(--bbva-border-radius);
        box-shadow: var(--bbva-shadow-sm);
    }
    </style>
    """, unsafe_allow_html=True)

# Funciones de datos simulados
def generate_dashboard_data():
    """Genera datos simulados para el dashboard PFM VELMAK"""
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    
    # KPIs actuales
    kpis = {
        'approval_rate': {'value': 89.7, 'change': 2.4, 'unit': '%'},
        'npl_rate': {'value': 3.2, 'change': -0.8, 'unit': '%'},
        'volume': {'value': 24850, 'change': 18.7, 'unit': 'peticiones'},
        'psi': {'value': 0.08, 'change': -0.02, 'unit': 'PSI'}
    }
    
    # Datos temporales para gráficos
    risk_data = pd.DataFrame({
        'date': dates,
        'risk_score': np.random.normal(720, 65, 30),
        'approval_rate': np.random.normal(88, 5, 30),
        'npl_rate': np.random.normal(3.5, 0.8, 30)
    })
    
    # Datos de distribución
    risk_dist = pd.DataFrame({
        'category': ['Riesgo Bajo', 'Riesgo Medio-Bajo', 'Riesgo Medio', 'Riesgo Medio-Alto', 'Riesgo Alto'],
        'count': [520, 380, 240, 85, 35],
        'percentage': [42.8, 31.3, 19.7, 7.0, 2.9]
    })
    
    return kpis, risk_data, risk_dist

def simulate_scoring(traditional_data, alternative_data):
    """Simula proceso de scoring con experiencia PFM VELMAK"""
    
    # Simulación con spinner personalizado
    with st.container():
        st.markdown("""
        <div class="velmak-spinner">
            <div class="velmak-spinner-animation"></div>
            <div class="velmak-spinner-text">Ejecutando modelo analítico...</div>
        </div>
        """, unsafe_allow_html=True)
    
    progress_bar = st.progress(0)
    
    steps = [
        "Validando identidad del cliente...",
        "Analizando datos tradicionales...",
        "Procesando datos alternativos...",
        "Ejecutando modelo de IA explicable...",
        "Calculando explicabilidad de variables...",
        "Generando decisión final..."
    ]
    
    for i, step in enumerate(steps):
        progress_bar.progress((i + 1) / len(steps))
        time.sleep(0.5)
        st.markdown(f"""
        <div class="velmak-spinner">
            <div class="velmak-spinner-animation"></div>
            <div class="velmak-spinner-text">{step}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Calcular score PFM VELMAK
    base_score = 600
    
    # Contribución datos tradicionales (60% peso)
    income_score = min(200, traditional_data['monthly_income'] / 30)
    employment_score = 150 if traditional_data['employment_verified'] else 0
    credit_score = 120 if traditional_data['credit_history'] == 'Excelente' else 80 if traditional_data['credit_history'] == 'Bueno' else 40
    age_score = min(50, (traditional_data['age'] - 25) * 2)
    
    # Contribución datos alternativos (40% peso)
    balance_score = min(100, alternative_data['account_balance'] / 150)
    transaction_score = min(80, alternative_data['transaction_count'] * 1.5)
    digital_score = min(60, alternative_data['digital_score'] * 0.6)
    stability_score = min(60, alternative_data['stability_months'] * 2)
    
    final_score = base_score + income_score + employment_score + credit_score + age_score + \
                 balance_score + transaction_score + digital_score + stability_score
    
    final_score = min(1000, max(0, final_score))
    
    # Decisión PFM VELMAK
    approved = final_score >= 700
    
    # Explicación SHAP simulada
    shap_explanation = {
        'account_balance': {'value': alternative_data['account_balance'], 'impact': 85, 'direction': 'positive'},
        'monthly_income': {'value': traditional_data['monthly_income'], 'impact': 120, 'direction': 'positive'},
        'employment_verified': {'value': traditional_data['employment_verified'], 'impact': 150, 'direction': 'positive'},
        'credit_history': {'value': traditional_data['credit_history'], 'impact': 120, 'direction': 'positive'},
        'digital_score': {'value': alternative_data['digital_score'], 'impact': 45, 'direction': 'positive'},
        'transaction_count': {'value': alternative_data['transaction_count'], 'impact': 35, 'direction': 'positive'},
        'stability_months': {'value': alternative_data['stability_months'], 'impact': 25, 'direction': 'positive'}
    }
    
    return final_score, approved, shap_explanation

def create_kpi_card(title, value, change, unit, icon):
    """Crea tarjeta KPI personalizada"""
    change_class = "velmak-positive" if change > 0 else "velmak-negative"
    change_symbol = "↑" if change > 0 else "↓"
    
    return f"""
    <div class="velmak-kpi-card">
        <div class="velmak-kpi-label">{icon} {title}</div>
        <div class="velmak-kpi-value">{value:,}{unit}</div>
        <div class="velmak-kpi-change {change_class}">
            {change_symbol} {abs(change)}{unit}
        </div>
    </div>
    """

def create_shap_plot(shap_data):
    """Crea gráfico SHAP personalizado"""
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
        hovertemplate='<b>%{y}</b><br>Impacto: %{x:.0f} puntos<extra></extra>'
    ))
    
    fig.update_layout(
        title="Explicabilidad de Variables - PFM VELMAK",
        xaxis_title="Impacto en Score (puntos)",
        yaxis_title="Variables Analizadas",
        height=450,
        margin=dict(l=20, r=20, t=40, b=20),
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#072146', family='Inter')
    )
    
    return fig

# Sidebar PFM VELMAK
st.sidebar.markdown("""
# 🏦 PFM VELMAK
## Sistema de Scoring Financiero
### Inteligencia Artificial Explicable
""", unsafe_allow_html=True)

page = st.sidebar.selectbox(
    "Navegación",
    ["📊 Dashboard Directivo", "🔍 Simulador de Scoring"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
**Versión:** 3.0.0  
**Entorno:** Producción  
**Estado:** Activo  
**Cumplimiento:** GDPR & AI Act  
**Modelo:** VELMAK-2024
""")

# Vista 1: Dashboard Directivo PFM VELMAK
if page == "📊 Dashboard Directivo":
    st.markdown('<div class="velmak-section-title">📊 Dashboard Directivo PFM VELMAK</div>', unsafe_allow_html=True)
    
    # Generar datos
    kpis, risk_data, risk_dist = generate_dashboard_data()
    
    # KPIs principales con st.metric personalizado
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Tasa de Aprobación",
            f"{kpis['approval_rate']['value']}%",
            f"{kpis['approval_rate']['change']:+.1f}%",
            delta_color="normal"
        )
    
    with col2:
        st.metric(
            "Tasa de Morosidad",
            f"{kpis['npl_rate']['value']}%",
            f"{kpis['npl_rate']['change']:+.1f}%",
            delta_color="inverse"
        )
    
    with col3:
        st.metric(
            "Volumen de Peticiones",
            f"{kpis['volume']['value']:,}",
            f"{kpis['volume']['change']:+.1f}%",
            delta_color="normal"
        )
    
    with col4:
        st.metric(
            "Population Stability",
            f"{kpis['psi']['value']:.3f}",
            f"{kpis['psi']['change']:+.3f}",
            delta_color="inverse"
        )
    
    st.markdown("---")
    
    # Gráficos interactivos
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="velmak-plot-container">', unsafe_allow_html=True)
        fig_trend = go.Figure()
        
        fig_trend.add_trace(go.Scatter(
            x=risk_data['date'],
            y=risk_data['risk_score'],
            mode='lines+markers',
            name='Score de Riesgo Promedio',
            line=dict(color='#004481', width=3),
            marker=dict(size=6, color='#004481')
        ))
        
        fig_trend.add_trace(go.Scatter(
            x=risk_data['date'],
            y=risk_data['approval_rate'] * 8,
            mode='lines+markers',
            name='Tasa de Aprobación (x8)',
            line=dict(color='#48AE64', width=3, dash='dash'),
            marker=dict(size=6, color='#48AE64')
        ))
        
        fig_trend.update_layout(
            title="Evolución del Riesgo Crediticio - PFM VELMAK",
            xaxis_title="Fecha",
            yaxis_title="Valor",
            height=400,
            margin=dict(l=20, r=20, t=40, b=20),
            legend=dict(x=0, y=1, bgcolor='rgba(255,255,255,0.9)'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#072146', family='Inter')
        )
        
        st.plotly_chart(fig_trend, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="velmak-plot-container">', unsafe_allow_html=True)
        fig_risk = go.Figure(data=[go.Pie(
            labels=risk_dist['category'],
            values=risk_dist['count'],
            hole=0.4,
            marker_colors=['#48AE64', '#028484', '#F7893B', '#F4F4F4', '#DA3851'],
            textinfo='label+percent',
            textposition='outside',
            hovertemplate='<b>%{label}</b><br>Cantidad: %{value}<br>Porcentaje: %{percent}<extra></extra>'
        )])
        
        fig_risk.update_layout(
            title="Distribución de Nivel de Riesgo",
            height=400,
            margin=dict(l=20, r=20, t=40, b=20),
            showlegend=True,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#072146', family='Inter')
        )
        
        st.plotly_chart(fig_risk, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Vista 2: Simulador de Scoring PFM VELMAK
elif page == "🔍 Simulador de Scoring":
    st.markdown('<div class="velmak-section-title">🔍 Simulador de Scoring - PFM VELMAK</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Formulario de datos tradicionales
        st.markdown('<div class="velmak-form-section">', unsafe_allow_html=True)
        st.markdown('<h3>📋 Datos Tradicionales</h3>', unsafe_allow_html=True)
        
        traditional_data = {
            'monthly_income': st.number_input("Ingreso Mensual (€)", min_value=0, max_value=50000, value=5500, step=100),
            'employment_verified': st.checkbox("Verificación de Empleo", value=True),
            'credit_history': st.selectbox("Historial Crediticio", ["Excelente", "Bueno", "Regular", "Malo"], index=0),
            'existing_debts': st.number_input("Deudas Existentes (€)", min_value=0, max_value=200000, value=12000, step=500),
            'age': st.number_input("Edad", min_value=18, max_value=100, value=42, step=1)
        }
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Formulario de datos alternativos
        st.markdown('<div class="velmak-form-section">', unsafe_allow_html=True)
        st.markdown('<h3>📱 Datos Alternativos</h3>', unsafe_allow_html=True)
        
        alternative_data = {
            'account_balance': st.number_input("Saldo Promedio (€)", min_value=0, max_value=200000, value=8500, step=100),
            'transaction_count': st.number_input("Transacciones Mensuales", min_value=0, max_value=500, value=68, step=1),
            'digital_score': st.number_input("Score Digital (0-100)", min_value=0, max_value=100, value=75, step=1),
            'stability_months': st.number_input("Meses de Estabilidad", min_value=0, max_value=120, value=36, step=1),
            'credit_utilization': st.slider("Utilización de Crédito", 0.0, 1.0, 0.32, 0.05)
        }
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Botón de evaluación
        if st.button("🚀 Evaluar con PFM VELMAK", type="primary", use_container_width=True):
            score, approved, shap_explanation = simulate_scoring(traditional_data, alternative_data)
            
            st.session_state.score = score
            st.session_state.approved = approved
            st.session_state.shap_explanation = shap_explanation
            st.session_state.traditional_data = traditional_data
            st.session_state.alternative_data = alternative_data
    
    with col2:
        # Resultados del scoring
        if 'score' in st.session_state:
            # Score Display
            st.markdown('<div class="velmak-score-display">', unsafe_allow_html=True)
            st.markdown(f'<div class="velmak-score-value">{st.session_state.score}</div>', unsafe_allow_html=True)
            st.markdown(f'<div style="font-size: 1.2rem; color: var(--bbva-text-secondary); margin-bottom: 16px;">Score PFM VELMAK (0-1000)</div>', unsafe_allow_html=True)
            
            if st.session_state.approved:
                st.markdown('<div class="velmak-decision-badge velmak-approved">✅ CRÉDITO APROBADO</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="velmak-decision-badge velmak-rejected">❌ CRÉDITO DENEGADO</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Explicación SHAP
            st.markdown('<div class="velmak-shap-plot">', unsafe_allow_html=True)
            st.markdown('<h4 style="color: var(--bbva-navy); margin-bottom: 20px;">🔍 Explicabilidad de Variables</h4>', unsafe_allow_html=True)
            
            shap_fig = create_shap_plot(st.session_state.shap_explanation)
            st.plotly_chart(shap_fig, use_container_width=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Resumen de decisión
            st.markdown('<div class="velmak-form-section">', unsafe_allow_html=True)
            st.markdown('<h4>📊 Resumen de Decisión</h4>', unsafe_allow_html=True)
            
            # Tabla de factores
            factors_data = []
            for feature, data in st.session_state.shap_explanation.items():
                direction_icon = "↗️" if data['direction'] == 'positive' else "↘️"
                direction_color = "#48AE64" if data['direction'] == 'positive' else "#DA3851"
                
                # Formatear valor según tipo de dato
                if isinstance(data['value'], bool):
                    valor_formateado = "Sí" if data['value'] else "No"
                elif isinstance(data['value'], str):
                    valor_formateado = data['value']
                else:
                    valor_formateado = f"{data['value']:,.2f}"
                
                factors_data.append({
                    'Variable': feature.replace('_', ' ').title(),
                    'Valor': valor_formateado,
                    'Impacto': f"{data['impact']:+.0f} pts",
                    'Dirección': f"{direction_icon} {data['direction'].title()}"
                })
            
            factors_df = pd.DataFrame(factors_data)
            st.dataframe(factors_df, hide_index=True, use_container_width=True)
            
            # Explicación en texto
            if st.session_state.approved:
                st.markdown("""
                <div style="background-color: rgba(72, 174, 100, 0.1); padding: 20px; border-radius: 8px; border-left: 4px solid #48AE64; margin: 20px 0;">
                    <strong>✅ Decisión Favorable:</strong> El perfil del cliente cumple con los estándares de PFM VELMAK para aprobación de crédito. 
                    Los factores positivos superan significativamente a los factores de riesgo, demostrando la capacidad predictiva del modelo.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="background-color: rgba(218, 56, 81, 0.1); padding: 20px; border-radius: 8px; border-left: 4px solid #DA3851; margin: 20px 0;">
                    <strong>❌ Decisión Desfavorable:</strong> El perfil del cliente no cumple actualmente con los criterios de aprobación de PFM VELMAK.
                    Se recomienda mejorar los aspectos identificados antes de una nueva evaluación.
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

# Footer PFM VELMAK
st.markdown("---")
st.markdown("""
<div class="velmak-footer">
    <strong>PFM VELMAK - Sistema de Scoring Financiero</strong><br>
    <small>© 2024 Proyecto Fin de Máster | Inteligencia Artificial Explicable</small><br>
    <small style="color: var(--bbva-aqua);">Cumplimiento GDPR & AI Act | Modelo Certificado</small>
</div>
""", unsafe_allow_html=True)

# Cargar CSS personalizado
load_custom_css()
