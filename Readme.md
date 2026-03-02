# Async Task Queue

A distributed task queue system built with FastAPI, Celery, Redis, and PostgreSQL.

## Features
- Submit background jobs via REST API
- Real-time job status polling (pending → started → success/failure)
- Multiple job types (email, data processing)
- Redis as message broker and result backend
- Retry logic with exponential backoff
- Fully containerized with Docker Compose

## Tech Stack
- **FastAPI** — API framework
- **Celery** — distributed task queue
- **Redis** — message broker + result backend
- **PostgreSQL** — job persistence
- **Docker Compose** — containerization

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/tasks/` | Submit a background job |
| GET | `/tasks/{task_id}` | Check job status and result |

## Job Types
**send_email:**
```json
{
  "job_type": "send_email",
  "payload": {
    "recipient": "user@example.com",
    "subject": "Hello!"
  }
}
```

**process_data:**
```json
{
  "job_type": "process_data",
  "payload": {
    "key1": "value1",
    "key2": "value2"
  }
}
```

## Run Locally
```bash
# Clone and setup
git clone https://github.com/nagarjun-nagaraj/task-queue.git
cd task-queue

# Add .env
echo "DATABASE_URL=postgresql://postgres:password@127.0.0.1:5432/taskqueue" > .env
echo "REDIS_URL=redis://localhost:6379" >> .env

# Start containers
docker compose up -d

# Install dependencies
pip install -r requirements.txt

# Terminal 1 — API
uvicorn app.main:app --reload

# Terminal 2 — Worker
celery -A app.celery_app.celery worker --loglevel=info
```