# ☁️ Cloud-Based Advertisement Processing System

## Introduction
Cloud Ads Starter is a backend system for registering and processing image-based advertisements in a scalable and decoupled manner. The goal of the project is to model a realistic cloud service that integrates multiple infrastructure components—such as databases, object storage, message queues, and third-party APIs—into a cohesive distributed system.

Users submit advertisements by providing a textual description, an image, and an email address. The request is handled synchronously only for validation and persistence, while all computationally intensive and decision-making steps are executed **asynchronously**. Uploaded images are stored in S3-compatible object storage and analyzed by an external image tagging service to determine whether they contain a vehicle. Based on the analysis result, the advertisement is either approved and categorized or rejected, and the user is notified of the outcome via email.

The system follows a **microservice-oriented architecture** consisting of an API service for request handling and a worker service for background processing. This design allows the system to remain responsive under load while enabling horizontal scalability and loose coupling between components.

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