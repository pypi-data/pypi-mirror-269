from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_apps():
    response = client.get("/apps")
    assert response.status_code == 200
    assert len(response.json()) == 5
