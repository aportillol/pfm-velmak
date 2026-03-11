# **CAPÍTULO 17: ANEXOS**

## **Anexo 1: Diccionario de Datos Alternativos (Data Dictionary)**

| Nombre Variable | Tipo Dato | Origen | Descripción de Negocio |
|-----------------|-------------|----------|------------------------|
| `account_balance_eur` | Float | API PSD2 | Saldo total en cuenta corriente en euros. Variable fundamental para evaluar capacidad de pago y estabilidad financiera. |
| `monthly_income_eur` | Float | API PSD2 | Ingreso mensual promedio declarado por el cliente. Indicador clave de capacidad de endeudamiento sostenible. |
| `transaction_count_30d` | Integer | API PSD2 | Número de transacciones realizadas en últimos 30 días. Proxy de actividad financiera y estabilidad de ingresos. |
| `avg_transaction_amount` | Float | API PSD2 | Importe medio de transacciones realizadas. Indicador de patrones de consumo y disciplina financiera. |
| `saving_account_balance` | Float | API PSD2 | Saldo en cuenta de ahorro. Indicador de capacidad de previsión y comportamiento financiero responsable. |
| `credit_card_utilization` | Float | API PSD2 | Porcentaje de utilización de límite de tarjeta de crédito. Proxy de presión financiera y gestión de deuda. |
| `direct_debit_frequency` | Integer | API PSD2 | Frecuencia de domiciliaciones bancarias. Indicador de estabilidad de pagos recurrentes y compromisos financieros. |
| `online_banking_login_days` | Integer | Web Tracking | Días promedio entre inicios de sesión en banca online. Proxy de engagement digital y control financiero. |
| `mobile_device_type` | String | Device Fingerprinting | Tipo de dispositivo móvil utilizado (iOS/Android). Variable contextual para patrones de comportamiento. |
| `app_session_duration` | Float | App Analytics | Duración promedio de sesión en aplicación móvil. Indicador de interés y complejidad de operaciones financieras. |
| `ecommerce_transaction_count` | Integer | E-commerce APIs | Número de transacciones en plataformas e-commerce. Proxy de comportamiento de consumo digital. |
| `subscription_services_count` | Integer | Telco APIs | Número de servicios de suscripción activos. Indicador de compromisos financieros recurrentes. |
| `telco_payment_history` | String | Telco APIs | Historial de pagos de servicios de telecomunicaciones. Proxy de fiabilidad en pagos y estabilidad financiera. |
| `social_media_activity_score` | Float | Social Media APIs | Puntuación de actividad en redes sociales. Variable contextual para perfil de comportamiento digital. |
| `location_stability_months` | Integer | Geolocation API | Meses en misma ubicación geográfica. Proxy de estabilidad residencial y laboral. |
| `employment_verification_status` | Boolean | HR APIs | Estado de verificación de empleo. Indicador directo de capacidad de ingresos. |
| `utility_payment_history` | String | Utility APIs | Historial de pagos de servicios básicos. Proxy de responsabilidad financiera y estabilidad de vida. |

## **Anexo 2: Mockup de Ingesta y Procesamiento (Fragmento de Código Python/PySpark)**

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, count, sum as _sum, avg as _avg
from pyspark.sql.types import StructType, StructField, StringType, FloatType, IntegerType, BooleanType
import json
from kafka import KafkaConsumer
import pymongo
from datetime import datetime

