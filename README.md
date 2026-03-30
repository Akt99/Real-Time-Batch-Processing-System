# Real Time Batch Processing System
## Live Demo

Click here to view the demo:
https://drive.google.com/file/d/1Z1kwT_2_TGqcOwdUVTqlP5AMb7b1zcfd/view?usp=drive_link

## Overview

This project is a full stack application that allows users to

Upload a CSV file of transactions
Process data in batches
Track job progress in real time
View processed results with filtering and pagination

---

## Key Features

CSV Upload and Job Creation.
Batch Processing using fixed size batches.
Real time Job Progress Tracking.
Data Validation and Classification.
Filtering by valid invalid and suspicious records.
Clean and scalable architecture.

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

React with Hooks.
Axios
Polling or WebSocket

---

## Application Flow

1. User uploads CSV using POST jobs </br>
2. Backend creates job with status pending </br>
3. User starts job using POST jobs id start </br>
4. Worker processes file in batches </br>
5. Database is updated after each batch </br>
6. Frontend polls job status </br>
7. User sees live progress </br>

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

### Upload CSV

**POST /jobs**

Accepts a CSV file and creates a new job.

**Request**

* Content Type: multipart form data
* File: CSV file containing transactions

**Response**

* job id
* status set to pending

---

### Start Processing

**POST /jobs/{id}/start**

Triggers background processing for the given job.

**Behavior**

* Changes job status to running
* Starts batch processing

---

### Get Job Status

**GET /jobs/{id}**

Returns the current status and progress of the job.

**Response Fields**

* id
* status
* total_records
* processed_records
* valid_records
* invalid_records
* suspicious_records
* progress_percent

---

### Get Transactions

**GET /jobs/{id}/transactions**

Fetches processed transactions for a job.

**Features**

* Pagination support
* Filtering by status:

  * valid
  * invalid
  * suspicious


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



### Prerequisites

- Docker Desktop installed and running

### Environment Variables

Create `backend/.env`:

```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@db:5432/batch_processing
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/1
CORS_ORIGINS=["http://localhost:3000"]
UPLOAD_DIR=storage/uploads
BATCH_SIZE=100
```

## Docker Setup

The Docker Compose setup initializes the following services:

* db for PostgreSQL
* redis for Celery broker and backend
* backend for FastAPI application
* worker for Celery batch processing
* frontend for React application

---

## Docker Commands

### Start Services

```bash
docker compose up -d
```

Starts all services in detached mode.

---

### View Logs

```bash
docker compose logs -f backend
docker compose logs -f worker
docker compose logs -f frontend
```

Displays real time logs for selected services.

---

### Stop Services

```bash
docker compose down
```

Stops and removes all running containers.

## Database Migration and Schema Setup

This project uses SQLAlchemy metadata initialization for database schema setup instead of a dedicated migration tool such as Alembic.

---

### Create the Database Schema

#### Local Setup

```bash
cd backend
python -m app.db.init_db
```

#### Docker Setup

```bash
docker compose exec backend python -m app.db.init_db
```

These commands create the required tables in PostgreSQL based on the defined SQLAlchemy models.

---

### Current Tables

The schema currently includes the following tables:

* jobs
* transactions

---

### Notes

* This project does not currently use versioned migrations with Alembic
* Schema creation is handled directly through SQLAlchemy model definitions
* If the schema evolves in the future, it is recommended to integrate Alembic for proper migration management
* Changes such as adding new fields or enum values (for example, additional job statuses) should ideally be managed through migrations

---

### Recommendation

For production readiness and long term maintainability, integrating Alembic is recommended to:

* Track schema changes
* Support versioned migrations
* Enable safe database updates across environments


---

## Design Decisions

Batch processing is used for scalability </br>
Separation of concerns across layers </br>
Polling is used for simplicity </br>
PostgreSQL is used for reliability and indexing </br>

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
