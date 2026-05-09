# AI Analytics Automation Platform

A backend-heavy AI analytics automation platform that converts uploaded CSV or Excel datasets into automated business reports, chart recommendations, time-series forecasts, anomaly insights, and LLM-generated summaries.

This project is designed as a production-style internal analytics platform, not a simple dashboard or course project.

## Core Goal

Users upload structured business data. The system asynchronously processes the dataset through a backend-driven analytics pipeline and generates a complete analytics report.

## System Flow

```text
User Upload CSV or Excel
↓
FastAPI Upload Endpoint
↓
JWT Authentication
↓
PostgreSQL Metadata Storage
↓
Celery Background Job
↓
Redis Queue
↓
Data Profiling Engine
↓
Analytics Engine
↓
Chart Recommendation Engine
↓
Forecasting Engine
↓
Ollama Summary Generator
↓
PostgreSQL Result Storage
↓
React Dashboard Fetches Report
```

## Architecture

Frontend Layer:
  React
  TypeScript
  Vite
  Minimal dashboard UI

Backend/API Layer:
  Python
  FastAPI
  PostgreSQL
  SQLAlchemy
  Alembic
  Redis
  Celery
  JWT Authentication
  Docker Compose

ML/Data Processing Layer:
  pandas
  NumPy
  scikit-learn
  Prophet-compatible forecasting structure
  anomaly detection
  chart recommendation
  Ollama-based local LLM summary generation

  
## Main Features
## Authentication
-User registration
-User login
-JWT access tokens
-Password hashing
-User-specific data isolation

## Dataset Upload
-CSV upload
-Excel upload
-File persistence
-Dataset metadata persistence
-Background processing job creation

## Data Understanding
-Numeric column detection
-Categorical column detection
-Datetime column detection
-Missing value profiling
-Outlier detection
-Correlation analysis
-Trend analysis

## Chart Recommendation

The system automatically recommends charts based on detected schema and analytics results.

Supported chart types:

-Line chart
-Bar chart
-Histogram
-Heatmap
-Pie chart
-Moving average chart
-Forecast chart

## Analytics Pipeline

The backend generates:

-Aggregations
-KPI summaries
-Trend summaries
-Anomaly summaries
-Correlation summaries
-Chart payloads

## Forecasting

The system automatically detects valid time-series candidates and generates future trend predictions.

Supported forecasting strategy:

-Prophet-style forecasting interface
-Regression fallback
-Forecast result persistence

## AI Summary Generation

The platform uses local Ollama with Qwen to generate business summaries from structured analytics facts.

The system does not send raw CSV content directly to the LLM. It first extracts structured facts through deterministic analytics pipelines, then asks the LLM to explain those facts in business language.

Example summary: 

```bash 
Sales increased by 18% during the analyzed period, with the strongest growth coming from the West region. The system detected an unusual spike in April, which may indicate a seasonal demand surge or a promotional effect.
```
## Local Deployment
This project is designed to run fully locally.

Required local tools:

-Docker Desktop
-Docker Compose
-Python 3.11+
-Node.js 20+
-Ollama
-Local Qwen model

Expected Ollama model:

ollama pull qwen2.5:1.5b

Run Ollama locally:

ollama serve

Then start the platform:

cp .env.example .env
docker compose up --build

## Local Services
Frontend:
  http://localhost:5173

Backend API:
  http://localhost:8000

FastAPI Docs:
  http://localhost:8000/docs

PostgreSQL:
  localhost:5432

Redis:
  localhost:6379

Ollama:
  http://localhost:11434