class OpenBankingDataProcessor:
    """Clase para procesamiento de datos de Open Banking desde Kafka"""
    
    def __init__(self, spark_session, kafka_config, mongo_config):
        self.spark = spark_session
        self.kafka_consumer = KafkaConsumer(
            'open_banking_topic',
            bootstrap_servers=kafka_config['bootstrap_servers'],
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            group_id='velmak_processor'
        )
        self.mongo_client = pymongo.MongoClient(mongo_config['connection_string'])
        self.db = self.mongo_client[mongo_config['database']]
        self.collection = self.db[mongo_config['collection']]
    
    def process_streaming_data(self):
        """Procesamiento en tiempo real de datos desde Kafka"""
        print(f"Iniciando procesamiento de streaming: {datetime.now()}")
        
        for message in self.kafka_consumer:
            try:
                # Extraer y validar datos del mensaje
                raw_data = message.value
                processed_data = self._validate_and_clean_data(raw_data)
                
                if processed_data:
                    # Transformar datos para análisis
                    enriched_data = self._enrich_data(processed_data)
                    
                    # Almacenar en MongoDB
                    self._store_to_mongodb(enriched_data)
                    
                    print(f"Procesado registro para cliente: {processed_data.get('customer_id')}")
                    
            except Exception as e:
                print(f"Error procesando mensaje: {str(e)}")
                continue
    
    def _validate_and_clean_data(self, data):
        """Validación y limpieza básica de datos"""
        if not data or 'customer_id' not in data:
            return None
        
        # Manejo de valores nulos
        cleaned_data = {
            'customer_id': data.get('customer_id'),
            'account_balance': float(data.get('account_balance', 0)) if data.get('account_balance') else None,
            'monthly_income': float(data.get('monthly_income', 0)) if data.get('monthly_income') else None,
            'transaction_count': int(data.get('transaction_count_30d', 0)) if data.get('transaction_count_30d') else None,
            'avg_transaction': float(data.get('avg_transaction_amount', 0)) if data.get('avg_transaction_amount') else None,
            'processing_timestamp': datetime.now().isoformat()
        }
        
        # Validación de rangos lógicos
        if cleaned_data['account_balance'] and cleaned_data['account_balance'] < 0:
            print(f"Advertencia: Saldo negativo para cliente {cleaned_data['customer_id']}")
        
        return cleaned_data
    
    def _enrich_data(self, data):
        """Enriquecimiento de datos con características derivadas"""
        enriched = data.copy()
        
        # Calcular ratio de utilización de crédito
        if data.get('credit_limit') and data.get('credit_card_balance'):
            enriched['credit_utilization_ratio'] = data['credit_card_balance'] / data['credit_limit']
        
        # Clasificar nivel de actividad financiera
        transaction_count = data.get('transaction_count', 0)
        if transaction_count > 50:
            enriched['activity_level'] = 'HIGH'
        elif transaction_count > 20:
            enriched['activity_level'] = 'MEDIUM'
        else:
            enriched['activity_level'] = 'LOW'
        
        # Calcular score de estabilidad financiera (simplificado)
        balance_score = 0
        if data.get('account_balance') and data.get('account_balance') > 1000:
            balance_score += 30
        if data.get('monthly_income') and data.get('monthly_income') > 2000:
            balance_score += 40
        if data.get('transaction_count') and data.get('transaction_count') > 20:
            balance_score += 30
        
        enriched['financial_stability_score'] = balance_score
        
        return enriched
    
    def _store_to_mongodb(self, data):
        """Almacenamiento de datos procesados en MongoDB"""
        try:
            # Insertar documento con estructura optimizada para consultas
            document = {
                'customer_id': data['customer_id'],
                'raw_data': data,
                'processed_features': {
                    'account_balance': data.get('account_balance'),
                    'monthly_income': data.get('monthly_income'),
                    'transaction_metrics': {
                        'count': data.get('transaction_count'),
                        'avg_amount': data.get('avg_transaction'),
                        'activity_level': data.get('activity_level')
                    },
                    'derived_features': {
                        'credit_utilization_ratio': data.get('credit_utilization_ratio'),
                        'financial_stability_score': data.get('financial_stability_score')
                    }
                },
                'metadata': {
                    'ingestion_timestamp': data.get('processing_timestamp'),
                    'data_source': 'open_banking_api',
                    'processing_version': '1.0'
                }
            }
            
            self.collection.insert_one(document)
            
        except Exception as e:
            print(f"Error almacenando en MongoDB: {str(e)}")

# Configuración inicial
if __name__ == "__main__":
    spark = SparkSession.builder \
        .appName("OpenBankingProcessor") \
        .config("spark.mongodb.input.uri", "mongodb://localhost:27017/velmak.raw_data") \
        .getOrCreate()
    
    kafka_config = {
        'bootstrap_servers': ['kafka-broker-1:9092', 'kafka-broker-2:9092'],
        'topic': 'open_banking_transactions'
    }
    
    mongo_config = {
        'connection_string': 'mongodb://localhost:27017',
        'database': 'velmak',
        'collection': 'processed_alternative_data'
    }
    
    # Iniciar procesamiento
    processor = OpenBankingDataProcessor(spark, kafka_config, mongo_config)
    processor.process_streaming_data()
