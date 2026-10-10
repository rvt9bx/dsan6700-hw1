from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict, Field

from mypkg.config import Settings
from mypkg.embeddings import TextEmbedder

app = FastAPI(title="dsan6700-hw1")
settings = Settings()

# Initialize embedder globally at startup to load weights into memory once
embedder = TextEmbedder()


class HealthResponse(BaseModel):
    """Response body for the health check endpoint."""

    status: str


@app.get("/health")
async def health() -> HealthResponse:
    """Report that the service is up and able to serve requests."""
    return HealthResponse(status="ok, service is up and running")


class PredictRequest(BaseModel):
    """Request body for the predict endpoint."""

    text: str = Field(..., min_length=1)


class PredictResponse(BaseModel):
    """Response body for the predict embedding endpoint."""

    text: str
    embedding_dim: int
    embedding: list[float]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "text": "This repository provides text embeddings.",
                "embedding_dim": 384,
                "embedding": [0.012, -0.045, 0.089],  # truncated
            }
        }
    )


@app.post("/predict", response_model=PredictResponse)
def predict_endpoint(request: PredictRequest):
    """API route exposing the embedding service."""
    prediction = embedder.predict(input_text=request.text)
    return prediction


# INTENTIONAL BLOCKING CALL
# @app.post("/predict")
# async def predict_blocking(payload: PredictRequest):
#     # time.sleep stands in for synchronous model inference on the event loop
#     time.sleep(1.0)
#     return {"result": f"processed: {payload.text}"}
