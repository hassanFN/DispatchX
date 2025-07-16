import os
import sys
from unittest.mock import MagicMock

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
sys.path.insert(0, os.path.join(parent_dir, 'dispatcher_service'))

# Ensure env vars required by dispatcher_service are present
os.environ.setdefault('GOOGLE_MAPS_API_KEY', 'test-key')

# Mock Kafka dependencies for Flask app import
sys.modules.setdefault("confluent_kafka", MagicMock())
sys.modules.setdefault("confluent_kafka.schema_registry", MagicMock())
sys.modules.setdefault("confluent_kafka.schema_registry.json_schema", MagicMock())
sys.modules.setdefault("confluent_kafka.serialization", MagicMock())
sys.modules.setdefault("jsonschema", MagicMock())
sys.modules.setdefault("structlog", MagicMock())
sys.modules.setdefault("googlemaps", MagicMock())


from dispatcher_service import app as dispatcher_app


def test_api_drivers_returns_list():
    client = dispatcher_app.app.test_client()
    resp = client.get('/api/drivers')
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    assert len(data) > 0
    expected_keys = {'id', 'location', 'current_tasks', 'rating', 'status'}
    assert all(expected_keys <= set(d.keys()) for d in data)


def test_api_tasks_returns_list():
    client = dispatcher_app.app.test_client()
    resp = client.get('/api/tasks')
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    assert len(data) > 0
    expected_keys = {'task_id', 'order_id', 'pickup', 'dropoff'}
    assert all(expected_keys <= set(t.keys()) for t in data)