```

## **Anexo 3: Ejemplo de Explicabilidad Algorítmica (Fragmento de Código Python)**

```python
import shap
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import json

class CreditScoringExplainer:
    """Clase para implementar explicabilidad en modelo de scoring crediticio"""
    
    def __init__(self, model, feature_names, X_train):
        self.model = model
        self.feature_names = feature_names
        self.X_train = X_train
        
        # Inicializar SHAP explainer
        self.explainer = shap.TreeExplainer(model)
        
        # Calcular valores SHAP para dataset de entrenamiento
        print("Calculando valores SHAP para dataset de entrenamiento...")
        self.shap_values = self.explainer.shap_values(X_train)
        
    def explain_individual_prediction(self, customer_data, customer_id):
        """
        Genera explicación detallada para una predicción individual
        cumpliendo con requisitos de transparencia de AI Act
        """
        try:
            # Realizar predicción
            prediction = self.model.predict_proba(customer_data)[0]
            prediction_class = np.argmax(prediction)
            confidence = prediction[prediction_class]
            
            # Calcular valores SHAP para esta predicción
            shap_values = self.explainer.shap_values(customer_data)
            
            # Generar explicación estructurada
            explanation = {
                'customer_id': customer_id,
                'prediction': {
                    'class': 'APPROVED' if prediction_class == 1 else 'REJECTED',
                    'confidence': float(confidence),
                    'risk_score': float(prediction[0])  # Probabilidad de default
                },
                'explanation': {
                    'main_factors': self._get_main_factors(shap_values[0], customer_data),
                    'feature_contributions': self._get_detailed_contributions(shap_values[0], customer_data),
                    'summary': self._generate_explanation_summary(shap_values[0], customer_data, prediction_class)
                },
                'compliance': {
                    'ai_act_compliant': True,
                    'explanation_method': 'SHAP (SHapley Additive exPlanations)',
                    'right_to_explanation': True,
                    'human_review_available': True
                },
                'timestamp': pd.Timestamp.now().isoformat()
            }
            
            return explanation
            
        except Exception as e:
            return {
                'error': f"Error generando explicación: {str(e)}",
                'customer_id': customer_id,
                'timestamp': pd.Timestamp.now().isoformat()
            }
    
    def _get_main_factors(self, shap_values, customer_data):
        """Identifica los factores principales que influyeron en la decisión"""
        # Obtener valores absolutos de SHAP
        abs_shap = np.abs(shap_values)
        
        # Top 5 factores más influyentes
        top_indices = np.argsort(abs_shap)[-5:][::-1]
        
        main_factors = []
        for idx in top_indices:
            factor = {
                'feature': self.feature_names[idx],
                'impact': 'INCREASES_RISK' if shap_values[idx] > 0 else 'DECREASES_RISK',
                'magnitude': float(abs_shap[idx]),
                'value': float(customer_data.iloc[0, idx]) if hasattr(customer_data, 'iloc') else float(customer_data[idx])
            }
            main_factors.append(factor)
        
        return main_factors
    
    def _get_detailed_contributions(self, shap_values, customer_data):
        """Genera contribución detallada de cada característica"""
        contributions = {}
        
        for i, (feature_name, shap_val) in enumerate(zip(self.feature_names, shap_values)):
            feature_value = float(customer_data.iloc[0, i]) if hasattr(customer_data, 'iloc') else float(customer_data[i])
            
            contributions[feature_name] = {
                'base_value': float(feature_value),
                'shap_value': float(shap_val),
                'impact_direction': 'POSITIVE' if shap_val > 0 else 'NEGATIVE',
                'impact_percentage': float(abs(shap_val) / np.sum(np.abs(shap_values)) * 100)
            }
        
        return contributions
    
    def _generate_explanation_summary(self, shap_values, customer_data, prediction_class):
        """Genera resumen en lenguaje natural de la explicación"""
        # Identificar factores más positivos y negativos
        positive_factors = []
        negative_factors = []
        
        for i, (feature_name, shap_val) in enumerate(zip(self.feature_names, shap_values)):
            feature_value = float(customer_data.iloc[0, i]) if hasattr(customer_data, 'iloc') else float(customer_data[i])
            
            if shap_val > 0:
                positive_factors.append(f"alto {feature_name} ({feature_value:.2f})")
            else:
                negative_factors.append(f"bajo {feature_name} ({feature_value:.2f})")
        
        # Generar explicación según resultado
        if prediction_class == 1:  # Aprobado
            summary = f"El crédito fue APROBADO principalmente por {', '.join(positive_factors[:3])}. "
            if negative_factors:
                summary += f"Los siguientes factores redujeron ligeramente el riesgo: {', '.join(negative_factors[:2])}. "
            summary += "La decisión se basa en un análisis equilibrado de múltiples factores financieros y de comportamiento."
        else:  # Rechazado
            summary = f"El crédito fue RECHAZADO principalmente por {', '.join(negative_factors[:3])}. "
            if positive_factors:
                summary += f"Los siguientes factores mitigaron parcialmente el riesgo: {', '.join(positive_factors[:2])}. "
            summary += "Se recomienda mejorar los aspectos identificados antes de una nueva solicitud."
        
        return summary
    
    def generate_explanation_report(self, customer_data, customer_id):
        """Genera reporte completo en formato JSON para API response"""
        explanation = self.explain_individual_prediction(customer_data, customer_id)
        
        # Estructura de respuesta para API VELMAK
        api_response = {
            'status': 'success',
            'data': {
                'scoring_result': explanation['prediction'],
                'explanation': explanation['explanation'],
                'compliance_info': explanation['compliance'],
                'request_metadata': {
                    'customer_id': customer_id,
                    'model_version': '2.1',
                    'explanation_version': '1.0',
                    'processing_time_ms': 150
                }
            }
        }
        
        return api_response

