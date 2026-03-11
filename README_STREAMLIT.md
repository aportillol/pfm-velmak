# PFM VELMAK - Aplicación Web Demo

## 🏦 Descripción

Aplicación web MVP del sistema de scoring financiero PFM VELMAK, desarrollada con Streamlit y diseño UI/UX profesional. La aplicación demuestra las capacidades de scoring basado en datos alternativos con Inteligencia Artificial explicable.

## ✨ Características Principales

### 📊 Dashboard Directivo
- **KPIs en tiempo real**: Tasa de aprobación, NPL, volumen API, PSI
- **Visualizaciones interactivas**: Evolución temporal, distribución de riesgo
- **Diseño responsivo**: Adaptado para desktop y móvil
- **Actualización automática**: Datos simulados con refresh dinámico

### 🔍 Evaluador de Crédito
- **Formulario por pasos**: Datos tradicionales vs alternativos
- **Simulación de IA**: Procesamiento con estados de carga animados
- **Score explicativo**: Visualización SHAP con contribución de variables
- **Decisiones transparentes**: Cumplimiento AI Act y GDPR

### 📈 Análisis de Riesgos
- **Monitoreo de drift**: Population Stability Index por variable
- **Métricas de rendimiento**: Precisión, recall, F1-score, ROC-AUC
- **Análisis de sesgos**: Equidad algorítmica por segmentos demográficos
- **Control de versiones**: Comparación de modelos históricos

## 🎨 Diseño UI/UX

