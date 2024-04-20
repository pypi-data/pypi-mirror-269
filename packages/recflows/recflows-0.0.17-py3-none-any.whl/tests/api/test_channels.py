from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_channels():
    response = client.get("/channels")
    assert response.status_code == 200
    assert len(response.json()) == 0