# Ejemplo de uso
def demo_explainability():
    """Demostración del sistema de explicabilidad"""
    
    # Datos de ejemplo (simulando un cliente real)
    customer_features = pd.DataFrame({
        'account_balance': [2500.0],
        'monthly_income': [3200.0],
        'transaction_count_30d': [45],
        'avg_transaction': [85.5],
        'credit_utilization': [0.35],
        'employment_verified': [1],
        'location_stability': [24]
    })
    
    feature_names = ['account_balance', 'monthly_income', 'transaction_count_30d', 
                   'avg_transaction', 'credit_utilization', 'employment_verified', 'location_stability']
    
    # Modelo entrenado (simulado)
    from sklearn.ensemble import RandomForestClassifier
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    
    # Datos de entrenamiento simulados
    X_train = pd.DataFrame(np.random.randn(1000, 7), columns=feature_names)
    y_train = np.random.randint(0, 2, 1000)
    model.fit(X_train, y_train)
    
    # Crear explainer
    explainer = CreditScoringExplainer(model, feature_names, X_train)
    
    # Generar explicación para el cliente
    explanation = explainer.explain_individual_prediction(customer_features, "CUST_001234")
    
    print("EXPLICACIÓN DETALLADA PARA EVALUACIÓN DE CRÉDITO")
    print("=" * 60)
    print(json.dumps(explanation, indent=2))
    
    return explanation

if __name__ == "__main__":
    demo_explainability()
```

## **Anexo 4: Medidas DAX de Control Operativo (Power BI)**

```dax
// Medida 1: Tasa de Morosidad NPL a 90 días
// Calcula el porcentaje de créditos en morosidad > 90 días
NPL Rate 90 Days = 
VAR NPL90Days = 
    CALCULATE(
        SUM('Loans'[Amount]) * 
        DIVIDE(
            SUM('Loans'[Days Past Due]),
            90
        ),
        'Loans'[Days Past Due] > 90
    )

VAR TotalLoans = SUM('Loans'[Amount])

RETURN
    DIVIDE(
        NPL90Days,
        TotalLoans,
        0
    )

// Medida 2: Volumen de Peticiones API Month-to-Date (MTD)
// Calcula el volumen total de llamadas a la API en el mes actual
API Volume MTD = 
VAR CurrentMonth = MONTH(TODAY())
VAR CurrentYear = YEAR(TODAY())

RETURN
    CALCULATE(
        COUNTROWS('API Logs'),
        FILTER(
            'API Logs'[Date] >= DATE(CurrentYear, CurrentMonth, 1) &&
            'API Logs'[Date] <= TODAY() &&
            'API Logs'[Status] = "Success"
        )
    )

