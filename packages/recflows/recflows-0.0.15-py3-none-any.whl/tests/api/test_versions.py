from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_versions():
    response = client.get("/versions")
    assert response.status_code == 200
    assert len(response.json()) == 0
