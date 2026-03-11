# **CAPÍTULO 1: INTRODUCCIÓN**

## **1.1 Contextualización del proyecto**

El sector financiero español está experimentando una transformación sin precedentes impulsada por la digitalización acelerada y la irrupción de las tecnologías FinTech. Según datos de la Asociación Española de FinTech e Insurtech (AEFI, 2024), España se consolida como el tercer mercado FinTech más importante de Europa y el sexto a nivel mundial, con un ecosistema que supera las 300 empresas y genera ingresos por valor de €15.3 mil millones en 2024, con una tasa de crecimiento anual compuesta (CAGR) del 18% para el período 2024-2028 (AEFI, 2024).

Esta revolución digital ha creado una paradoja fundamental en el sistema financiero español: por un lado, la abundancia de datos digitales generados por los ciudadanos en su vida cotidiana; por otro, la persistencia de brechas significativas en la inclusión financiera. Según el informe del Defensor del Pueblo (2024), aproximadamente 8 millones de personas en España enfrentan algún grado de exclusión financiera, con colectivos especialmente vulnerables como jóvenes (18-30 años) con tasas de exclusión del 35%, población inmigrante (28%) y trabajadores autónomos (22%) (Defensor del Pueblo, 2024).

El contexto regulatorio europeo ha evolucionado significativamente con la implementación de la Directiva PSD2, que ha abierto las puertas al Open Banking y facilitado el acceso a datos financieros mediante APIs estandarizadas (Banco de España, 2024). Simultáneamente, el Reglamento General de Protección de Datos (GDPR) y la propuesta de AI Act establecen un marco ético y legal para el uso responsable de datos y algoritmos de inteligencia artificial (European Commission, 2022).

En este escenario, PFM VELMAK se posiciona como una empresa especializada en scoring financiero alternativo que sirve a clientes del sector FinTech. La empresa opera bajo un modelo B2B, proporcionando APIs de evaluación de riesgo crediticio que permiten a las entidades financieras tomar decisiones más informadas y rápidas, especialmente para segmentos de población tradicionalmente desatendidos por el sistema bancario convencional.

La relevancia del Big Data y la analítica avanzada en este contexto es fundamental. Los datos alternativos derivados del comportamiento digital —patrones de consumo en plataformas de delivery, uso de servicios de transporte, actividad en e-commerce, pagos de servicios básicos y comportamiento en redes sociales— han demostrado ser predictores robustos de la solvencia crediticia (Ghosh, 2021). Estos datos, procesados mediante algoritmos de machine learning, permiten construir perfiles de riesgo más precisos e inclusivos que los métodos tradicionales basados exclusivamente en historiales bancarios (World Bank, 2022).

## **1.2 Justificación de la importancia del análisis del modelo de datos y su mejora**

La transformación del modelo de datos de PFM VELMAK representa una oportunidad estratégica tanto desde la perspectiva del negocio como del impacto social. Los sistemas tradicionales de scoring crediticio dependen fundamentalmente de bureaus de crédito como CIRBE (Central de Información de Riesgos del Banco de España) y ASNEF (Asociación Nacional de Establecimientos Financieros), lo que limita significativamente la capacidad de evaluar a personas sin historial crediticio formal (Banco de España, 2024).

El potencial de los datos digitales reside en su capacidad para capturar matices del comportamiento financiero que los datos tradicionales ignoran. Por ejemplo, la regularidad en los pagos de servicios de delivery, la estabilidad en los patrones de transporte o el comportamiento de compra en plataformas e-commerce pueden indicar disciplina financiera y capacidad de pago, incluso en ausencia de historial bancario (OECD, 2022). Estos datos alternativos, cuando son analizados mediante técnicas avanzadas de machine learning, pueden mejorar la precisión en la evaluación de riesgo hasta en un 15-20% comparado con métodos convencionales (Kreditech, 2023).

