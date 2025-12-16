# ☁️ Cloud Ads Starter

A **cloud-native advertisement processing system** built with **FastAPI**, **Docker**, and **event-driven microservices**.  
This project demonstrates how modern cloud applications handle **file uploads, async processing, object storage, and messaging** using open-source tools.

---

## 🚀 Overview

**Cloud Ads Starter** is a simplified cloud backend for creating advertisements that include image uploads.  
It is designed to showcase:

- Microservice architecture  
- Asynchronous task processing  
- S3-compatible object storage  
- Message queues  
- Containerized deployment  

---

## 🧩 Architecture

```
Client
  │
  ▼
FastAPI (API Service)
  │
  ├── PostgreSQL (metadata)
  ├── MinIO (image storage – S3 compatible)
  └── RabbitMQ (event queue)
          │
          ▼
     Worker Service
       ├── Image tagging (Imagga)
       └── Email notifications (Mailgun)
```

---

## 🛠️ Tech Stack

| Component        | Technology |
|------------------|------------|
| API              | FastAPI + Uvicorn |
| Worker           | Python |
| Database         | PostgreSQL |
| Object Storage   | MinIO (S3 compatible) |
| Message Queue    | RabbitMQ |
| Image Tagging    | Imagga API |
| Email Service    | Mailgun |
| Containerization | Docker & Docker Compose |

---

## 📁 Project Structure

```
cloud-ads-starter/
│
├── service_api/
│   ├── app.py
│   ├── storage.py
│   ├── message_queue.py
│   ├── db.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── service_worker/
│   ├── worker.py
│   ├── image_tagging.py
│   ├── emailer.py
│   ├── storage.py
│   ├── message_queue.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## ⚙️ Environment Variables

Create a `.env` file using the provided example:

```bash
cp .env.example .env
```

---

## ▶️ Running the Project

### Prerequisites
- Docker
- Docker Compose

### Start services

```bash
docker compose up --build
```

---

## 📤 API Usage

- Uploads an image
- Stores it in MinIO
- Saves metadata in PostgreSQL
- Publishes a message to RabbitMQ

The worker then processes the task asynchronously.

---

## 📦 Storage

- Images are stored in **MinIO**
- Accessed via **presigned URLs**
- Fully compatible with AWS S3 SDKs

---

## 🔄 Asynchronous Processing

This project follows an **event-driven design** using RabbitMQ to decouple services and improve scalability.

---

## 🎯 Learning Objectives

- Microservices architecture
- Event-driven systems
- Cloud storage patterns
- Docker-based deployment

---

## 📜 License

Educational / demo project.
