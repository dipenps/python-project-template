# Deployment Guide

## Overview

This document provides comprehensive instructions for deploying {{ project_name }} in various environments.

## Prerequisites

### System Requirements
- **Operating System**: Linux, macOS, or Windows (with WSL)
- **Python**: {{ python_version }} or later
- **Memory**: Minimum 2GB RAM, 4GB recommended
- **Storage**: Minimum 10GB free space
- **Network**: Internet access for dependency installation

### Required Tools
- **uv**: Package management tool
- **Docker**: For containerized deployment
- **kubectl**: For Kubernetes deployment
- **Git**: For source code management

## Local Development Deployment

### 1. Clone Repository
```bash
git clone https://github.com/{{ github_username }}/{{ project_slug }}.git
cd {{ project_slug }}
```

### 2. Install Dependencies
```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install project dependencies
uv sync

# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Configure Environment
```bash
# Copy example configuration
cp .env.example .env

# Edit configuration file
nano .env
```

### 4. Run Application
```bash
# Run the application
uv run {{ package_slug }} --config config.yaml

# Or run in development mode
uv run {{ package_slug }} --dev --config config.yaml
```

## Docker Deployment

### 1. Build Docker Image
```bash
# Build the Docker image
docker build -t {{ project_slug }}:latest .

# Tag for registry
docker tag {{ project_slug }}:latest your-registry.com/{{ project_slug }}:latest
```

### 2. Run Container
```bash
# Run with default configuration
docker run -d --name {{ project_slug }} -p 8000:8000 {{ project_slug }}:latest

# Run with custom configuration
docker run -d --name {{ project_slug }} \
  -p 8000:8000 \
  -v $(pwd)/config.yaml:/app/config.yaml \
  -e ENV=production \
  {{ project_slug }}:latest
```

### 3. Docker Compose
```yaml
version: '3.8'
services:
  {{ project_slug }}:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENV=production
    volumes:
      - ./config.yaml:/app/config.yaml
      - ./data:/app/data
      - ./logs:/app/logs
    restart: unless-stopped
```

## Kubernetes Deployment

### 1. Create Namespace
```bash
kubectl create namespace {{ project_slug }}
```

### 2. Create ConfigMap
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ project_slug }}-config
  namespace: {{ project_slug }}
data:
  config.yaml: |
    log_level: INFO
    max_agents: 100
    message_timeout: 30.0
    heartbeat_interval: 10.0
```

### 3. Create Secret
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: {{ project_slug }}-secrets
  namespace: {{ project_slug }}
type: Opaque
data:
  api-key: <base64-encoded-api-key>
  database-url: <base64-encoded-database-url>
```

### 4. Create Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ project_slug }}
  namespace: {{ project_slug }}
spec:
  replicas: 3
  selector:
    matchLabels:
      app: {{ project_slug }}
  template:
    metadata:
      labels:
        app: {{ project_slug }}
    spec:
      containers:
      - name: {{ project_slug }}
        image: {{ project_slug }}:latest
        ports:
        - containerPort: 8000
        env:
        - name: ENV
          value: "production"
        volumeMounts:
        - name: config
          mountPath: /app/config.yaml
          subPath: config.yaml
        - name: secrets
          mountPath: /app/secrets
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
      volumes:
      - name: config
        configMap:
          name: {{ project_slug }}-config
      - name: secrets
        secret:
          secretName: {{ project_slug }}-secrets
```

### 5. Create Service
```yaml
apiVersion: v1
kind: Service
metadata:
  name: {{ project_slug }}-service
  namespace: {{ project_slug }}
spec:
  selector:
    app: {{ project_slug }}
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

### 6. Deploy to Kubernetes
```bash
# Apply all configurations
kubectl apply -f k8s/

# Check deployment status
kubectl get pods -n {{ project_slug }}

# Check service
kubectl get svc -n {{ project_slug }}
```

## Cloud Deployment

### AWS Deployment

#### 1. ECS Deployment
```bash
# Create ECS cluster
aws ecs create-cluster --cluster-name {{ project_slug }}-cluster

# Create task definition
aws ecs register-task-definition --cli-input-json file://task-definition.json

# Create service
aws ecs create-service \
  --cluster {{ project_slug }}-cluster \
  --service-name {{ project_slug }}-service \
  --task-definition {{ project_slug }}-task \
  --desired-count 3
```

#### 2. EKS Deployment
```bash
# Create EKS cluster
eksctl create cluster --name {{ project_slug }}-cluster --region us-west-2

# Deploy application
kubectl apply -f k8s/
```

### Google Cloud Deployment

#### 1. GKE Deployment
```bash
# Create GKE cluster
gcloud container clusters create {{ project_slug }}-cluster \
  --zone us-central1-a \
  --num-nodes 3