El impacto social de esta mejora es sustancial. La inclusión financiera no solo facilita el acceso a créditos, sino que constituye un pilar fundamental para la movilidad social y el desarrollo económico. Según el Global Findex Database del Banco Mundial (2023), cada 10% de aumento en la inclusión financiera se asocia con un crecimiento económico adicional del 0.5-1% en los países en desarrollo, una relación que también se observa en economías avanzadas como España (World Bank, 2023).

Desde la perspectiva regulatoria, la implementación de un modelo de datos mejorado posiciona a PFM VELMAK favorablemente frente a los requisitos crecientes de transparencia y explicabilidad. La AI Act europea exige que los sistemas de toma de decisiones de alta riesgo sean interpretables y auditables, un requisito que los modelos de caja negra tradicionales no cumplen (European Commission, 2022). La implementación de técnicas de IA explicable, como SHAP (SHapley Additive exPlanations), no solo asegura el cumplimiento regulatorio, sino que genera confianza tanto en los clientes FinTech como en los usuarios finales (Lundberg & Lee, 2017).

El caso de negocio es igualmente compelling. El mercado español de scoring crediticio alternativo representa una oportunidad de €2.1 mil millones, aproximadamente el 32% del mercado total FinTech (McKinsey & Company, 2023). Las entidades financieras que adoptan estos modelos reportan reducciones del 25% en las tasas de impago y aumentos del 30% en la aprobación de créditos para segmentos tradicionalmente excluidos (PwC, 2024).

## **1.3 Objetivos del proyecto: generales y específicos**

### **Objetivo General**

Desarrollar un sistema integral de scoring crediticio basado en datos de comportamiento digital y técnicas de Big Data que permita a PFM VELMAK ofrecer evaluaciones de riesgo más precisas, rápidas e inclusivas a sus clientes del sector FinTech, contribuyendo simultáneamente a la reducción de la exclusión financiera en España y al crecimiento sostenible de la empresa.

### **Objetivos Específicos**

1. **Implementación de modelo de Machine Learning con alta precisión**: Desarrollar y desplegar un modelo ensemble que combine múltiples algoritmos (XGBoost, Random Forest, Redes Neuronales) para alcanzar una precisión superior al 90% en la predicción de riesgo crediticio, medida mediante el área bajo la curva ROC (ROC-AUC).

2. **Desarrollo de API RESTful de alto rendimiento**: Construir una arquitectura de microservicios con latencia inferior a 50ms (percentil 95) y capacidad de procesamiento superior a 10,000 solicitudes por segundo, garantizando una disponibilidad del 99.9% mediante implementación de patrones de resiliencia y escalabilidad horizontal.

3. **Creación de dashboard de analytics interactivo**: Implementar una plataforma de visualización de datos en tiempo real que permita a los clientes FinTech monitorizar carteras, identificar tendencias de riesgo y tomar decisiones informadas mediante interfaces intuitivas basadas en principios de diseño centrado en el usuario.

4. **Implementación de sistema de IA explicable**: Integrar SHAP y LIME (Local Interpretable Model-agnostic Explanations) para proporcionar explicaciones comprensibles de cada decisión de scoring, cumpliendo con los requisitos de la AI Act europea y generando confianza en clientes y usuarios finales.

5. **Validación con datasets sintéticos y reales**: Realizar pruebas exhaustivas utilizando tanto datos sintéticos generados mediante técnicas de GANs (Generative Adversarial Networks) como datasets reales anonimizados de clientes piloto, validando el rendimiento del modelo en diversos escenarios y segmentos poblacionales.

6. **Aseguramiento de cumplimiento regulatorio**: Garantizar el cumplimiento integral de GDPR, PSD2 y las directrices del Banco de España mediante implementación de privacy by design, anonimización de datos y establecimiento de protocolos de auditoría y gobernanza de algoritmos.

## **1.4 Metodología empleada**

El proyecto seguirá una adaptación del framework CRISP-DM (Cross-Industry Standard Process for Data Mining) específicamente diseñada para el sector financiero, incorporando mejores prácticas de MLOps y principios de desarrollo ágil. Esta metodología se estructura en seis fases iterativas que permiten el desarrollo incremental y la validación continua.