// Medida 3: Population Stability Index (PSI) para Alerta de Drift
// Calcula PSI entre distribución actual vs distribución de entrenamiento
Population Stability Index = 
VAR CurrentDistribution = 
    ADDCOLUMNS(
        SUMMARIZE('Current Data', 'Current Data'[Score Range]),
        "Current %", DIVIDE(SUM('Current Data'[Count]), CALCULATE(SUM('Current Data'[Count]), ALL('Current Data')))
    )

VAR BaselineDistribution = 
    ADDCOLUMNS(
        SUMMARIZE('Baseline Data', 'Baseline Data'[Score Range]),
        "Baseline %", DIVIDE(SUM('Baseline Data'[Count]), CALCULATE(SUM('Baseline Data'[Count]), ALL('Baseline Data')))
    )

VAR MergedTables = 
    NATURALLEFTOUTERJOIN(CurrentDistribution, BaselineDistribution, 'Current Data'[Score Range], 'Baseline Data'[Score Range])

RETURN
    SUMX(
        MergedTables,
        IF(
            ISBLANK([Baseline %]),
            0,
            ([Current %] - [Baseline %]) * 
            LN([Current %] / [Baseline %])
        )
    )

// Medida 4: Latencia Promedio de API por Percentil
// Calcula latencia P95 para monitoreo de rendimiento
API Latency P95 = 
VAR LatencyValues = 
    CALCULATETABLE(
        "API Logs",
        "API Logs"[Response Time],
        "API Logs"[Status] = "Success"
    )

RETURN
    PERCENTILEX.INC(
        LatencyValues,
        0.95,
        "API Logs"[Response Time]
    )

// Medida 5: Tasa de Conversión por Canal de Adquisición
// Calcula tasa de conversión desglosada por canal
Conversion Rate by Channel = 
VAR LeadsByChannel = SUMMARIZE('Leads', 'Leads'[Channel], "Lead Count", COUNTROWS('Leads'))
VAR CustomersByChannel = SUMMARIZE('Customers', 'Customers'[Channel], "Customer Count", COUNTROWS('Customers'))

RETURN
    SUMX(
        NATURALINNERJOIN(LeadsByChannel, CustomersByChannel, 'Leads'[Channel], 'Customers'[Channel]),
        DIVIDE([Customer Count], [Lead Count])
    )

// Medida 6: Score de Riesgo Promedio por Segmento
// Calcula score de riesgo promedio desglosado por segmento demográfico
Average Risk Score by Segment = 
VAR RiskScores = 
    CALCULATETABLE(
        "Customer Segments",
        "Customer Segments"[Risk Score],
        "Customer Segments"[Segment]
    )

RETURN
    AVERAGEX(
        RiskScores,
        "Customer Segments"[Risk Score]
    )

// Medida 7: Crecimiento de Ingresos Recurrentes (MRR Growth)
// Calcula crecimiento mes sobre mes de ingresos recurrentes
MRR Growth Rate = 
VAR CurrentMRR = CALCULATE(SUM('Revenue'[MRR]), 'Revenue'[Date] = EOMONTH(TODAY(), -1))
VAR PreviousMRR = CALCULATE(SUM('Revenue'[MRR]), 'Revenue'[Date] = EOMONTH(TODAY(), -2))

RETURN
    DIVIDE(
        CurrentMRR - PreviousMRR,
        PreviousMRR,
        0
    )

// Medida 8: Índice de Satisfacción del Cliente (NPS)
// Calcula Net Promoter Score basado en encuestas
Net Promoter Score = 
VAR Promoters = CALCULATE(COUNTROWS('Survey Responses'), 'Survey Responses'[NPS Category] = "Promoter")
VAR Detractors = CALCULATE(COUNTROWS('Survey Responses'), 'Survey Responses'[NPS Category] = "Detractor")
VAR TotalResponses = COUNTROWS('Survey Responses')

RETURN
    DIVIDE(
        (Promoters - Detractors) * 100,
        TotalResponses,
        0
    )
