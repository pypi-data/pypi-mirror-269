from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_recommenders():
    response = client.get("/recommenders")
    assert response.status_code == 200
    assert len(response.json()) == 0
