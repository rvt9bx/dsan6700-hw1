# DSAN 6700 Homework 1

## Project Overview

This project is a minimal FastAPI web service for DSAN 6700 HW 1. 

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
git clone 
cd dsan6700-hw1
uv sync
```

### Run the Web Service and Verify:

On MacOS or Linux:
```
PYTHONPATH=src uv run uvicorn mypkg.mypkg:app --reload
# check health endpoint
curl http://127.0.0.1:8000/health
# check prediction endpoint
curl -X POST http://127.0.0.1:8000/predict -H "Content-Type: application/json" -d '{"text":"hello, this is a test"}'
```

After starting the server with uvicorn locally, you can also visit http://127.0.0.1:8000/health (or whatever host and port you specify) to check the health endpoint, or visit the built in Swagger UI documentation at http://127.0.0.1:8000/docs. 