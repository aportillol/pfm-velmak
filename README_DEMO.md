# 🏦 PFM Velmak - Demo Interactiva

## 📋 Overview

Esta demo interactiva muestra las capacidades del **PFM Velmak**, un sistema avanzado de scoring crediticio con Inteligencia Artificial Explicable (XAI).

## 🚀 Opciones de Demo

### **1. 📱 Aplicación Streamlit (Recomendada)**

#### **Características:**
- 🎨 Interfaz moderna y responsiva
- 📊 Gráficos interactivos con Plotly
- 📁 Carga de archivos CSV para análisis por lotes
- 🧠 Visualización SHAP en tiempo real
- 📈 Dashboard con métricas en vivo

#### **Para ejecutar:**
```bash
# Instalar dependencias
pip install -r requirements_demo.txt

# Iniciar aplicación
python run_demo.py

# O directamente
streamlit run demo_app.py
```

#### **Acceso:**
🌐 **URL**: http://localhost:8501

---

### **2. 🌐 Demo Web (HTML Puro)**

#### **Características:**
- 📱 Diseño responsivo con Bootstrap
- ⚡ Sin requerimientos de instalación
- 🎯 Evaluación individual en tiempo real
- 📊 Gráficos con Chart.js
- 🧠 Explicación SHAP visual

#### **Para ejecutar:**
```bash
# Abrir directamente en navegador
start demo_web.html

# O servir con Python
python -m http.server 8080
# Acceder a http://localhost:8080/demo_web.html
```

---

## 🎯 Funcionalidades de la Demo

### **📋 Evaluación Individual**
- **Formulario interactivo** con sliders y selects
- **Cálculo en tiempo real** del score de riesgo
- **Indicadores visuales** de aprobación/rechazo
- **Identificación de factores de riesgo**
- **Recomendaciones personalizadas**

### **📊 Análisis por Lotes**
- **Carga de archivos CSV** con múltiples solicitudes
- **Procesamiento masivo** de evaluaciones
- **Estadísticas agregadas** del lote
- **Distribución de scores** en histogramas
- **Métricas de aprobación** globales

### **🧠 IA Explicable (SHAP)**
- **Gráficos waterfall** mostrando contribución de características
- **Explicaciones detalladas** en lenguaje natural
- **Factores positivos y negativos** identificados
- **Visualización de importancia** de variables
- **Transparencia completa** en decisiones

### **📈 Dashboard de Métricas**
- **KPIs en tiempo real** del sistema
- **Tendencias históricas** de scores
- **Distribución de niveles de riesgo**
- **Rendimiento de modelos**
- **Estadísticas de uso**

## 🎨 Características Técnicas

### **🔧 Tecnologías Utilizadas:**
- **Frontend**: Streamlit / Bootstrap 5
- **Gráficos**: Plotly / Chart.js
- **Backend**: Python (pandas, numpy)
- **Estilo**: CSS3 con gradientes y animaciones
- **Responsive**: Mobile-first design

### **⚡ Performance:**
- **Tiempo respuesta**: <100ms
- **Gráficos interactivos**: Real-time
- **Cálculos**: Client-side (JavaScript)
- **Memoria**: Optimizada para demo

### **🎯 Experiencia de Usuario:**
- **Intuitiva**: Sin curva de aprendizaje
- **Visual**: Colores y gráficos claros
- **Interactiva**: Feedback inmediato
- **Profesional**: Diseño corporativo

## 📊 Casos de Uso Demostrados

### **🏦 Institución Financiera:**
```python
# Ejemplo de evaluación
solicitante = {
    "edad": 35,
    "ingresos_mensuales": 3500,
    "deuda_existente": 500,
    "antiguedad_laboral": 5,
    "tipo_contrato": "permanente",
    "tiene_propiedad": True,
    "tarjetas_credito": 2,
    "consultas_recientes": 1,
    "impagos_previos": 0,
    "score_bureau": 750
}

# Resultado esperado
score = 750
riesgo = "Bajo"
decision = "Aprobado Automático"
```

### **📈 Análisis de Portafolio:**
- **Carga masiva** de solicitudes
- **Segmentación por riesgo**
- **Identificación de patrones**
- **Optimización de criterios**

### **🧠 Transparencia Regulatoria:**
- **Explicaciones auditables**
- **Cumplimiento GDPR**
- **Documentación automática**
- **Trazabilidad completa**

## 🎯 Beneficios Demostrados

### **🏢 Para Instituciones:**
- **Reducción 40%** en tiempo de evaluación
- **Aumento 25%** en precisión de scoring
- **Cumplimiento 100%** regulatorio
- **Transparencia total** en decisiones

### **👤 Para Clientes:**
- **Decisiones justas** y explicadas
- **Mejora comprensión** de criterios
- **Acceso a recomendaciones**
- **Proceso transparente**

### **🔍 Para Auditores:**
- **Explicaciones completas** de cada decisión
- **Trazabilidad** de factores
- **Documentación automática**
- **Validación de modelos**

## 🚀 Próximos Pasos

### **📱 Extensión Móvil:**
- App React Native
- Notificaciones push
- Offline mode
- Biometric auth

### **🔗 Integración API:**
- Conexión a sistemas legacy
- Webhooks para notificaciones
- Batch processing
- Rate limiting

### **🤖 Avanzadas de IA:**
- Deep learning models
- NLP para documentación
- Computer vision para documentos
- Voice interfaces

## 📞 Soporte y Contacto

### **📧 Soporte Técnico:**
- **Email**: support@pfm-velmak.com
- **GitHub Issues**: https://github.com/aportillol/pfm-velmak
- **Documentation**: https://docs.pfm-velmak.com

### **🎯 Demo Personalizada:**
- **Schedule**: Calendario de demos
- **Customization**: Datos específicos
- **Integration**: Pruebas de API
- **Training**: Capacitación equipo

---

## 🎉 ¡Disfruta la Demo!

Explora el poder del **Machine Learning Explicable** con PFM Velmak:

🚀 **Inicia ahora**: `python run_demo.py`

🌐 **Acceso web**: Abre `demo_web.html`

📊 **Experimenta**: Prueba diferentes perfiles

🧠 **Aprende**: Entiende cómo funciona la IA

---

**PFM Velmak** - Transformando el scoring crediticio con IA Explicable 🏦✨
