from fastapi.testclient import TestClient


# Test the root endpoint.
def test_root(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "running"