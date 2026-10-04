"""Tests for the API endpoints."""

from fastapi.testclient import TestClient

# This import works because of the pythonpath setting added to pyproject.toml.
from main import app

# TestClient calls the app directly, so the server does not need to be running.
client = TestClient(app)


# Fixed: functions now have two blank lines between them (one before).
def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# Fixed: this function had no body, which caused an IndentationError and
# stopped every test in this file from running, even test_health_check.
def test_calculation_addition():
    response = client.post("/calculate", json={"a": 10, "b": 5, "operation": "add"})
    assert response.status_code == 200
    assert response.json() == {"result": 15}


# Fixed: added the remaining cases you had been checking by hand in /docs.
# Error responses also check the message, not only the status code.
def test_calculation_divide_by_zero_returns_400():
    response = client.post("/calculate", json={"a": 10, "b": 0, "operation": "divide"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Division by zero is not allowed."


# 422 comes from the schema: "power" is not in the Operation enum, so FastAPI
# rejects the request before the route function runs.
def test_calculation_unknown_operation_returns_422():
    response = client.post("/calculate", json={"a": 10, "b": 5, "operation": "power"})
    assert response.status_code == 422


def test_calculation_missing_field_returns_422():
    response = client.post("/calculate", json={"a": 10, "operation": "add"})
    assert response.status_code == 422


def test_power():
    response = client.post("/power", json={"base": 2, "exponent": 10})
    assert response.status_code == 200
    assert response.json() == {"result": 1024}


def test_power_zero_base_negative_exponent_returns_400():
    response = client.post("/power", json={"base": 0, "exponent": -1})
    assert response.status_code == 400
    assert response.json()["detail"] == "Zero base with negative exponent is not allowed."


def test_power_overflow_returns_400():
    response = client.post("/power", json={"base": 10, "exponent": 1000})
    assert response.status_code == 400
