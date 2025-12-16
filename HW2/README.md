# 🪙 HW2 – Crypto Price Cache  

## 🌟 Overview

This project implements a **containerized cryptocurrency price API** with **Redis-based caching**, developed as part of the **Cloud Computing** course homework.

The goal is to demonstrate how a **cloud-native application** can be built, containerized, and deployed step-by-step using **Docker** and **Kubernetes**.

🚀 The system is implemented in **three progressive stages**:

1️⃣ Building a custom Docker image for HTTP testing  
2️⃣ Running the API + Redis locally using **Docker Compose**  
3️⃣ Deploying the system on **Kubernetes (Minikube)** with:
- Replicated API pods  
- Persistent Redis storage  
- Service discovery & load balancing  

---

## 🏗️ Architecture Overview

### 🔹 Crypto API
- Python-based REST API  
- Fetches live cryptocurrency prices from an external provider  
- Uses Redis to cache results with a configurable TTL  

### 🔹 Redis Cache
- Shared cache across API replicas  
- Backed by **PersistentVolume (PV)** and **PersistentVolumeClaim (PVC)** in Kubernetes  

### 🔹 curltest Pod
- Temporary debugging pod  
- Used to validate **in-cluster networking**, DNS, and load balancing  

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

### Build the image
```bash
docker build -t hw2-curl:1.0 .
```

---

## 🐳 Step 2 – Run with Docker Compose

```bash
cd step2-app
docker compose up --build
```

### Test the API
```bash
curl http://localhost:8000/price
```

---

## ☸️ Step 3 – Kubernetes Deployment (Minikube)

### Start Minikube
```bash
minikube start
```

### Deploy resources
```bash
kubectl apply -f step3-k8s/app-configmap.yaml
kubectl apply -f step3-k8s/redis-pv.yaml
kubectl apply -f step3-k8s/redis-pvc.yaml
kubectl apply -f step3-k8s/redis-deployment.yaml
kubectl apply -f step3-k8s/redis-service.yaml
kubectl apply -f step3-k8s/app-deployment.yaml
kubectl apply -f step3-k8s/app-service.yaml
```

---

## 🔬 In-Cluster Testing

```bash
minikube image load hw2-curl:1.0
kubectl run curltest --image=hw2-curl:1.0 --restart=Never --command -- sh -c "sleep 3600"
kubectl exec -it curltest -- sh
```

```sh
for i in $(seq 1 10); do
  wget -qO- http://crypto-api/price
  echo
done
```

---

## 🧹 Cleanup

```bash
kubectl delete pod curltest
minikube stop
```

---

## 🏁 Conclusion

This project demonstrates Docker, Docker Compose, and Kubernetes fundamentals, including service discovery, persistence, and distributed caching using Redis.
