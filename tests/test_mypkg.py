from fastapi.testclient import TestClient

from mypkg.mypkg import app

client = TestClient(app)


def test_health_returns_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok, service is up and running"}


def test_predict_echoes_input_text():
    response = client.post("/predict", json={"text": "hello"})
    assert response.status_code == 200
    assert response.json() == {"prediction": "echo: hello"}


def test_predict_rejects_empty_text():
    response = client.post("/predict", json={"text": ""})
    assert response.status_code == 422
