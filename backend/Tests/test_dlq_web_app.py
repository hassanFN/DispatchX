import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
from dlq_web_app import app
from unittest.mock import patch, MagicMock
import json

def test_index_route_returns_html():
    with patch("dlq_web_app.app.Consumer") as MockConsumer:
        mock_consumer = MagicMock()
        mock_message = MagicMock()
        mock_message.value.return_value = json.dumps({"error": "schema fail"}).encode()
        mock_consumer.poll.side_effect = [mock_message, None, None, None, None]
        mock_message.headers.return_value = [("correlation_id", "1234")]  # ✅ Real-looking data
        MockConsumer.return_value = mock_consumer

        client = app.app.test_client()
        response = client.get("/")

        assert response.status_code == 200
        assert b"Dead Letter Queue Messages" in response.data