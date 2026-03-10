# **ANEXO A: Arquitectura Técnica Detallada**

## **A.1 Arquitectura General del Sistema**

### **A.1.1 Vista General de la Arquitectura**

#### **Diagrama de Arquitectura Completa**
```mermaid
graph TB
    subgraph "Capa de Presentación"
        WEB[Web Dashboard]
        API_CLIENT[API Clients]
        MOBILE[Mobile App]
    end
    
    subgraph "Capa de Gateway"
        NGINX[Nginx Load Balancer]
        KONG[Kong API Gateway]
    end
    
    subgraph "Microservicios Principales"
        AUTH[Auth Service]
        SCORING[Scoring Service]
        DATA_INGESTION[Data Ingestion Service]
        ANALYTICS[Analytics Service]
        NOTIFICATION[Notification Service]
    end
    
    subgraph "Capa de Datos"
        POSTGRES[(PostgreSQL)]
        MONGODB[(MongoDB)]
        REDIS[(Redis Cache)]
        KAFKA[Apache Kafka]
        S3[Amazon S3]
    end
    
    subgraph "Capa de ML/AI"
        FEATURE_STORE[Feature Store]
        ML_PIPELINE[ML Pipeline]
        SHAP_SERVICE[SHAP Service]
    end
    
    WEB --> NGINX
    API_CLIENT --> NGINX
    MOBILE --> NGINX
    
    NGINX --> KONG
    KONG --> AUTH
    KONG --> SCORING
    KONG --> ANALYTICS
    
    AUTH --> POSTGRES
    SCORING --> FEATURE_STORE
    SCORING --> SHAP_SERVICE
    DATA_INGESTION --> KAFKA
    ANALYTICS --> MONGODB
    
    FEATURE_STORE --> POSTGRES
    FEATURE_STORE --> REDIS
    ML_PIPELINE --> S3
    SHAP_SERVICE --> MONGODB
```

### **A.1.2 Especificaciones Técnicas por Componente**

#### **A.1.2.1 API Gateway (Kong + Nginx)**
```yaml
# docker-compose.yml - API Gateway
version: '3.8'
services:
  nginx:
    image: nginx:1.21
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - kong

  kong:
    image: kong:3.4
    environment:
      KONG_DATABASE: "off"
      KONG_DECLARATIVE_CONFIG: "/kong/declarative/kong.yml"
      KONG_PROXY_ACCESS_LOG: "/dev/stdout"
      KONG_ADMIN_ACCESS_LOG: "/dev/stdout"
      KONG_PROXY_ERROR_LOG: "/dev/stderr"
      KONG_ADMIN_ERROR_LOG: "/dev/stderr"
      KONG_ADMIN_LISTEN: "0.0.0.0:8001"
    volumes:
      - ./kong.yml:/kong/declarative/kong.yml
    ports:
      - "8000:8000"
      - "8001:8001"
      - "8443:8443"
      - "8444:8444"
```

```yaml
# kong.yml - Configuración Kong
_format_version: "3.0"
_transform:
  - tag: null
  - value_type: text
services:
  - name: auth-service
    url: http://auth-service:8001
    routes:
    - name: auth-routes
      paths:
      - /auth
      methods:
      - POST
      - GET
      - PUT
      - DELETE
    plugins:
    - name: rate-limiting
      config:
        minute: 100
        hour: 1000
        fault_tolerant: true
  - name: scoring-service
    url: http://scoring-service:8002
    routes:
    - name: scoring-routes
      paths:
      - /score
      - /explain
      methods:
      - POST
    plugins:
    - name: request-size-limiting
      config:
        allowed_payload_size: 5
    - name: prometheus
      config:
        per_consumer: true
```

#### **A.1.2.2 Auth Service (Python + FastAPI)**
```python
# auth_service.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from datetime import datetime, timedelta
import jwt
import bcrypt
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import redis

app = FastAPI(title="PFM Velmak Auth Service", version="1.0.0")

# Configuración
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Base de datos
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgres:5432/pfm_auth"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Redis
redis_client = redis.Redis(host='redis', port=6379, db=0)

# Modelos
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int

class UserCreate(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

# Funciones de autenticación
def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_password_hash(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Endpoints
@app.post("/auth/register", response_model=Token)
async def register(user: UserCreate):
    db = SessionLocal()
    
    # Verificar si el usuario ya existe
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Crear nuevo usuario
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Generar token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    # Cachear en Redis
    redis_client.setex(f"token:{user.email}", ACCESS_TOKEN_EXPIRE_MINUTES * 60, access_token)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }

@app.post("/auth/login", response_model=Token)
async def login(user: UserLogin):
    db = SessionLocal()
    
    # Verificar usuario
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    # Generar token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
```

