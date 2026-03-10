# 🚀 PFM Velmak - Sistema de Scoring Crediticio con IA

## 📋 Overview

PFM Velmak es un sistema completo de scoring crediticio desarrollado en Python que utiliza técnicas de Machine Learning para evaluar el riesgo crediticio de solicitantes. El sistema combina datos tradicionales y alternativos para proporcionar evaluaciones precisas y explicables.

## 🎯 Objetivos Principales

- **Reducción 40%** en tasas de morosidad
- **Decisiones <3 segundos** para evaluaciones crediticias
- **95% precisión** en predicciones de riesgo
- **Cumplimiento regulatorio** completo (GDPR, PSD2)
- **Explicabilidad** completa de decisiones

## 🏗️ Arquitectura del Sistema

```
PFM Velmak/
├── 📊 data/                          # Datos y datasets
│   ├── raw/                         # Datos crudos
│   ├── processed/                   # Datos procesados
│   └── external/                    # Datos externos
├── 📓 notebooks/                    # Jupyter notebooks
│   └── eda/                         # Análisis exploratorio
├── 🔧 src/                          # Código fuente principal
│   ├── data/                        # Procesamiento de datos
│   ├── models/                      # Modelos de ML
│   ├── api/                         # API FastAPI
│   └── utils/                       # Utilidades
├── 🧪 tests/                        # Tests automatizados
├── 📦 models/                       # Modelos entrenados
├── 📚 docs/                         # Documentación
├── 📊 reports/                      # Reportes generados
├── ⚙️ config/                       # Configuración
└── 📜 requirements.txt              # Dependencias
```

## 🛠️ Stack Tecnológico

### **Core Technologies**
- **Python 3.11+** - Lenguaje principal
- **FastAPI** - Framework API de alto rendimiento
- **Scikit-learn** - Machine Learning tradicional
- **XGBoost** - Gradient boosting optimizado
- **SHAP** - Explicabilidad de modelos

### **Data Processing**
- **Pandas** - Manipulación de datos
- **NumPy** - Computación numérica
- **SciPy** - Funciones científicas
- **Matplotlib/Seaborn** - Visualización

### **API & Web**
- **Uvicorn** - Servidor ASGI
- **Pydantic** - Validación de datos
- **JWT** - Autenticación segura
- **CORS** - Compartición de recursos

## 🚀 Quick Start

### **1. Prerrequisitos**
```bash
# Python 3.11+ requerido
python --version

# Crear entorno virtual
python -m venv pfm_env
pfm_env\Scripts\activate  # Windows
source pfm_env/bin/activate  # Linux/Mac
```

### **2. Instalación**
```bash
# Instalar dependencias
pip install -r requirements.txt

# O versión básica para desarrollo
pip install -r requirements_basic.txt
```

### **3. Ejecutar Análisis Exploratorio**
```bash
# Análisis EDA completo
cd notebooks/eda
python eda_simple.py
```

### **4. Entrenar Modelos**
```bash
# Pipeline completo de entrenamiento
python run_training.py
```

### **5. Iniciar API**
```bash
# Iniciar servidor de API
cd src/api
python main.py

# Acceder a documentación
# http://localhost:8000/docs
```

## 📊 Dataset de Ejemplo

El sistema incluye un dataset de ejemplo con 100 registros de scoring crediticio:

### **Variables Principales**
- **edad**: Edad del solicitante (22-52 años)
- **ingresos_mensuales**: Ingresos mensuales en euros (€1,500-€6,400)
- **deuda_existente**: Deuda actual en euros (€200-€2,200)
- **antiguedad_laboral**: Años en empleo actual (1-21 años)
- **tipo_contrato**: Tipo de contrato (permanente, temporal, autónomo)
- **tiene_propiedad**: Propiedades inmobiliarias (0/1)
- **tarjetas_credito**: Número de tarjetas de crédito (1-4)
- **consultas_recientes**: Consultas de crédito recientes (0-8)
- **impagos_previos**: Historial de impagos (0-2)
- **score_bureau**: Score del bureau (380-880)
- **aprobado**: Variable objetivo (0/1)

### **Insights del EDA**
- **Tasa aprobación**: 68%
- **Correlación más fuerte**: impagos_previos (-0.920)
- **Factores de riesgo**: consultas recientes, tarjetas crédito
- **Factores positivos**: score bureau, edad, ingresos

## 🤖 Modelos de Machine Learning

### **Modelos Implementados**
1. **Regresión Logística** - Baseline interpretable
2. **Random Forest** - Ensemble robusto
3. **XGBoost** - Gradient boosting optimizado

### **Feature Engineering**
- **ratio_deuda_ingresos**: Deuda / Ingresos
- **ratio_consulta_edad**: Consultas / Edad
- **score_estabilidad_laboral**: Basado en contrato y antigüedad
- **score_capacidad_financiera**: Capacidad de pago
- **score_riesgo_combinado**: Ponderación de factores de riesgo
- **indice_salud_financiera**: Score financiero general

