from fastapi import FastAPI
from pydantic import BaseModel, Field

from mypkg.config import Settings

app = FastAPI(title="dsan6700-hw1")
settings = Settings()


class HealthResponse(BaseModel):
    """Response body for the health check endpoint."""

    status: str


@app.get("/health")
def health() -> HealthResponse:
    """Report that the service is up and able to serve requests."""
    return HealthResponse(status="ok, service is up and running")


class PredictRequest(BaseModel):
    """Request body for the placeholder predict endpoint."""

    text: str = Field(..., min_length=1)


class PredictResponse(BaseModel):
    """Response body for the placeholder predict endpoint."""

    prediction: str


@app.post("/predict")
def predict(payload: PredictRequest) -> PredictResponse:
    """Echo the input text back as a placeholder prediction."""
    return PredictResponse(prediction=f"echo: {payload.text}")