#### **A.1.2.3 Scoring Service (Python + FastAPI)**
```python
# scoring_service.py
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, List, Optional
import pandas as pd
import numpy as np
import joblib
import shap
from datetime import datetime
import asyncio
import redis
from prometheus_client import Counter, Histogram, generate_latest

app = FastAPI(title="PFM Velmak Scoring Service", version="1.0.0")

# Métricas Prometheus
REQUEST_COUNT = Counter('scoring_requests_total', 'Total scoring requests', ['method', 'endpoint'])
REQUEST_DURATION = Histogram('scoring_request_duration_seconds', 'Scoring request duration')

# Redis cache
redis_client = redis.Redis(host='redis', port=6379, db=0)

# Modelos cargados
model = joblib.load('/models/xgboost_model.pkl')
preprocessor = joblib.load('/models/preprocessor.pkl')
explainer = shap.TreeExplainer(model)

# Modelos Pydantic
class ScoringRequest(BaseModel):
    customer_id: str
    features: Dict[str, float]
    request_id: Optional[str] = None
    priority: Optional[str] = "normal"  # normal, high, urgent

class ScoringResponse(BaseModel):
    customer_id: str
    score: float
    risk_level: str
    confidence: float
    explanation: Dict[str, float]
    processing_time_ms: float
    request_id: str
    timestamp: str

class BatchScoringRequest(BaseModel):
    customers: List[Dict[str, float]]
    batch_id: str
    priority: Optional[str] = "normal"

class BatchScoringResponse(BaseModel):
    batch_id: str
    results: List[ScoringResponse]
    total_processed: int
    processing_time_ms: float
    timestamp: str

# Funciones auxiliares
def determine_risk_level(score: float) -> str:
    if score >= 800:
        return "Mínimo"
    elif score >= 650:
        return "Bajo"
    elif score >= 500:
        return "Medio"
    else:
        return "Alto"

def calculate_confidence(score: float) -> float:
    # Basado en la distancia al umbral de decisión
    if score >= 750:
        return min(0.95, 0.5 + (score - 750) / 500)
    elif score <= 400:
        return min(0.95, 0.5 + (400 - score) / 500)
    else:
        return 0.5

def generate_shap_explanation(features: Dict[str, float]) -> Dict[str, float]:
    # Convertir a DataFrame
    df = pd.DataFrame([features])
    
    # Preprocesar
    X_processed = preprocessor.transform(df)
    
    # Calcular SHAP values
    shap_values = explainer.shap_values(X_processed)
    
    # Mapear a nombres de características
    feature_names = preprocessor.get_feature_names_out()
    shap_dict = dict(zip(feature_names, shap_values[0]))
    
    return shap_dict

# Endpoints
@app.post("/score", response_model=ScoringResponse)
async def calculate_score(
    request: ScoringRequest,
    background_tasks: BackgroundTasks
):
    start_time = datetime.now()
    REQUEST_COUNT.labels(method="POST", endpoint="/score").inc()
    
    with REQUEST_DURATION.time():
        # Generar request_id si no se proporciona
        request_id = request.request_id or f"req_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{request.customer_id}"
        
        # Verificar cache
        cache_key = f"score:{request.customer_id}:{hash(str(request.features))}"
        cached_result = redis_client.get(cache_key)
        
        if cached_result:
            return ScoringResponse.parse_raw(cached_result)
        
        try:
            # Preprocesar features
            df = pd.DataFrame([request.features])
            X_processed = preprocessor.transform(df)
            
            # Calcular score
            score = float(model.predict(X_processed)[0])
            
            # Determinar riesgo y confianza
            risk_level = determine_risk_level(score)
            confidence = calculate_confidence(score)
            
            # Generar explicación
            explanation = generate_shap_explanation(request.features)
            
            # Calcular tiempo de procesamiento
            processing_time = (datetime.now() - start_time).total_seconds() * 1000
            
            # Crear respuesta
            response = ScoringResponse(
                customer_id=request.customer_id,
                score=score,
                risk_level=risk_level,
                confidence=confidence,
                explanation=explanation,
                processing_time_ms=processing_time,
                request_id=request_id,
                timestamp=datetime.now().isoformat()
            )
            
            # Cachear resultado (5 minutos)
            redis_client.setex(cache_key, 300, response.json())
            
            # Background task: logging
            background_tasks.add_task(log_scoring_request, request, response)
            
            return response
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Scoring error: {str(e)}")

@app.post("/score/batch", response_model=BatchScoringResponse)
async def calculate_batch_score(request: BatchScoringRequest):
    start_time = datetime.now()
    REQUEST_COUNT.labels(method="POST", endpoint="/score/batch").inc()
    
    with REQUEST_DURATION.time():
        results = []
        
        # Verificar cache para batch
        cache_key = f"batch:{hash(str(request.customers))}"
        cached_result = redis_client.get(cache_key)
        
        if cached_result:
            return BatchScoringResponse.parse_raw(cached_result)
        
        try:
            # Procesar cada cliente
            for i, customer_data in enumerate(request.customers):
                customer_id = f"customer_{i}"
                
                # Crear request individual
                individual_request = ScoringRequest(
                    customer_id=customer_id,
                    features=customer_data,
                    request_id=f"{request.batch_id}_{customer_id}"
                )
                
                # Calcular score
                result = await calculate_score(individual_request, BackgroundTasks())
                results.append(result)
            
            # Calcular tiempo total
            processing_time = (datetime.now() - start_time).total_seconds() * 1000
            
            # Crear respuesta batch
            response = BatchScoringResponse(
                batch_id=request.batch_id,
                results=results,
                total_processed=len(results),
                processing_time_ms=processing_time,
                timestamp=datetime.now().isoformat()
            )
            
            # Cachear resultado (10 minutos)
            redis_client.setex(cache_key, 600, response.json())
            
            return response
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Batch scoring error: {str(e)}")

@app.get("/metrics")
async def metrics():
    return generate_latest()

# Background tasks
async def log_scoring_request(request: ScoringRequest, response: ScoringResponse):
    """Logging asíncrono de solicitudes de scoring"""
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "customer_id": request.customer_id,
        "request_id": response.request_id,
        "score": response.score,
        "risk_level": response.risk_level,
        "processing_time_ms": response.processing_time_ms
    }
    
    # Enviar a sistema de logging (Elasticsearch, etc.)
    print(f"Scoring request logged: {log_data}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
```

