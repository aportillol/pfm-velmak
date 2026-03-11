# BBVA Algoritmo de Confianza - Aplicación Web Demo

## 🏦 Descripción

Aplicación web MVP del sistema de scoring financiero "Algoritmo de Confianza" de BBVA, desarrollada con Streamlit y siguiendo el Design System oficial de BBVA. La aplicación demuestra las capacidades de scoring basado en datos alternativos con Inteligencia Artificial explicable, manteniendo la identidad visual y la confianza institucional del banco.

## ✨ Características Principales

### 📊 Dashboard Directivo BBVA
- **KPIs en tiempo real**: Tasa de aprobación, NPL, volumen API, PSI con colores BBVA
- **Visualizaciones corporativas**: Evolución temporal con paleta BBVA
- **Diseño institucional**: Identidad visual BBVA completa
- **Actualización automática**: Datos simulados con refresh dinámico

### 🔍 Evaluador de Crédito BBVA
- **Formulario por pasos**: Datos tradicionales vs alternativos con estilo BBVA
- **Simulación IA BBVA**: Procesamiento con loading animado en colores BBVA
- **Score con branding**: Display BBVA con colores corporativos
- **Decisiones claras**: Aprobado/Denegado con colores BBVA semánticos

### 🎨 BBVA Design System

