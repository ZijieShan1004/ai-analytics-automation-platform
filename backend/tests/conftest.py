import pytest
from fastapi.testclient import TestClient

from app.main import app


# Create a FastAPI test client.
@pytest.fixture
def client() -> TestClient:
    return TestClient(app)