### **A.2 Configuración de Infraestructura**

#### **A.2.1 Kubernetes Deployment**
```yaml
# k8s/scoring-service.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: scoring-service
  labels:
    app: scoring-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: scoring-service
  template:
    metadata:
      labels:
        app: scoring-service
    spec:
      containers:
      - name: scoring-service
        image: pfm-velmak/scoring-service:latest
        ports:
        - containerPort: 8002
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: pfm-secrets
              key: database-url
        - name: REDIS_URL
          valueFrom:
            configMapKeyRef:
              name: pfm-config
              key: redis-url
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8002
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8002
          initialDelaySeconds: 5
          periodSeconds: 5

---
apiVersion: v1
kind: Service
metadata:
  name: scoring-service
spec:
  selector:
    app: scoring-service
  ports:
  - protocol: TCP
    port: 8002
    targetPort: 8002
  type: ClusterIP

---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: scoring-service-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: scoring-service
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

#### **A.2.2 Monitoring con Prometheus y Grafana**
```yaml
# monitoring/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "pfm_rules.yml"

scrape_configs:
  - job_name: 'scoring-service'
    static_configs:
      - targets: ['scoring-service:8002']
    metrics_path: /metrics
    scrape_interval: 5s

  - job_name: 'kong'
    static_configs:
      - targets: ['kong:8001']
    metrics_path: /metrics

  - job_name: 'nginx'
    static_configs:
      - targets: ['nginx:9113']

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093
```

```yaml
# monitoring/pfm_rules.yml
groups:
  - name: pfm_alerts
    rules:
      - alert: HighLatency
        expr: scoring_request_duration_seconds{quantile="0.95"} > 0.1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High latency detected in scoring service"
          description: "95th percentile latency is {{ $value }}s"

      - alert: HighErrorRate
        expr: rate(scoring_requests_total{status=~"5.."}[5m]) / rate(scoring_requests_total[5m]) > 0.05
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "High error rate in scoring service"
          description: "Error rate is {{ $value | humanizePercentage }}"

      - alert: LowThroughput
        expr: rate(scoring_requests_total[5m]) < 10
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Low throughput detected"
          description: "Throughput is {{ $value }} requests/second"
```

### **A.3 Configuración de Base de Datos**

#### **A.3.1 PostgreSQL Schema**
```sql
-- Schema para PFM Velmak
CREATE DATABASE pfm_velmak;

-- Tabla de usuarios
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    role VARCHAR(50) DEFAULT 'user'
);

-- Tabla de solicitudes de scoring
CREATE TABLE scoring_requests (
    id SERIAL PRIMARY KEY,
    customer_id VARCHAR(255) NOT NULL,
    request_id VARCHAR(255) UNIQUE NOT NULL,
    features JSONB NOT NULL,
    score DECIMAL(10,2) NOT NULL,
    risk_level VARCHAR(50) NOT NULL,
    confidence DECIMAL(5,4) NOT NULL,
    explanation JSONB,
    processing_time_ms DECIMAL(10,2),
    status VARCHAR(50) DEFAULT 'completed',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    user_id INTEGER REFERENCES users(id)
);

