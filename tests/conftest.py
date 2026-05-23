from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src.app import activities as activities_data
from src.app import app


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset in-memory activity state around each test."""
    original_activities = deepcopy(activities_data)
    yield
    activities_data.clear()
    activities_data.update(deepcopy(original_activities))


@pytest.fixture
def client():
    return TestClient(app)