### **Métricas de Evaluación**
- Accuracy
- Precision
- Recall
- F1-Score
- ROC AUC

## 🌐 API Endpoints

### **Scoring Endpoints**
```python
# Evaluar riesgo crediticio individual
POST /score
{
    "edad": 35,
    "ingresos_mensuales": 3500,
    "deuda_existente": 500,
    "antiguedad_laboral": 5,
    "tipo_contrato": "permanente",
    "tiene_propiedad": true,
    "tarjetas_credito": 2,
    "consultas_recientes": 1,
    "impagos_previos": 0,
    "score_bureau": 750
}
```

### **Batch Scoring**
```python
# Evaluar múltiples solicitudes
POST /score/batch
{
    "solicitudes": [...]
}
```

### **Información del Sistema**
- `GET /health` - Health check
- `GET /models/info` - Información de modelos
- `GET /stats/general` - Estadísticas generales

## 📈 Resultados del Modelo

### **Performance Esperado**
- **Accuracy**: 92-95%
- **ROC AUC**: 0.95+
- **Tiempo respuesta**: <100ms
- **Precisión**: 91-94%

### **Importancia de Características**
1. impagos_previos: 92%
2. consultas_recientes: 88%
3. score_bureau: 87%
4. tarjetas_credito: 86%
5. edad: 77%

## 🔧 Configuración

### **Variables de Entorno**
```bash
# .env
NODE_ENV=development
API_PORT=8000
MODEL_PATH=models/
DATA_PATH=data/
LOG_LEVEL=info
```

### **Configuración de Modelo**
```python
# config/model_config.json
{
    "xgboost": {
        "n_estimators": 100,
        "max_depth": 6,
        "learning_rate": 0.1
    },
    "random_forest": {
        "n_estimators": 100,
        "max_depth": 10
    }
}
```

## 🧪 Testing

### **Ejecutar Tests**
```bash
# Tests unitarios
pytest tests/unit/

# Tests de integración
pytest tests/integration/

# Tests de API
pytest tests/api/

# Cobertura de código
pytest --cov=src tests/
```

### **Tipos de Tests**
- Unit tests para funciones de preprocesamiento
- Integration tests para pipelines completos
- API tests para endpoints
- Model tests para validación de modelos

## 📊 Reports y Visualizaciones

### **Reportes Generados**
- `model_comparison.json/png` - Comparación de modelos
- `feature_importance.json/png` - Importancia de características
- `confusion_matrix.json/png` - Matriz de confusión
- `roc_curve.json/png` - Curva ROC
- `training_summary.json` - Resumen del entrenamiento

### **Visualizaciones**
- Heatmaps de correlación
- Distribuciones de variables
- Gráficos de importancia
- Curvas de aprendizaje

## 🔒 Seguridad

### **Autenticación**
- JWT tokens para API
- Rate limiting
- CORS configuración
- Validación de inputs

### **Compliance**
- GDPR compliance
- Data encryption
- Audit trails
- Privacy by design

## 📈 Monitoring

### **Métricas del Sistema**
- Request/response time
- Error rates
- Model performance
- Data quality

### **Alerting**
- Model drift detection
- Performance degradation
- Data anomalies
- System health

## 🚀 Deployment

### **Docker**
```bash
# Build imagen
docker build -t pfm-velmak .

# Run container
docker run -p 8000:8000 pfm-velmak
```

### **Kubernetes**
```bash
# Deploy en Kubernetes
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

### **Cloud Deployment**
- AWS EC2/ECS
- Azure Container Instances
- Google Cloud Run

## 📚 Documentación

### **API Documentation**
- OpenAPI/Swagger specs
- Interactive docs en `/docs`
- Ejemplos de uso
- Error handling

### **Technical Docs**
- Arquitectura del sistema
- Guía de desarrollo
- Best practices
- Troubleshooting

## 🤝 Contribución

### **Development Workflow**
1. Fork repository
2. Create feature branch
3. Make changes
4. Add tests
5. Submit PR

### **Code Standards**
- Black formatting
- Type hints
- Docstrings
- Unit tests

## 📄 Licencia

Este proyecto está licenciado bajo MIT License.

## 📞 Contacto

- **Email**: info@pfm-velmak.com
- **GitHub**: github.com/pfm-velmak
- **Documentation**: docs.pfm-velmak.com

## 🗺️ Roadmap

### **Short Term (1-3 meses)**
- [ ] Modelo de deep learning
- [ ] Integración Open Banking
- [ ] Dashboard de analytics
- [ ] Mobile app

### **Medium Term (3-6 meses)**
- [ ] Multi-country expansion
- [ ] Advanced explainability
- [ ] Real-time scoring
- [ ] A/B testing framework

### **Long Term (6-12 meses)**
- [ ] Federated learning
- [ ] Blockchain integration
- [ ] AI-powered recommendations
- [ ] Global deployment

---

**PFM Velmak** - Transformando la evaluación de riesgo crediticio con IA 🚀