# Deploy application
kubectl apply -f k8s/
```

#### 2. Cloud Run Deployment
```bash
# Build and push image
gcloud builds submit --tag gcr.io/PROJECT_ID/{{ project_slug }}

# Deploy to Cloud Run
gcloud run deploy {{ project_slug }} \
  --image gcr.io/PROJECT_ID/{{ project_slug }} \
  --platform managed \
  --region us-central1
```

### Azure Deployment

#### 1. AKS Deployment
```bash
# Create AKS cluster
az aks create \
  --resource-group myResourceGroup \
  --name {{ project_slug }}-cluster \
  --node-count 3 \
  --enable-addons monitoring

# Deploy application
kubectl apply -f k8s/
```

## Production Deployment

### 1. Environment Setup
```bash
# Set production environment variables
export ENV=production
export LOG_LEVEL=INFO
export MAX_AGENTS=100
export MESSAGE_TIMEOUT=30.0
```

### 2. Security Configuration
```bash
# Generate secure secrets
openssl rand -base64 32 > api-key.txt
openssl rand -base64 32 > database-key.txt

# Set file permissions
chmod 600 api-key.txt database-key.txt
```

### 3. Monitoring Setup
```bash
# Install monitoring tools
helm install prometheus prometheus-community/prometheus
helm install grafana grafana/grafana

# Configure alerts
kubectl apply -f monitoring/alerts.yaml
```

### 4. Backup Configuration
```bash
# Create backup script
cat > backup.sh << 'EOF'
#!/bin/bash
# Backup configuration and data
kubectl get configmap {{ project_slug }}-config -o yaml > backup/config-$(date +%Y%m%d).yaml
kubectl get secret {{ project_slug }}-secrets -o yaml > backup/secrets-$(date +%Y%m%d).yaml
EOF

chmod +x backup.sh
```

## Health Checks

### 1. Application Health
```bash
# Check application status
curl http://localhost:8000/health

# Check readiness
curl http://localhost:8000/ready

# Check metrics
curl http://localhost:8000/metrics
```

### 2. Kubernetes Health
```bash
# Check pod status
kubectl get pods -n {{ project_slug }}

# Check service status
kubectl get svc -n {{ project_slug }}

# Check logs
kubectl logs -f deployment/{{ project_slug }} -n {{ project_slug }}
```

## Troubleshooting

### Common Issues

#### 1. Application Won't Start
```bash
# Check logs
kubectl logs deployment/{{ project_slug }} -n {{ project_slug }}

# Check configuration
kubectl describe configmap {{ project_slug }}-config -n {{ project_slug }}

# Check secrets
kubectl describe secret {{ project_slug }}-secrets -n {{ project_slug }}
```

#### 2. Performance Issues
```bash
# Check resource usage
kubectl top pods -n {{ project_slug }}

# Check metrics
curl http://localhost:8000/metrics

# Check logs for errors
kubectl logs deployment/{{ project_slug }} -n {{ project_slug }} | grep ERROR
```

#### 3. Network Issues
```bash
# Check service endpoints
kubectl get endpoints -n {{ project_slug }}

# Test connectivity
kubectl run test-pod --image=busybox --rm -it -- wget -qO- http://{{ project_slug }}-service:80/health
```

## Rollback Procedures

### 1. Application Rollback
```bash
# Rollback to previous version
kubectl rollout undo deployment/{{ project_slug }} -n {{ project_slug }}

# Check rollback status
kubectl rollout status deployment/{{ project_slug }} -n {{ project_slug }}
```

### 2. Configuration Rollback
```bash
# Restore previous configuration
kubectl apply -f backup/config-$(date -d '1 day ago' +%Y%m%d).yaml

# Restart deployment
kubectl rollout restart deployment/{{ project_slug }} -n {{ project_slug }}
```

## Maintenance

### 1. Regular Updates
```bash
# Update dependencies
uv sync --upgrade

# Update Docker image
docker build -t {{ project_slug }}:latest .
docker push your-registry.com/{{ project_slug }}:latest

# Update deployment
kubectl set image deployment/{{ project_slug }} {{ project_slug }}=your-registry.com/{{ project_slug }}:latest -n {{ project_slug }}
```

### 2. Backup and Recovery
```bash
# Create backup
./backup.sh

# Test recovery
kubectl apply -f backup/config-$(date +%Y%m%d).yaml
kubectl apply -f backup/secrets-$(date +%Y%m%d).yaml
```

### 3. Monitoring and Alerting
```bash
# Check system health
kubectl get pods -n {{ project_slug }}
kubectl top pods -n {{ project_slug }}

# Check logs
kubectl logs deployment/{{ project_slug }} -n {{ project_slug }} --tail=100
```