-- Tabla de modelos
CREATE TABLE ml_models (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    version VARCHAR(50) NOT NULL,
    model_type VARCHAR(100) NOT NULL,
    accuracy DECIMAL(5,4),
    precision DECIMAL(5,4),
    recall DECIMAL(5,4),
    roc_auc DECIMAL(5,4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    file_path VARCHAR(500)
);

-- Tabla de features
CREATE TABLE features (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    data_type VARCHAR(50) NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de feature_store
CREATE TABLE feature_store (
    id SERIAL PRIMARY KEY,
    customer_id VARCHAR(255) NOT NULL,
    feature_id INTEGER REFERENCES features(id),
    value DECIMAL(15,6),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    UNIQUE(customer_id, feature_id)
);

-- Índices
CREATE INDEX idx_scoring_requests_customer_id ON scoring_requests(customer_id);
CREATE INDEX idx_scoring_requests_created_at ON scoring_requests(created_at);
CREATE INDEX idx_feature_store_customer_id ON feature_store(customer_id);
CREATE INDEX idx_feature_store_feature_id ON feature_store(feature_id);
CREATE INDEX idx_feature_store_expires_at ON feature_store(expires_at);

-- Triggers para actualización automática
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at 
    BEFORE UPDATE ON users 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

#### **A.3.2 MongoDB Collections**
```javascript
// MongoDB Collections para PFM Velmak

// Collection: analytics_events
db.createCollection("analytics_events", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["event_type", "timestamp", "customer_id", "data"],
      properties: {
        event_type: {
          bsonType: "string",
          enum: ["scoring_request", "model_training", "system_alert"]
        },
        timestamp: {
          bsonType: "date"
        },
        customer_id: {
          bsonType: "string"
        },
        data: {
          bsonType: "object"
        }
      }
    }
  }
});

// Collection: shap_explanations
db.createCollection("shap_explanations", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["customer_id", "request_id", "explanation", "created_at"],
      properties: {
        customer_id: {
          bsonType: "string"
        },
        request_id: {
          bsonType: "string"
        },
        explanation: {
          bsonType: "object"
        },
        created_at: {
          bsonType: "date"
        }
      }
    }
  }
});

// Índices
db.analytics_events.createIndex({ "customer_id": 1, "timestamp": -1 });
db.analytics_events.createIndex({ "event_type": 1, "timestamp": -1 });
db.shap_explanations.createIndex({ "customer_id": 1 });
db.shap_explanations.createIndex({ "request_id": 1 });
```

### **A.4 Configuración de Streaming**

#### **A.4.1 Apache Kafka Configuration**
```properties
# kafka/server.properties
broker.id=1
listeners=PLAINTEXT://:9092
log.dirs=/var/kafka-logs
num.network.threads=3
num.io.threads=8
socket.send.buffer.bytes=102400
socket.receive.buffer.bytes=102400
socket.request.max.bytes=104857600
num.partitions=3
num.recovery.threads.per.data.dir=1
offsets.topic.replication.factor=1
transaction.state.log.replication.factor=1
transaction.state.log.min.isr=1
log.retention.hours=168
log.segment.bytes=1073741824
log.retention.check.interval.ms=300000
zookeeper.connect=zookeeper:2181
zookeeper.connection.timeout.ms=18000
group.initial.rebalance.delay.ms=0
```

```python
# kafka_producer.py
from kafka import KafkaProducer
import json
import asyncio
from datetime import datetime

class PFMKafkaProducer:
    def __init__(self, bootstrap_servers=['kafka:9092']):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda k: k.encode('utf-8') if k else None,
            acks='all',
            retries=3,
            batch_size=16384,
            linger_ms=10,
            buffer_memory=33554432
        )
    
    async def send_scoring_request(self, request_data):
        """Enviar solicitud de scoring a Kafka"""
        topic = 'scoring-requests'
        key = request_data.get('customer_id')
        
        message = {
            'request_id': request_data['request_id'],
            'customer_id': request_data['customer_id'],
            'features': request_data['features'],
            'timestamp': datetime.now().isoformat(),
            'priority': request_data.get('priority', 'normal')
        }
        
        try:
            future = self.producer.send(topic, key=key, value=message)
            record_metadata = await asyncio.wrap_future(future)
            
            print(f"Message sent to {record_metadata.topic} [{record_metadata.partition}] at offset {record_metadata.offset}")
            return record_metadata
            
        except Exception as e:
            print(f"Error sending message: {e}")
            raise
    
    async def send_analytics_event(self, event_type, customer_id, data):
        """Enviar evento de analytics"""
        topic = 'analytics-events'
        key = customer_id
        
        message = {
            'event_type': event_type,
            'customer_id': customer_id,
            'timestamp': datetime.now().isoformat(),
            'data': data
        }
        
        try:
            future = self.producer.send(topic, key=key, value=message)
            record_metadata = await asyncio.wrap_future(future)
            return record_metadata
            
        except Exception as e:
            print(f"Error sending analytics event: {e}")
            raise
    
    def close(self):
        self.producer.close()

# Uso del producer
async def main():
    producer = PFMKafkaProducer()
    
    # Enviar solicitud de scoring
    request_data = {
        'request_id': 'req_12345',
        'customer_id': 'cust_67890',
        'features': {
            'edad': 35,
            'ingresos_mensuales': 3500,
            'deuda_existente': 500
        },
        'priority': 'high'
    }
    
    await producer.send_scoring_request(request_data)
    
    # Enviar evento de analytics
    await producer.send_analytics_event(
        'scoring_completed',
        'cust_67890',
        {'score': 750, 'risk_level': 'Bajo', 'processing_time': 45}
    )
    
    producer.close()

if __name__ == "__main__":
    asyncio.run(main())
```

---

## **A.5 Configuración de Deployment**

### **A.5.1 Docker Compose Completo**
```yaml
# docker-compose.yml
version: '3.8'

services:
  # Base de datos PostgreSQL
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: pfm_velmak
      POSTGRES_USER: pfm_user
      POSTGRES_PASSWORD: pfm_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./scripts/init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    networks:
      - pfm-network

  # MongoDB
  mongodb:
    image: mongo:6.0
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: admin_password
      MONGO_INITDB_DATABASE: pfm_analytics
    volumes:
      - mongodb_data:/data/db
    ports:
      - "27017:27017"
    networks:
      - pfm-network

  # Redis Cache
  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"
    networks:
      - pfm-network

  # Apache Zookeeper
  zookeeper:
    image: confluentinc/cp-zookeeper:7.3.0
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000
    networks:
      - pfm-network

  # Apache Kafka
  kafka:
    image: confluentinc/cp-kafka:7.3.0
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
    volumes:
      - kafka_data:/var/lib/kafka/data
    networks:
      - pfm-network

  # Nginx Load Balancer
  nginx:
    image: nginx:1.21-alpine
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/ssl:/etc/nginx/ssl
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - kong
    networks:
      - pfm-network

  # Kong API Gateway
  kong:
    image: kong:3.4
    environment:
      KONG_DATABASE: "off"
      KONG_DECLARATIVE_CONFIG: "/kong/declarative/kong.yml"
      KONG_PROXY_ACCESS_LOG: "/dev/stdout"
      KONG_ADMIN_ACCESS_LOG: "/dev/stdout"
      KONG_PROXY_ERROR_LOG: "/dev/stderr"
      KONG_ADMIN_ERROR_LOG: "/dev/stderr"
      KONG_ADMIN_LISTEN: "0.0.0.0:8001"
    volumes:
      - ./kong/kong.yml:/kong/declarative/kong.yml
    ports:
      - "8000:8000"
      - "8001:8001"
      - "8443:8443"
      - "8444:8444"
    depends_on:
      - postgres
      - redis
    networks:
      - pfm-network

  # Auth Service
  auth-service:
    build: ./services/auth-service
    environment:
      DATABASE_URL: postgresql://pfm_user:pfm_password@postgres:5432/pfm_auth
      REDIS_URL: redis://redis:6379
      SECRET_KEY: your-secret-key
    depends_on:
      - postgres
      - redis
    ports:
      - "8001:8001"
    networks:
      - pfm-network

  # Scoring Service
  scoring-service:
    build: ./services/scoring-service
    environment:
      DATABASE_URL: postgresql://pfm_user:pfm_password@postgres:5432/pfm_velmak
      REDIS_URL: redis://redis:6379
      MONGODB_URL: mongodb://admin:admin_password@mongodb:27017/pfm_analytics
      KAFKA_BOOTSTRAP_SERVERS: kafka:9092
    volumes:
      - ./models:/models
    depends_on:
      - postgres
      - redis
      - mongodb
      - kafka
    ports:
      - "8002:8002"
    networks:
      - pfm-network

  # Data Ingestion Service
  data-ingestion:
    build: ./services/data-ingestion
    environment:
      KAFKA_BOOTSTRAP_SERVERS: kafka:9092
      MONGODB_URL: mongodb://admin:admin_password@mongodb:27017/pfm_analytics
      POSTGRES_URL: postgresql://pfm_user:pfm_password@postgres:5432/pfm_velmak
    depends_on:
      - kafka
      - mongodb
      - postgres
    networks:
      - pfm-network

  # Analytics Service
  analytics-service:
    build: ./services/analytics-service
    environment:
      MONGODB_URL: mongodb://admin:admin_password@mongodb:27017/pfm_analytics
      POSTGRES_URL: postgresql://pfm_user:pfm_password@postgres:5432/pfm_velmak
    depends_on:
      - mongodb
      - postgres
    ports:
      - "8003:8003"
    networks:
      - pfm-network

  # Prometheus
  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - ./monitoring/pfm_rules.yml:/etc/prometheus/pfm_rules.yml
      - prometheus_data:/prometheus
    ports:
      - "9090:9090"
    networks:
      - pfm-network

  # Grafana
  grafana:
    image: grafana/grafana:latest
    environment:
      GF_SECURITY_ADMIN_PASSWORD: admin
    volumes:
      - grafana_data:/var/lib/grafana
      - ./monitoring/grafana/dashboards:/etc/grafana/provisioning/dashboards
      - ./monitoring/grafana/datasources:/etc/grafana/provisioning/datasources
    ports:
      - "3000:3000"
    depends_on:
      - prometheus
    networks:
      - pfm-network

  # Alertmanager
  alertmanager:
    image: prom/alertmanager:latest
    volumes:
      - ./monitoring/alertmanager.yml:/etc/alertmanager/alertmanager.yml
      - alertmanager_data:/alertmanager
    ports:
      - "9093:9093"
    networks:
      - pfm-network

volumes:
  postgres_data:
  mongodb_data:
  redis_data:
  kafka_data:
  prometheus_data:
  grafana_data:
  alertmanager_data:

networks:
  pfm-network:
    driver: bridge
```

---

## **A.6 Configuración de Seguridad**

### **A.6.1 SSL/TLS Configuration**
```nginx
# nginx/nginx.conf
events {
    worker_connections 1024;
}

http {
    # Configuración SSL
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # Headers de seguridad
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    upstream kong_backend {
        server kong:8000;
    }

    server {
        listen 80;
        server_name pfm-velmak.com;
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name pfm-velmak.com;

        ssl_certificate /etc/nginx/ssl/pfm-velmak.crt;
        ssl_certificate_key /etc/nginx/ssl/pfm-velmak.key;

        location / {
            proxy_pass http://kong_backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

### **A.6.2 Network Policies (Kubernetes)**
```yaml
# k8s/network-policies.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: pfm-network-policy
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    ports:
    - protocol: TCP
      port: 8000
    - protocol: TCP
      port: 8001
    - protocol: TCP
      port: 8002
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          name: database
    ports:
    - protocol: TCP
      port: 5432
    - protocol: TCP
      port: 27017
    - protocol: TCP
      port: 6379
    - protocol: TCP
      port: 9092
```

---

## **A.7 Performance Optimization**

### **A.7.1 Caching Strategy**
```python
# cache_manager.py
import redis
import json
import pickle
from typing import Any, Optional
from datetime import timedelta

class CacheManager:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
        self.default_ttl = 300  # 5 minutos

    def get(self, key: str) -> Optional[Any]:
        """Obtener valor del cache"""
        try:
            value = self.redis.get(key)
            if value:
                return pickle.loads(value)
            return None
        except Exception as e:
            print(f"Cache get error: {e}")
            return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Establecer valor en cache"""
        try:
            ttl = ttl or self.default_ttl
            serialized_value = pickle.dumps(value)
            return self.redis.setex(key, ttl, serialized_value)
        except Exception as e:
            print(f"Cache set error: {e}")
            return False

    def delete(self, key: str) -> bool:
        """Eliminar valor del cache"""
        try:
            return bool(self.redis.delete(key))
        except Exception as e:
            print(f"Cache delete error: {e}")
            return False

    def invalidate_pattern(self, pattern: str) -> int:
        """Invalidar keys por patrón"""
        try:
            keys = self.redis.keys(pattern)
            if keys:
                return self.redis.delete(*keys)
            return 0
        except Exception as e:
            print(f"Cache invalidate pattern error: {e}")
            return 0

# Uso del cache manager
cache = CacheManager(redis_client)

# Cache de resultados de scoring
def get_cached_score(customer_id: str, features_hash: str) -> Optional[dict]:
    cache_key = f"score:{customer_id}:{features_hash}"
    return cache.get(cache_key)

def set_cached_score(customer_id: str, features_hash: str, result: dict):
    cache_key = f"score:{customer_id}:{features_hash}"
    cache.set(cache_key, result, ttl=300)  # 5 minutos
```

### **A.7.2 Database Connection Pooling**
```python
# database.py
import asyncpg
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

class DatabaseManager:
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.engine = None
        self.session_factory = None

    async def initialize(self):
        """Inicializar pool de conexiones"""
        self.engine = create_async_engine(
            self.database_url,
            pool_size=20,
            max_overflow=30,
            pool_pre_ping=True,
            pool_recycle=3600,
            echo=False
        )
        
        self.session_factory = sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    async def get_session(self) -> AsyncSession:
        """Obtener sesión de base de datos"""
        async with self.session_factory() as session:
            try:
                yield session
            finally:
                await session.close()

    async def close(self):
        """Cerrar pool de conexiones"""
        if self.engine:
            await self.engine.dispose()

# Configuración de pool optimizado
DATABASE_URL = "postgresql+asyncpg://user:password@postgres:5432/pfm_velmak"

db_manager = DatabaseManager(DATABASE_URL)
```

---

## **A.8 Backup y Disaster Recovery**

### **A.8.1 Backup Strategy**
```bash
#!/bin/bash
# backup.sh

# Variables
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"
POSTGRES_CONTAINER="pfm_postgres_1"
MONGODB_CONTAINER="pfm_mongodb_1"

# Crear directorio de backup
mkdir -p $BACKUP_DIR/$DATE

# Backup PostgreSQL
echo "Iniciando backup PostgreSQL..."
docker exec $POSTGRES_CONTAINER pg_dump -U pfm_user pfm_velmak > $BACKUP_DIR/$DATE/postgres_backup.sql

# Backup MongoDB
echo "Iniciando backup MongoDB..."
docker exec $MONGODB_CONTAINER mongodump --db pfm_analytics --out /tmp/mongodb_backup
docker cp $MONGODB_CONTAINER:/tmp/mongodb_backup $BACKUP_DIR/$DATE/mongodb_backup

# Comprimir backups
echo "Comprimiendo backups..."
tar -czf $BACKUP_DIR/$DATE/pfm_backup.tar.gz -C $BACKUP_DIR/$DATE postgres_backup.sql mongodb_backup

# Limpiar backups antiguos (mantener últimos 7 días)
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "Backup completado: $BACKUP_DIR/$DATE/pfm_backup.tar.gz"
```

### **A.8.2 Recovery Procedures**
```bash
#!/bin/bash
# recovery.sh

BACKUP_FILE=$1
RECOVERY_DIR="/tmp/recovery_$(date +%Y%m%d_%H%M%S)"

if [ -z "$BACKUP_FILE" ]; then
    echo "Uso: $0 <backup_file.tar.gz>"
    exit 1
fi

# Crear directorio de recuperación
mkdir -p $RECOVERY_DIR

# Extraer backup
echo "Extrayendo backup..."
tar -xzf $BACKUP_FILE -C $RECOVERY_DIR

# Recuperar PostgreSQL
echo "Recuperando PostgreSQL..."
docker exec -i pfm_postgres_1 psql -U pfm_user pfm_velmak < $RECOVERY_DIR/postgres_backup.sql

# Recuperar MongoDB
echo "Recuperando MongoDB..."
docker cp $RECOVERY_DIR/mongodb_backup/pfm_analytics pfm_mongodb_1:/tmp/
docker exec pfm_mongodb_1 mongorestore --db pfm_analytics /tmp/pfm_analytics

echo "Recuperación completada"
```

---

## **A.9 Monitoring y Logging**

### **A.9.1 Structured Logging**
```python
# logging_config.py
import logging
import json
from datetime import datetime
from typing import Dict, Any

class StructuredLogger:
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Handler para JSON
        handler = logging.StreamHandler()
        formatter = StructuredFormatter()
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log_scoring_request(self, customer_id: str, request_id: str, 
                          score: float, processing_time: float):
        """Log estructurado para solicitud de scoring"""
        self.logger.info("scoring_request_completed", extra={
            "event_type": "scoring_request",
            "customer_id": customer_id,
            "request_id": request_id,
            "score": score,
            "processing_time_ms": processing_time,
            "timestamp": datetime.now().isoformat()
        })

class StructuredFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage()
        }
        
        # Agregar campos extra si existen
        if hasattr(record, '__dict__'):
            log_entry.update(record.__dict__)
        
        return json.dumps(log_entry)

# Uso del logger
logger = StructuredLogger("scoring_service")
```

---

## **A.10 Testing y Quality Assurance**

### **A.10.1 Unit Tests**
```python
# tests/test_scoring_service.py
import pytest
import asyncio
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
import json

from scoring_service import app, ScoringRequest, ScoringResponse

client = TestClient(app)

class TestScoringService:
    def test_health_check(self):
        """Test endpoint de salud"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_calculate_score_success(self):
        """Test cálculo de score exitoso"""
        request_data = {
            "customer_id": "test_customer",
            "features": {
                "edad": 35,
                "ingresos_mensuales": 3500,
                "deuda_existente": 500
            },
            "request_id": "test_request_123"
        }
        
        response = client.post("/score", json=request_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["customer_id"] == "test_customer"
        assert "score" in data
        assert "risk_level" in data
        assert 0 <= data["score"] <= 1000

    def test_calculate_score_invalid_features(self):
        """Test con features inválidos"""
        request_data = {
            "customer_id": "test_customer",
            "features": {
                "edad": "invalid",  # Debe ser número
                "ingresos_mensuales": 3500
            }
        }
        
        response = client.post("/score", json=request_data)
        assert response.status_code == 422

    @patch('scoring_service.redis_client')
    def test_cache_hit(self, mock_redis):
        """Test cache hit"""
        # Simular cache hit
        cached_response = ScoringResponse(
            customer_id="test_customer",
            score=750.0,
            risk_level="Bajo",
            confidence=0.85,
            explanation={"edad": 50.0, "ingresos": 30.0},
            processing_time_ms=25.0,
            request_id="test_request",
            timestamp="2024-01-01T00:00:00"
        )
        
        mock_redis.get.return_value = cached_response.json()
        
        request_data = {
            "customer_id": "test_customer",
            "features": {"edad": 35, "ingresos_mensuales": 3500}
        }
        
        response = client.post("/score", json=request_data)
        assert response.status_code == 200
        
        # Verificar que se usó el cache
        mock_redis.get.assert_called_once()

    def test_batch_scoring(self):
        """Test batch scoring"""
        request_data = {
            "batch_id": "test_batch",
            "customers": [
                {"edad": 35, "ingresos_mensuales": 3500},
                {"edad": 28, "ingresos_mensuales": 2800}
            ]
        }
        
        response = client.post("/score/batch", json=request_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["batch_id"] == "test_batch"
        assert len(data["results"]) == 2
        assert data["total_processed"] == 2

if __name__ == "__main__":
    pytest.main([__file__])
```

---

## **A.11 Deployment Automation**

### **A.11.1 CI/CD Pipeline**
```yaml
# .github/workflows/deploy.yml
name: Deploy PFM Velmak

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: test_password
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-asyncio
    
    - name: Run tests
      run: |
        pytest tests/ -v --cov=services --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3

  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2
    
    - name: Login to Docker Hub
      uses: docker/login-action@v2
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}
    
    - name: Build and push images
      run: |
        docker buildx build -t pfm-velmak/scoring-service:latest --push .
        docker buildx build -t pfm-velmak/auth-service:latest --push ./services/auth-service
        docker buildx build -t pfm-velmak/analytics-service:latest --push ./services/analytics-service

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to Kubernetes
      run: |
        echo "${{ secrets.KUBECONFIG }}" | base64 -d > kubeconfig
        export KUBECONFIG=kubeconfig
        
        kubectl apply -f k8s/
        kubectl rollout status deployment/scoring-service
        kubectl rollout status deployment/auth-service
        kubectl rollout status deployment/analytics-service
```

---

## **A.12 Security Best Practices**

### **A.12.1 Security Headers and Policies**
```python
# security.py
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

def setup_security_middleware(app: FastAPI):
    """Configurar middleware de seguridad"""
    
    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["https://pfm-velmak.com"],
        allow_credentials=True,
        allow_methods=["GET", "POST"],
        allow_headers=["*"],
    )
    
    # Trusted Hosts
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["pfm-velmak.com", "*.pfm-velmak.com"]
    )
    
    @app.middleware("http")
    async def add_security_headers(request: Request, call_next):
        response = await call_next(request)
        
        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        return response
```

---

## **A.13 Performance Monitoring**

### **A.13.1 Custom Metrics**
```python
# metrics.py
from prometheus_client import Counter, Histogram, Gauge, generate_latest
import time
import functools

# Métricas personalizadas
SCORING_REQUESTS_TOTAL = Counter(
    'scoring_requests_total',
    'Total number of scoring requests',
    ['method', 'endpoint', 'status']
)

SCORING_REQUEST_DURATION = Histogram(
    'scoring_request_duration_seconds',
    'Time spent processing scoring requests',
    ['method', 'endpoint'],
    buckets=[0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
)

ACTIVE_CONNECTIONS = Gauge(
    'active_connections',
    'Number of active connections'
)

MODEL_ACCURACY = Gauge(
    'model_accuracy',
    'Current model accuracy',
    ['model_name', 'model_version']
)

def track_performance(metric_name: str):
    """Decorator para track performance"""
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                SCORING_REQUESTS_TOTAL.labels(
                    method="POST", 
                    endpoint=metric_name, 
                    status="success"
                ).inc()
                return result
            except Exception as e:
                SCORING_REQUESTS_TOTAL.labels(
                    method="POST", 
                    endpoint=metric_name, 
                    status="error"
                ).inc()
                raise
            finally:
                duration = time.time() - start_time
                SCORING_REQUEST_DURATION.labels(
                    method="POST", 
                    endpoint=metric_name
                ).observe(duration)
        return wrapper
    return decorator

# Uso del decorator
@track_performance("calculate_score")
async def calculate_score(request: ScoringRequest):
    # Lógica de scoring
    pass
```

---

**FIN DEL ANEXO A: Arquitectura Técnica Detallada**

*Este anexo contiene la especificación técnica completa de la arquitectura del sistema PFM Velmak, incluyendo diagramas, configuraciones de deployment, estrategias de seguridad, y procedimientos de operación.*
