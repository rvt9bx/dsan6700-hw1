import asyncio
import time
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient

from mypkg.mypkg import app, get_embedder

# Mock output matching PredictResponse structure
MOCK_PREDICTION_OUTPUT = {
    "text": "Hello world",
    "embedding_dim": 384,
    "embedding": [0.1] * 384,  # Synthetic 384-dimensional vector
}

# Mock embedder instance
mock_embedder = MagicMock()
mock_embedder.predict.return_value = MOCK_PREDICTION_OUTPUT
app.dependency_overrides[get_embedder] = lambda: mock_embedder

client = TestClient(app)


def test_health_returns_ok():
    """Ensure that requesting the health endpoint returns 200 and status output"""

    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok, service is up and running"}


def test_predict_endpoint_success():
    """Test /predict endpoint with a mocked embedding prediction."""

    mock_embedder.predict.reset_mock()
    mock_embedder.predict.return_value = MOCK_PREDICTION_OUTPUT

    payload = {
        "text": "Hello world",
    }

    response = client.post("/predict", json=payload)

    # Assert HTTP status
    assert response.status_code == 200

    # Assert JSON payload matches schema
    data = response.json()
    assert data["text"] == "Hello world"
    assert data["embedding_dim"] == 384
    assert len(data["embedding"]) == 384

    # Ensure the embedder method was actually called with right params
    mock_embedder.predict.assert_called_once_with(
        input_text="Hello world",
    )


def test_predict_rejects_empty_text():
    """Ensure that hitting the predict endpoint with no text returns 422
    unprocessable content error"""

    response = client.post("/predict", json={"text": ""})
    assert response.status_code == 422


@pytest.mark.anyio
async def test_predict_endpoint_does_not_block_health():
    """
    Tests that a synchronous CPU-heavy predict operation running on a worker thread
    does not block the main event loop from serving /health.
    """

    # 1. Mock the embedding model so it simulates a 1-second CPU calculation
    def slow_embed(*_args, **_kwargs):
        time.sleep(1.0)  # Blocking synchronous CPU delay
        return MOCK_PREDICTION_OUTPUT

    mock_embedder.predict.side_effect = slow_embed

    # 2. Set up the async test client
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        start_time = time.perf_counter()

        # 3. Schedule the slow /predict task on the event loop
        predict_payload = {"text": "Hello world"}
        predict_task = asyncio.create_task(
            client.post("/predict", json=predict_payload)
        )

        # 4. Give the event loop a brief moment to dispatch the /predict call
        await asyncio.sleep(0.05)

        # 5. Fire the health check request
        health_res = await client.get("/health")
        health_duration = time.perf_counter() - start_time

        # 6. Wait for the predict request to complete
        predict_res = await predict_task

        # Assertions
        assert health_res.status_code == 200
        assert health_res.json() == {"status": "ok, service is up and running"}

        # Verify /health responded quickly (< 200ms) despite /predict taking ~1000ms
        assert health_duration < 0.2, (
            f"Health check was delayed! Took {health_duration:.2f}s"
        )
        assert predict_res.status_code == 200
        assert mock_embedder.predict.called

    # Reset side effect
    mock_embedder.predict.side_effect = None
