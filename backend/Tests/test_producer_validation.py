import pytest 
import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
from send_test_service.send_test import validate_task, SCHEMA_PATH

def test_validate_task_success():
    valid_task = {
        "schema_version": 1,
        "task_id": "task-001",
        "order_id": "order-123",
        "pickup": {"address": "123", "lat": 1.0, "lon": 2.0},
        "dropoff": {"address": "456", "lat": 1.0, "lon": 2.0},
        "timestamp": "2025-06-21T10:00:00Z",
        "status": "pending",
        "priority": "high",
        "assignee_id": None,
        "eta_minutes": 15,
        "instructions": "Leave it",
        "metadata": {"fragile": True, "customer_notes": "test"}
    }

    validate_task(valid_task, SCHEMA_PATH)


def test_validate_task_failure():
    invalid_task = {
        "order_id": "order-123"  # missing fields
    }

    with pytest.raises(Exception):
        validate_task(invalid_task, SCHEMA_PATH)