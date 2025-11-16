📌 InsightHub — Cloud Monitoring & Metrics Dashboard

A real-time cloud monitoring platform that ingests metrics, stores them in PostgreSQL, and visualizes system performance using Streamlit.
Built with Docker-powered microservices.

📸 Screenshots
Real-time Dashboard


<img width="1920" height="1080" alt="InsightHub Dashboard" src="https://github.com/user-attachments/assets/622bd931-1ed8-4195-bf23-fea9e8d20dfa" />


API Docs (FastAPI Swagger UI)



<img width="1920" height="1080" alt="FastAPI Swagger Docs" src="https://github.com/user-attachments/assets/5fddaad1-575c-4211-b035-d3a0fc65886d" />







🧠 What InsightHub Does

InsightHub is a lightweight, containerized cloud monitoring stack that simulates what enterprise observability tools like Datadog, New Relic, and Grafana do:

✔ Collect metrics (CPU, memory, latency, errors)

✔ Store metrics in PostgreSQL

✔ Serve a FastAPI backend with /metrics, /latest, /series

✔ Render a live dashboard in Streamlit

✔ Run everything with docker compose up

✔ Auto-generates data using a separate metrics generator service

This project demonstrates:

Microservices

Full stack in containers

API design

Database queries

Dashboard UI

DevOps fundamentals (Docker, WSL2, networking, environment configs)



🏗 Architecture Overview

               +-------------------+
               |   Metrics Generator|
               |  (Python service) |
               +---------+---------+
                         |
                         | POST /metrics
                         v
             +--------------------------+
             |        FastAPI API       |
             +------------+-------------+
                          |
                          |   INSERT + SELECT
                          v
                 +------------------+
                 |    PostgreSQL    |
                 +------------------+
                          |
                          |   GET /metrics/latest
                          v
              +-----------------------------+
              |     Streamlit Dashboard     |
              +-----------------------------+

🛠 Tech Stack

Python 3.11

FastAPI (API backend)

Streamlit (UI dashboard)

PostgreSQL 15

Docker + Docker Compose

WSL2 (Windows compatibility)

psycopg (database driver)




📂 Project Structure
.
├── services/
│   ├── api/           # FastAPI backend
│   ├── dashboard/     # Streamlit app
│   └── generator/     # Metrics generator
├── sql/
│   └── init.sql       # DB schema
├── .env.example       # Environment template
├── docker-compose.yml
└── README.md


🚀 Running InsightHub
1. Clone the repo
git clone https://github.com/tinosith/cloud-monitoring-insighthub.git
cd cloud-monitoring-insighthub

2. Create your .env
cp .env.example .env

3. Start the whole stack
docker compose up --build

4. Open the services
Service	URL
Dashboard (Streamlit)	http://localhost:8501

API Docs (Swagger)	http://localhost:8000/docs

Database	localhost:5432
🧪 API Endpoints (FastAPI)
✔ Test Health
GET /health

✔ Ingest a Metric
POST /metrics

✔ Latest Value
GET /metrics/latest

✔ Time Series
GET /metrics/series


🧭 Roadmap (Next Milestones)
Sprint 2 – Cloud + CI/CD

Deploy backend to Render / Railway / Fly.io

Deploy dashboard to Streamlit Cloud

Push PostgreSQL to Supabase

Sprint 3 – Add Authentication

JWT auth

API keys for external clients

Sprint 4 – Real Cloud Data

Replace simulated metrics with:

AWS CloudWatch ingestion

System metrics via psutil

Kubernetes node metrics

Sprint 5 – Alerting System

Slack / Email alerts

Threshold-based triggers

👤 Author

Tinotenda Sithole
Cloud & DevOps Engineer (in training)
GitHub: https://github.com/tinosith


