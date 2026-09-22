from fastapi.testclient import TestClient

from mypkg.mypkg import app

client = TestClient(app)


def test_health_returns_ok():
    """Ensure that requesting the health endpoint returns 200 and status output"""

    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok, service is up and running"}


def test_predict_echoes_input_text():
    """Ensure that hitting the predict endpoint returns 200 and echoed text"""

    response = client.post("/predict", json={"text": "hello"})
    assert response.status_code == 200
    assert response.json() == {"prediction": "echo: hello"}


def test_predict_rejects_empty_text():
    """Ensure that hitting the predict endpoint with no text returns 422
    unprocessable content error"""

    response = client.post("/predict", json={"text": ""})
    assert response.status_code == 422
