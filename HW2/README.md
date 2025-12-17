# 🪙 Crypto Price Caching Service  

## 🌟 Introduction

The Crypto Price Cache project is a scalable backend system designed to fetch, cache, and serve real-time cryptocurrency price data using Docker, Kubernetes, and Redis. The objective of this project is to demonstrate how a cloud-native application can be constructed and deployed in a Kubernetes environment with the integration of containerized services, load balancing, and caching.

This system operates in three stages:
1. Docker Image Creation: Building a lightweight image for testing the API endpoint.
2. Local Development: Running the Crypto API and Redis services with Docker Compose for testing.
3. Kubernetes Deployment: Deploying the application on a Kubernetes cluster with persistent storage, load balancing, and service discovery.

The project showcases how modern backend systems can handle high availability, scalability, and fault tolerance by leveraging distributed services such as Redis for caching and Kubernetes for orchestration.

> 🔧 **Note:**  
> Kubernetes nodes cannot access locally built Docker images.  
> Application images must be **tagged and pushed to Docker Hub** before deployment.

---

## 🚀 Overview

Crypto Price Cache is a containerized backend system that implements:

- Cryptocurrency Price API  
- Redis Caching for improved performance  
- Docker Compose for local development  
- Kubernetes deployment with load balancing and service discovery  

---
## 🏗️ Architecture

### 🔹 Crypto API
- Python-based REST API  
- Fetches live cryptocurrency prices from an external provider  
- Uses Redis to cache results with a configurable TTL  

### 🔹 Redis Cache
- Shared cache across API replicas  
- Backed by PersistentVolume (PV) and PersistentVolumeClaim (PVC) in Kubernetes  

### 🔹 curltest Pod
- Temporary debugging pod  
- Used to validate in-cluster networking, DNS, and load balancing  

---

## 📁 Project Structure

```
hw2-crypto-cache/
├── step1-curl-image/
│   ├── Dockerfile
│   └── README.md
│
├── step2-app/
│   ├── app/
│   ├── docker-compose.yml
│   └── Dockerfile
│
├── step3-k8s/
│   ├── app-configmap.yaml
│   ├── app-deployment.yaml
│   ├── app-service.yaml
│   ├── redis-deployment.yaml
│   ├── redis-service.yaml
│   ├── redis-pv.yaml
│   └── redis-pvc.yaml
│
└── README.md
```

---

## 🧪 Step 1 – curl Docker Image

This step builds a lightweight image containing `curl` and `wget`, which is later used for **in-cluster testing**.

### Build the image
```bash
docker build -t YOUR_DOCKERHUB_USERNAME/hw2-curl:1.0 .
```

Test the image locally:
```bash
docker run --rm YOUR_DOCKERHUB_USERNAME/hw2-curl:1.0
```

Push the image to Docker Hub:
```bash
docker push YOUR_DOCKERHUB_USERNAME/hw2-curl:1.0
```

---

## 🐳 Step 2 – Run with Docker Compose

This step runs the API and Redis **locally** for functional validation.

```bash
cd step2-app
docker compose up --build
```

### Test the API
```bash
curl http://localhost:8000/health
curl "http://localhost:8000/price?coin=bitcoin&currency=usd"
curl "http://localhost:8000/price?coin=bitcoin&currency=usd"
```

The second request should return:
```json
"cached": true
```

Stop local services:
```bash
docker compose down
```

Build and push the API image for Kubernetes:
```bash
docker build -t YOUR_DOCKERHUB_USERNAME/hw2-crypto-api:1.0 .
docker push YOUR_DOCKERHUB_USERNAME/hw2-crypto-api:1.0
```

---

## ☸️ Step 3 – Kubernetes Deployment (Minikube)

### Start Minikube
```bash
minikube start
kubectl get nodes
```

### Deploy resources

Update the image name in `step3-k8s/app-deployment.yaml`:
```yaml
image: YOUR_DOCKERHUB_USERNAME/hw2-crypto-api:1.0
```

Apply manifests:
```bash
kubectl apply -f step3-k8s/app-configmap.yaml
kubectl apply -f step3-k8s/redis-pv.yaml
kubectl apply -f step3-k8s/redis-pvc.yaml
kubectl apply -f step3-k8s/redis-deployment.yaml
kubectl apply -f step3-k8s/redis-service.yaml
kubectl apply -f step3-k8s/app-deployment.yaml
kubectl apply -f step3-k8s/app-service.yaml
```

Verify:
```bash
kubectl get pods -o wide
kubectl get svc
kubectl get pv,pvc
```

---

## 🔬 In-Cluster Testing

Load the curl image if needed:
```bash
minikube image load YOUR_DOCKERHUB_USERNAME/hw2-curl:1.0
```

Create test pod:
```bash
kubectl run curltest   --image=YOUR_DOCKERHUB_USERNAME/hw2-curl:1.0   --restart=Never --command -- sh -c "sleep 3600"
```

Exec into the pod:
```bash
kubectl exec -it curltest -- sh
```

Test the service:
```sh
for i in $(seq 1 10); do
  wget -qO- "http://crypto-api/price?coin=bitcoin&currency=usd"
  echo
done
```

---

## 🧹 Cleanup

```bash
kubectl delete pod curltest
kubectl delete -f step3-k8s
minikube stop
```

---

## 🏁 Conclusion

This project demonstrates Docker, Docker Compose, and Kubernetes fundamentals, including service discovery, persistent storage, and distributed caching using Redis. It provides a complete example of developing, containerizing, and deploying a cloud-native application.