#### Paleta de Colores Corporativos
- **BBVA Core Blue (#004481)**: Color principal corporativo
- **BBVA Navy (#072146)**: Sidebar, cabeceras, textos principales
- **BBVA Aqua (#028484/#2DCCCD)**: Botones primarios, acentos, progresos
- **BBVA Background (#F4F4F4)**: Fondo limpio institucional
- **BBVA White (#FFFFFF)**: Tarjetas de contenido

#### Colores Semánticos BBVA
- **Success (#48AE64)**: Aprobaciones y métricas positivas
- **Warning (#F7893B)**: Revisión manual, advertencias
- **Danger (#DA3851)**: Rechazos y riesgos críticos
- **Text Secondary (#666666)**: Subtítulos y texto secundario

#### Tipografía y Formas
- **Fuente Inter**: Simulando Benton Sans de BBVA
- **Border-radius ligero**: Elegancia sin exceso de redondeo
- **Sombras sutiles**: Profundidad sin saturación visual
- **Data-Ink Ratio óptimo**: Sin bordes innecesarios en tablas

## 🚀 Instalación y Ejecución

### Prerrequisitos
- Python 3.8+
- pip instalado

### Instalación
```bash
# Clonar repositorio
git clone <repositorio-bbva>
cd bbva-algoritmo-confianza

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
# Iniciar aplicación BBVA
streamlit run bbva_app.py

# Acceder en navegador
http://localhost:8501
```

## 📱 Estructura y Flujo BBVA

### Navegación Principal
1. **Dashboard Directivo**: Vista ejecutiva con KPIs y métricas BBVA
2. **Evaluador de Crédito**: Simulador interactivo con IA explicable BBVA

### Flujo de Usuario BBVA

#### Dashboard Directivo
```
Usuario accede → Visualiza KPIs BBVA → Explora gráficos corporativos → Filtra por período → Exporta reportes BBVA
```

#### Evaluador de Crédito
```
Usuario ingresa datos tradicionales → Completa datos alternativos BBVA → Presiona "Evaluar BBVA" → Ve animación BBVA Aqua → Recibe score con branding BBVA → Analiza explicación SHAP con colores BBVA
```

## 🎯 Componentes UI BBVA

### Tarjetas KPI BBVA
- **Gradiente sutil**: Blanco a gris claro
- **Hover effects**: Elevación y sombra mejorada
- **Colores semánticos**: Verde/rojo según cambios
- **Tipografía jerárquica**: Labels uppercase, values grandes

### Formularios BBVA
- **Secciones diferenciadas**: Tradicionales vs Alternativos
- **Inputs BBVA-styled**: Bordes y colores corporativos
- **Validación en tiempo real**: Feedback visual BBVA
- **Agrupación lógica**: Información organizada por categorías

### Loading States BBVA
- **Spinner BBVA Aqua**: Animación circular con color corporativo
- **Texto descriptivo**: "Analizando con Algoritmo de Confianza..."
- **Fondo blanco**: Contenedor limpio institucional
- **Borde BBVA Aqua**: Marco corporativo del loading

### Gráficos BBVA
- **Paleta corporativa**: Todos los gráficos usan colores BBVA
- **Sin bordes innecesarios**: Data-ink ratio optimizado
- **Tipografía consistente**: Fuente BBVA en todos los textos
- **Fondos blancos**: Limpieza y legibilidad máxima

## 📊 Métricas y KPIs BBVA

### Dashboard Directivo
- **Tasa de Aprobación**: Porcentaje con colores BBVA semánticos
- **NPL Rate**: Tasa de morosidad con alertas BBVA
- **Volumen API**: Peticiones mensuales con tracking BBVA
- **Population Stability**: PSI con umbrales BBVA

### Evaluador de Crédito
- **BBVA Score**: 0-1000 con display corporativo
- **Decisión BBVA**: Aprobado/Denegado con colores BBVA
- **Feature Importance**: Contribución variables con colores BBVA
- **Compliance Indicators**: Estado GDPR/AI Act con branding BBVA

## 🔒 Seguridad y Privacidad BBVA

### Cumplimiento Corporativo
- **GDPR Compliant**: Diseño privacy-by-default BBVA
- **AI Act Ready**: Explicabilidad con branding BBVA
- **Data Minimization**: Solo datos necesarios BBVA
- **Right to Explanation**: SHAP con identidad visual BBVA

### Medidas de Seguridad BBVA
- **Input Validation**: Validación con estilos BBVA
- **Output Sanitization**: Limpieza con estándares BBVA
- **Session Management**: Estados seguros BBVA
- **Error Handling**: Manejo elegante con diseño BBVA

## 🎯 Casos de Uso BBVA

### Para Clientes BBVA
- **Evaluación rápida**: Procesamiento BBVA vs días tradicionales
- **Transparencia BBVA**: Explicaciones con identidad visual
- **Confianza institucional**: Experiencia BBVA consistente
- **Seguridad garantizada**: Cumplimiento BBVA de estándares

### Para Analistas BBVA
- **Visualización BBVA**: Métricas con identidad corporativa
- **Control de calidad**: Monitoreo con diseño BBVA
- **Análisis de impacto**: Evaluación con estética BBVA
- **Reportes BBVA**: Generación con branding BBVA

### Para Equipos de Desarrollo
- **Design System BBVA**: Componentes reutilizables corporativos
- **Testing BBVA**: Simulación con experiencia BBVA
- **Validación BBVA**: Features con identidad visual BBVA
- **Documentación BBVA**: Ejemplos con diseño BBVA

## 🚀 Mejoras Futuras BBVA

### Short Term (1-3 meses)
- [ ] Integración APIs BBVA reales
- [ ] Base datos BBVA persistente
- [ ] Autenticación BBVA con SSO
- [ ] Exportación PDF con branding BBVA

### Medium Term (3-6 meses)
- [ ] Machine Learning BBVA en tiempo real
- [ ] Dashboard personalizable BBVA
- [ ] Alertas BBVA automáticas
- [ ] Integración core BBVA

### Long Term (6-12 meses)
- [ ] IA conversacional BBVA
- [ ] Análisis predictivo BBVA
- [ ] Gamificación BBVA
- [ ] Expansión internacional BBVA

## 📞 Soporte y Contacto BBVA

### Documentación BBVA
- **API Documentation**: Endpoints con formato BBVA
- **Model Documentation**: Arquitectura BBVA
- **Deployment Guide**: Producción BBVA
- **Troubleshooting**: Problemas BBVA

### Equipo BBVA
- **Product Manager BBVA**: Estrategia BBVA
- **UI/UX Designer BBVA**: Experiencia BBVA
- **Data Scientist BBVA**: Modelos BBVA
- **Full Stack Developer BBVA**: Arquitectura BBVA

---

**BBVA Algoritmo de Confianza** © 2024 - Banco Bilbao Vizcaya Argentaria | IA Explicable con Identidad Corporativa
