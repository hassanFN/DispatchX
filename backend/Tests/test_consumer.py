import os
import sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
import pytest
from unittest.mock import patch, MagicMock
from dispatcher_service.app import dlq_producer,process_task,handle_kafka_message # adjust import to your path





def test_valid_message(monkeypatch):
    mock_msg = MagicMock()

    mock_msg.value.return_value = {
        "schema_version": 1,
        "task_id": "task-001",
        "order_id": "order-123",
        "pickup": {
            "address": "123 Main St",
            "lat": 40.0,
            "lon": -88.0
        },
        "dropoff": {
            "address": "456 Elm St",
            "lat": 40.0,
            "lon": -88.0
        },
        "timestamp": "2025-06-21T10:00:00Z",
        "status": "pending",
        "priority": "high",
        "assignee_id": None,
        "eta_minutes": 15,
        "instructions": "Leave at door",
        "metadata": {
            "fragile": True,
            "customer_notes": "Handle with care"
        }
    }


    mock_msg.error.return_value = None
    mock_msg.headers.return_value = [("correlation_id", b"test-id")]
    mock_msg.topic.return_value = "dispatch-tasks"
    mock_msg.partition.return_value = 0
    mock_msg.offset.return_value = 0
    mock_msg.key.return_value = "order-123"

    #monkeypatch.setattr("dispatcher_service.app.process_task", lambda task: True)
 # Mock the DLQ producer to track calls
    mock_dlq_producer = MagicMock()
    monkeypatch.setattr("dispatcher_service.app.dlq_producer", mock_dlq_producer)
    handle_kafka_message(mock_msg)
    print("Handle kafka function is running...")



    # Simulate Kafka error
def test_kafka_error_message(monkeypatch):
    mock_msg = MagicMock()
    mock_msg.error.return_value = "Kafka Error"
    mock_msg.headers.return_value = [("correlation_id", b"err-id")]
    mock_msg.topic.return_value = "dispatch-tasks"
    mock_msg.partition.return_value = 0
    mock_msg.offset.return_value = 0
    mock_msg.key.return_value = "err-order"

    mock_dlq_producer = MagicMock()
    monkeypatch.setattr("dispatcher_service.app.dlq_producer", mock_dlq_producer)

    handle_kafka_message(mock_msg)
    assert mock_dlq_producer.produce.called
    assert mock_dlq_producer.flush.called





def test_invalid_message_schema(monkeypatch):
    mock_msg = MagicMock()

    # Invalid message: missing required field 'task_id'
    invalid_value = {
        "schema_version": 1,
        # "task_id": "task-001",  # intentionally omitted
        "order_id": "order-123",
        "pickup": {
            "address": "123 Main St",
            "lat": 40.0,
            "lon": -88.0
        },
        "dropoff": {
            "address": "456 Elm St",
            "lat": 40.0,
            "lon": -88.0
        },
        "timestamp": "2025-06-21T10:00:00Z",
        "status": "pending",
        "priority": "high",
        "assignee_id": None,
        "eta_minutes": 15,
        "instructions": "Leave at door",
        "metadata": {
            "fragile": True,
            "customer_notes": "Handle with care"
        }
    }

    mock_msg.value.return_value = invalid_value
    mock_msg.error.return_value = None
    mock_msg.headers.return_value = [("correlation_id", b"test-id")]
    mock_msg.topic.return_value = "dispatch-tasks"
    mock_msg.partition.return_value = 0
    mock_msg.offset.return_value = 0
    mock_msg.key.return_value = "order-123"




    # Run your message handler with the invalid message
    with patch("dispatcher_service.app.send_to_dlq") as mock_send:
        handle_kafka_message(mock_msg)
        mock_send.assert_called_once()
        

   

    # Assert that DLQ producer was called with error info
 

    # Optional: inspect what was sent to DLQ
    #args, kwargs = mock_dlq_producer.produce.call_args
    #assert kwargs["topic"] == "your-dlq-topic-name" or args[0] == "your-dlq-topic-name"
    # You can also decode kwargs["value"] or args[2] to check error details if needed












def test_process_task_failure(monkeypatch):
    mock_msg = MagicMock()
    mock_msg.value.return_value = {
        "schema_version": 1,
        #"task_id": "task-crash",
        "order_id": "order-crash",
        "pickup": {
            "address": "123 Crash St",
            "lat": 40.0,
            "lon": -88.0
        },
        "dropoff": {
            "address": "456 Boom St",
            "lat": 40.0,
            "lon": -88.0
        },
        "timestamp": "2025-06-21T10:00:00Z",
        "status": "pending",
        "priority": "high",
        "assignee_id": None,
        "eta_minutes": 15,
        "instructions": "Leave at door",
        "metadata": {
            "fragile": True,
            "customer_notes": "Handle with care"
        }
    }

    mock_msg.error.return_value = None
    mock_msg.headers.return_value = [("correlation_id", b"crash-id")]
    mock_msg.topic.return_value = "dispatch-tasks"
    mock_msg.partition.return_value = 0
    mock_msg.offset.return_value = 0
    mock_msg.key.return_value = "order-crash"

    # Simulate crash in process_task
    #monkeypatch.setattr("dispatcher_service.app.process_task", lambda task: (_ for _ in ()).throw(Exception("Boom")))

       
    with patch("dispatcher_service.app.send_to_dlq") as mock_send:
        handle_kafka_message(mock_msg)
        mock_send.assert_called_once()

    