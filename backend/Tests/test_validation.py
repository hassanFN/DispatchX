from send_test_service.send_test import validate_task, SCHEMA_PATH
import pytest


def test_validate_task_valid():
    task = {
        "schema_version": 1,
        "task_id": "task-001",
        "order_id": "order-123",
        "pickup": {
            "address": "123 Main St, Springfield, IL",
            "lat": 40.1123,
            "lon": -88.2284
        },
        "dropoff": {
            "address": "456 Elm St, Lincoln, IL",
            "lat": 40.1500,
            "lon": -88.2500
        },
        "timestamp": "2025-06-21T10:00:00Z",
        "status": "pending",
        "priority": "high",
        "assignee_id": None,
        "eta_minutes": 15,
        "instructions": "Leave at front door, ring bell twice",
        "metadata": {
            "fragile": True,
            "customer_notes": "Handle with care"
        }
    }
    # Should not raise an error
    validate_task(task, SCHEMA_PATH)

def test_validate_task_invalid_missing_field():
    invalid_task = {
        "schema_version": 1,
        # Missing task_id!
        "order_id": "order-123",
        "pickup": {
            "address": "123 Main St",
            "lat": 40.1123,
            "lon": -88.2284
        },
        "dropoff": {
            "address": "456 Elm St",
            "lat": 40.1500,
            "lon": -88.2500
        },
        "timestamp": "2025-06-21T10:00:00Z",
        "status": "pending",
        "priority": "high"
    }
    with pytest.raises(Exception):
        validate_task(invalid_task, SCHEMA_PATH)

