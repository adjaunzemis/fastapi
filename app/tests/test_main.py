from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)

def test_root():
    response = client.get("/?token=jessica")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello Bigger Applications!"}

def test_root_invalid_token():
    response = client.get("/?token=invalid")
    assert response.status_code == 400
    assert response.json() == {"detail": "No Jessica token provided"}
