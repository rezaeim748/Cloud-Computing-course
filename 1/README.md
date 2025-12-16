# ☁️ Cloud Ads Starter

## Introduction
This project implements a cloud-based advertisement registration and processing system designed to demonstrate practical usage of modern cloud services and distributed backend architectures. The main goal of the project is to build a realistic service that integrates multiple cloud components—such as databases, object storage, message queues, image processing APIs, and email services—into a cohesive, scalable application.

In this system, users can submit advertisements for vehicles (e.g., cars, motorcycles, bicycles) by providing a textual description, an image, and an email address. Upon submission, the advertisement is stored and processed asynchronously. The uploaded image is analyzed using an image tagging service to determine whether it actually contains a vehicle. Based on the result of this analysis, the advertisement is either approved and categorized or rejected. Finally, the user is notified of the outcome via email.

The architecture follows a microservice-oriented design and consists of two main backend services:

A request-handling service responsible for receiving user requests, storing advertisement data, uploading images to object storage, and publishing processing jobs to a message queue.

A worker service that consumes messages from the queue, retrieves images, performs image tagging, updates the advertisement status in the database, and sends email notifications.

To reflect real-world cloud environments, the project makes use of:

PostgreSQL as a managed database service (DBaaS)

S3-compatible object storage for storing advertisement images

RabbitMQ for asynchronous communication between services

Imagga for image tagging and classification

Mailgun for email notification delivery

This project was developed as part of a Cloud Computing course assignment, with the primary objective of gaining hands-on experience in designing, implementing, and deploying distributed systems using cloud services, rather than focusing solely on business logic or UI concerns

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