### Paleta de Colores
- **Principal**: Azul Marino (#1e3a5f) - Confianza y estabilidad
- **Secundario**: Gris Medio (#4a5568) - Neutralidad profesional
- **Acento**: Verde Esmeralda (#10b981) - Aprobaciones y métricas positivas
- **Fondo**: Off-white (#f8fafc) - Claridad y legibilidad
- **Alertas**: Rojo (#ef4444) - Riesgos y rechazos

### Tipografía
- **Principal**: Inter (sans-serif moderna)
- **Jerarquía clara**: Títulos grandes, subtítulos atenuados
- **Peso visual**: Negritas estratégicas para reducir carga cognitiva

### Componentes UI
- **Tarjetas KPI**: Con sombras suaves y hover effects
- **Formularios**: Agrupados lógicamente con validación en tiempo real
- **Gráficos**: Minimalistas, data-ink ratio optimizado
- **Loading states**: Indicadores visuales durante procesamiento

## 🚀 Instalación y Ejecución

### Prerrequisitos
- Python 3.8+
- pip instalado

### Instalación
```bash
# Clonar el repositorio
git clone <repositorio-url>
cd pfm-velmak-demo

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt
```

### Ejecución
```bash
# Iniciar aplicación
streamlit run streamlit_app.py

# Acceder en navegador
# http://localhost:8501
```

## 📱 Estructura de la Aplicación

### Navegación Principal
1. **Dashboard Directivo**: Vista ejecutiva con KPIs y métricas
2. **Evaluador de Crédito**: Simulador interactivo con IA explicable
3. **Análisis de Riesgos**: Monitoreo avanzado y control de calidad

### Flujo de Usuario

#### Dashboard Directivo
```
Usuario accede → Visualiza KPIs principales → Explora gráficos interactivos → Filtra por período/segmento → Exporta reportes
```

#### Evaluador de Crédito
```
Usuario ingresa datos tradicionales → Completa datos alternativos → Presiona "Evaluar" → Ve animación de procesamiento → Recibe score + explicación → Analiza contribución variables
```

#### Análisis de Riesgos
```
Usuario selecciona filtros → Visualiza PSI por variable → Analiza métricas de rendimiento → Revisa equidad algorítmica → Compara versiones de modelo
```

## 🔧 Arquitectura Técnica

### Stack Tecnológico
- **Frontend**: Streamlit (Python)
- **Visualizaciones**: Plotly (gráficos interactivos)
- **Procesamiento**: Pandas + NumPy
- **Estilos**: CSS personalizado con variables CSS
- **Diseño**: Mobile-first, responsive design

### Componentes Principales
- **KPI Cards**: Componentes reutilizables con animaciones
- **SHAP Plot**: Visualización personalizada de explicabilidad
- **Data Simulator**: Generación de datos realistas para demo
- **Loading States**: Indicadores de progreso con texto descriptivo

## 📊 Métricas y KPIs

### Dashboard Directivo
- **Tasa de Aprobación**: Porcentaje de créditos aprobados
- **NPL Rate**: Tasa de morosidad a 90 días
- **API Volume**: Volumen de peticiones mensuales
- **PSI Score**: Population Stability Index para drift detection

### Evaluador de Crédito
- **Credit Score**: Puntuación 0-1000 con IA explicable
- **Decision Logic**: Aprobado/Denegado con umbral configurable
- **Feature Importance**: Contribución de cada variable al score
- **Compliance Indicators**: Estado de cumplimiento GDPR/AI Act

### Análisis de Riesgos
- **Model Performance**: Métricas de clasificación
- **Bias Analysis**: Equidad por segmentos demográficos
- **Drift Detection**: PSI por variable con alertas
- **Version Control**: Comparación histórica de modelos

## 🎯 Casos de Uso

### Para Instituciones Financieras
- **Evaluación rápida**: Procesamiento en segundos vs días tradicionales
- **Transparencia regulatoria**: Cumplimiento GDPR y AI Act
- **Reducción de sesgos**: IA explicable para decisiones justas
- **Eficiencia operativa**: Automatización de procesos manuales

### Para Analistas de Riesgo
- **Visualización interactiva**: Exploración detallada de métricas
- **Control de calidad**: Monitoreo continuo del modelo
- **Análisis de impacto**: Evaluación de cambios en el modelo
- **Reportes automáticos**: Generación de informes regulatorios

### Para Equipos de Desarrollo
- **Testing de modelos**: Simulación de diferentes escenarios
- **Debugging visual**: Identificación de problemas en datos
- **Validación de features**: Evaluación de nuevas variables
- **Documentación viva**: Ejemplos de uso y resultados

## 🔒 Seguridad y Privacidad

### Cumplimiento Regulatorio
- **GDPR Compliant**: Diseño privacy-by-default
- **AI Act Ready**: Explicabilidad algorítmica integrada
- **Data Minimization**: Solo datos necesarios para scoring
- **Right to Explanation**: SHAP para transparencia completa

### Medidas de Seguridad
- **Input Validation**: Validación de todos los datos de entrada
- **Output Sanitization**: Limpieza de respuestas sensibles
- **Session Management**: Manejo seguro de estados de usuario
- **Error Handling**: Manejo elegante de excepciones

## 🚀 Mejoras Futuras

### Short Term (1-3 meses)
- [ ] Integración con APIs reales de Open Banking
- [ ] Base de datos persistente para historial
- [ ] Autenticación de usuarios y roles
- [ ] Exportación de reportes en PDF/Excel

### Medium Term (3-6 meses)
- [ ] Machine Learning en tiempo real
- [ ] Dashboard personalizable por usuario
- [ ] Alertas automáticas por email/SMS
- [ ] Integración con sistemas core bancarios

### Long Term (6-12 meses)
- [ ] IA conversacional para soporte
- [ ] Análisis predictivo de tendencias
- [ ] Gamificación para educación financiera
- [ ] Expansión a múltiples mercados

## 📞 Soporte y Contacto

### Documentación Técnica
- **API Documentation**: Endpoints y formatos de datos
- **Model Documentation**: Arquitectura y algoritmos
- **Deployment Guide**: Instrucciones de producción
- **Troubleshooting**: Problemas comunes y soluciones

### Equipo de Desarrollo
- **Product Manager**: Estrategia de producto y roadmap
- **UI/UX Designer**: Experiencia de usuario y accesibilidad
- **Data Scientist**: Modelos de ML y explicabilidad
- **Full Stack Developer**: Arquitectura y despliegue

---

**PFM VELMAK** © 2024 - Transformando el scoring financiero con IA explicable y datos alternativos
