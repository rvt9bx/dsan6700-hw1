# DSAN 6700 Homework 2

## Project Overview

This project is a minimal FastAPI web service for DSAN 6700 HW 2. 

It has two endpoints:

| Endpoint | Method | Purpose|
|----|----|----|
| /health | GET | Check the health of the API |
| /predict | POST | Placeholder prediction endpoint | 

**Authors:**

Nkemdibe Okweye, Noelle Martell, Erin Brzusek, Ellie Byrd

## Installation and Running 

### Install Prerequisites:

- Python >= 3.11
- uv 

On MacOS or Linux:
```
curl -LsSf https://astral.sh/uv/install.sh | sh
uv python install 3.12
```

### Install Service:

On MacOS or Linux:
```
git clone https://github.com/rvt9bx/dsan6700-hw1.git
cd dsan6700-hw1
uv sync
```

### Configure Environment:

```
cp .env.local.example .env
```
or 
```
cp .env.production.example .env
```

Add Hugging Face API key to use a gated embedding model. 

### Run the Web Service and Verify:

On MacOS or Linux:
```
PYTHONPATH=src 
uv run uvicorn mypkg.mypkg:app --reload
# check health endpoint
curl http://127.0.0.1:8000/health
# check prediction endpoint
curl -X POST http://127.0.0.1:8000/predict -H "Content-Type: application/json" -d '{"text":"hello, this is a test"}'
```

After starting the server with uvicorn locally, you can also visit http://127.0.0.1:8000/health (or whatever host and port you specify) to check the health endpoint, or visit the built in Swagger UI documentation at http://127.0.0.1:8000/docs. 

## Running with Docker

### Install Prerequisites:

- Docker Desktop (MacOS/Windows) or Docker Engine (Linux)

### Configure Environment:

```
cp .env.local.example .env
```
or
```
cp .env.production.example .env
```

### Build and Start the Service:

On a fresh clone of the repository:
```
git clone https://github.com/rvt9bx/dsan6700-hw1.git
cd dsan6700-hw1
cp .env.local.example .env
docker compose up -d --build
```

### Verify:

```
# check health endpoint
curl http://localhost:8000/health
# check prediction endpoint
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{"text":"hello, this is a test"}'
```

You can also visit http://localhost:8000/docs for the Swagger UI, or http://localhost:8000/health in a browser.

### Stop the Service:

```
docker compose down
```