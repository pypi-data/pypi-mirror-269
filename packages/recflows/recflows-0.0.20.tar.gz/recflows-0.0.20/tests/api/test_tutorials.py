from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_tutorials():
    response = client.get("/tutorials")
    assert response.status_code == 200
    assert len(response.json()) == 0