```

## **Anexo 5: Estructura del Payload de la API de VELMAK (JSON)**

```json
{
  "status": "success",
  "timestamp": "2024-03-15T14:32:18.452Z",
  "request_id": "REQ_20240315_001234",
  "data": {
    "customer_id": "CUST_ES_789456",
    "scoring_result": {
      "decision": "APPROVED",
      "risk_score": 285,
      "confidence_level": 0.87,
      "risk_category": "LOW_MEDIUM",
      "recommended_credit_limit_eur": 15000.00,
      "interest_rate_applied": 0.065,
      "decision_timestamp": "2024-03-15T14:32:18.452Z"
    },
    "explanation": {
      "compliance": {
        "ai_act_compliant": true,
        "explanation_available": true,
        "human_review_required": false,
        "right_to_explanation": true,
        "explanation_method": "SHAP_v2.1"
      },
      "main_factors": [
        {
          "factor": "account_balance",
          "impact": "POSITIVE",
          "magnitude": 0.35,
          "description": "Saldo estable de €2,500 indica capacidad de pago",
          "value": 2500.00
        },
        {
          "factor": "monthly_income",
          "impact": "POSITIVE", 
          "magnitude": 0.28,
          "description": "Ingreso mensual de €3,200 demuestra solvencia",
          "value": 3200.00
        },
        {
          "factor": "credit_utilization",
          "impact": "NEGATIVE",
          "magnitude": 0.18,
          "description": "Utilización del crédito al 35% indica presión financiera moderada",
          "value": 0.35
        },
        {
          "factor": "transaction_frequency",
          "impact": "POSITIVE",
          "magnitude": 0.12,
          "description": "Alta frecuencia de transacciones (45/mes) muestra actividad financiera saludable",
          "value": 45
        },
        {
          "factor": "employment_stability",
          "impact": "POSITIVE",
          "magnitude": 0.07,
          "description": "Verificación de empleo estable por más de 2 años",
          "value": 24
        }
      ],
      "detailed_contributions": {
        "positive_factors": [
          {
            "feature": "account_balance",
            "contribution": "+35%",
            "base_value": 2500.00,
            "reasoning": "Saldo por encima del umbral mínimo de €1,000"
          },
          {
            "feature": "monthly_income", 
            "contribution": "+28%",
            "base_value": 3200.00,
            "reasoning": "Ingreso superior al promedio del segmento"
          }
        ],
        "negative_factors": [
          {
            "feature": "credit_utilization",
            "contribution": "-18%",
            "base_value": 0.35,
            "reasoning": "Utilización moderada pero por encima del óptimo del 30%"
          }
        ]
      },
      "natural_language_summary": "El crédito ha sido APROBADO basado principalmente en su saldo estable de €2,500 y ingresos mensuales de €3,200. Los factores positivos incluyen alta actividad transaccional (45 operaciones/mes) y estabilidad laboral verificada (24 meses). Se observó una utilización moderada del crédito (35%) que genera ligera presión financiera. La decisión cumple con los criterios de riesgo establecidos y se basa en análisis equilibrado de múltiples indicadores financieros y de comportamiento."
    },
    "model_metadata": {
      "model_version": "2.1.3",
      "training_data_period": "2022-01-01 to 2024-02-29",
      "feature_count": 47,
      "algorithm_type": "XGBoost_Ensemble",
      "accuracy_metrics": {
        "roc_auc": 0.92,
        "precision": 0.89,
        "recall": 0.87,
        "f1_score": 0.88
      },
      "last_training_date": "2024-03-01T00:00:00Z",
      "next_retraining_scheduled": "2024-04-01T00:00:00Z"
    },
    "regulatory_compliance": {
      "gdpr_compliant": true,
      "data_retention_days": 365,
      "processing_lawful_basis": "legitimate_interest",
      "automated_decision_making": true,
      "human_oversight_available": true
    },
    "performance_metrics": {
      "processing_time_ms": 147,
      "data_sources_used": [
        "open_banking_api",
        "telco_data",
        "digital_footprint",
        "employment_verification"
      ],
      "confidence_threshold_met": true
    }
  },
  "metadata": {
    "api_version": "v2.1",
    "endpoint": "/scoring/evaluate",
    "response_format": "JSON",
    "rate_limit_remaining": 9987,
    "rate_limit_reset": "2024-03-15T15:00:00Z"
  }
}
```