### **Fase 1: Comprensión del Negocio y Contexto Regulatorio**

Esta fase inicial involucra un análisis profundo del modelo de negocio actual de PFM VELMAK, el ecosistema FinTech español y el marco regulatorio aplicable. Se realizarán entrevistas con stakeholders clave, análisis de la competencia (Fintonic, Creditas, Kreditech) y revisión exhaustiva de requerimientos regulatorios (Banco de España, 2024; EBA, 2023).

### **Fase 2: Comprensión y Preparación de Datos**

Se implementará un pipeline de ingesta de datos que integre múltiples fuentes:
- **Datos transaccionales**: APIs de plataformas de delivery (Glovo, Uber Eats), servicios de transporte (Cabify, Uber) y e-commerce (Amazon, Zara)
- **Datos de comportamiento**: Patrones de uso de servicios digitales, geolocalización y temporalidad
- **Datos tradicionales**: Información de bureaus de crédito cuando esté disponible

El procesamiento utilizará Apache Spark para transformación a gran escala, con implementación de técnicas de feature engineering automatizadas y detección de anomalías mediante isolation forests (Apache Software Foundation, 2024).

### **Fase 3: Modelado y Experimentación**

Se desarrollará un enfoque de modelado ensemble que combine:
- **Gradient Boosting**: XGBoost y LightGBM para capturar relaciones no lineales
- **Deep Learning**: Redes neuronales recurrentes para patrones temporales y grafos neuronales para relaciones sociales
- **Métodos híbridos**: Combinación de aprendizaje supervisado y no supervisado para detección de patrones emergentes

La experimentación seguirá principios de TDD (Test-Driven Development) con validación cruzada estratificada y optimización de hiperparámetros mediante Bayesian optimization (Chen & Guestrin, 2016).

### **Fase 4: Evaluación y Validación**

La evaluación utilizará múltiples métricas adaptadas al contexto financiero:
- **Métricas de discriminación**: ROC-AUC, Precision-Recall AUC, KS statistic
- **Métricas de calibración**: Brier score, Hosmer-Lemeshow test
- **Métricas de negocio**: Cost-benefit analysis, expected loss reduction
- **Métricas de equidad**: Demographic parity, equal opportunity difference

Se realizará backtesting histórico y validación forward-looking para asegurar la robustez del modelo en diferentes condiciones de mercado (Bahnsen et al., 2022).

### **Fase 5: Despliegue y Monitorización**

El despliegue seguirá una arquitectura de microservicios con:
- **API Gateway**: Kong o AWS API Gateway para routing y autenticación
- **Servicios de scoring**: Contenerizados con Docker y orquestados con Kubernetes
- **Feature Store**: Feast para centralización y versionado de features
- **Streaming**: Apache Kafka para procesamiento en tiempo real

El monitorización implementará MLflow para tracking de experimentos, Prometheus para métricas de sistema y dashboards personalizados con Grafana para business intelligence.

### **Fase 6: Gestión del Cambio y Mejora Continua**

Se establecerá un framework de mejora continua con:
- **Retraining automatizado**: Programas de reentrenamiento basados en detección de drift de datos
- **A/B testing**: Experimentación controlada para validar mejoras
- **Feedback loops**: Incorporación de resultados reales para refinamiento del modelo
- **Auditorías periódicas**: Revisión de sesgos, cumplimiento y performance

La metodología incorpora principios de Responsible AI y Data Ethics, asegurando que el desarrollo tecnológico se alinee con valores de transparencia, equidad y responsabilidad social (Doshi-Velez & Kim, 2017).

---

**Este capítulo establece las bases fundamentales del proyecto, justificando la necesidad estratégica de transformar el modelo de datos de PFM VELMAK mediante la aplicación de técnicas avanzadas de Big Data y Machine Learning. Los objetivos definidos y la metodología propuesta aseguran un enfoque estructurado y medible que posicionará a la empresa como líder en el sector de scoring crediticio alternativo en España.**
