# Real Time Batch Processing System

## Overview

This project is a full stack application that allows users to

Upload a CSV file of transactions
Process data in batches
Track job progress in real time
View processed results with filtering and pagination

---

## Key Features

CSV Upload and Job Creation
Batch Processing using fixed size batches
Real time Job Progress Tracking
Data Validation and Classification
Filtering by valid invalid and suspicious records
Clean and scalable architecture

---

## Architecture Diagram

```
                Frontend React
                        |
             Polling or WebSocket
                        |
                FastAPI API Layer
                        |
                 Service Layer
                Business Logic
                        |
              Repository Layer
                   Database Access
                        |
                  PostgreSQL
                        |
              Background Worker
                 Batch Processor
```

---

## Tech Stack

### Backend

FastAPI using Python
PostgreSQL
SQLAlchemy
Background Tasks or Celery

### Frontend

React with Hooks
Axios
Polling or WebSocket

---

## Application Flow

1 User uploads CSV using POST jobs
2 Backend creates job with status pending
3 User starts job using POST jobs id start
4 Worker processes file in batches
5 Database is updated after each batch
6 Frontend polls job status
7 User sees live progress

---

## Job Lifecycle

pending to running to completed

failed is used only for system level errors

---

## Project Structure

### Backend

```
backend
│
├── app
│   ├── main.py
│   ├── core
│   ├── models
│   ├── schemas
│   ├── api routes
│   ├── services
│   ├── repositories
│   ├── workers
│   └── utils
```

### Frontend

```
frontend
│
├── src
│   ├── api
│   ├── components
│   ├── pages
│   ├── hooks
│   ├── App.jsx
│   └── main.jsx
```

---

## API Endpoints

Upload CSV
POST jobs

Start Processing
POST jobs id start

Get Job Status
GET jobs id

Get Transactions
GET jobs id transactions

---

## Validation Rules

Each row must contain
transaction_id as UUID
user_id as UUID
amount as numeric
timestamp as ISO 8601

---

## Transaction Classification

Valid when all checks pass

Suspicious when amount is less than zero or greater than fifty thousand

Invalid when any validation fails

---

## Example Response

```json
{
  "id": "job 123",
  "status": "running",
  "total_records": 1000,
  "processed_records": 450,
  "valid_records": 430,
  "invalid_records": 20,
  "progress_percent": 45
}
```

---

## Setup Instructions

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## Design Decisions

Batch processing is used for scalability
Separation of concerns across layers
Polling is used for simplicity
PostgreSQL is used for reliability and indexing

---

## Optional Enhancements

Job retry mechanism
Resume interrupted jobs
WebSocket based real time updates
Docker setup
Concurrency control

---

## Key Learning Outcomes

Backend architecture design
Batch processing systems
Real time UI updates
Data validation strategies
Clean code practices

---

## Author

Arnab Kumar Tripathy
