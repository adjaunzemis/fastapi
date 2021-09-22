from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)

def test_read_items():
    response = client.get(
        "/items/?token=jessica",
        headers={"X-Token": "fake-super-secret-token"}
    )
    assert response.status_code == 200
    assert response.json() == {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}


def test_read_items_invalid_header_token():
    response = client.get(
        "/items/?token=jessica",
        headers={"X-Token": "invalid-token"}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "X-Token header invalid"}
    
def test_read_items_invalid_query_token():
    response = client.get(
        "/items/?token=invalid",
        headers={"X-Token": "fake-super-secret-token"}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "No Jessica token provided"}

def test_read_item():
    response = client.get(
        "/items/gun/?token=jessica",
        headers={"X-Token": "fake-super-secret-token"}
    )
    assert response.status_code == 200
    assert response.json() == {"name": "Portal Gun", "item_id":"gun"}

def test_read_item_not_found():
    response = client.get(
        "/items/invalid/?token=jessica",
        headers={"X-Token": "fake-super-secret-token"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}

def test_update_item():
    response = client.post(
        "/items/plumbus/?token=jessica",
        headers={"X-Token": "fake-super-secret-token"},
        json={}
    )
    assert response.status_code == 200
    assert response.json() == {"item_id": "plumbus", "name": "The great Plumbus"}
