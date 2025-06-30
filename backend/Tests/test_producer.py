from unittest.mock import patch, MagicMock
from send_test_service.send_test import main, task  # assuming same structure as before
import pytest
from unittest.mock import ANY


def test_producer_send_success():
    with patch("send_test_service.send_test.SerializingProducer") as MockProducer:
        mock_producer = MagicMock()
        MockProducer.return_value = mock_producer

        main()

        # Check that produce was called once with correct arguments
        mock_producer.produce.assert_called_once_with(
            topic="dispatch-tasks",
            key=task["order_id"],
            value=task,
            on_delivery=ANY         # ✅ Accept any callable here
        )

        # Check flush was called
        mock_producer.flush.assert_called_once()


def test_producer_send_failure():
    with patch("send_test_service.send_test.SerializingProducer") as MockProducer:
        mock_producer = MagicMock()
        mock_producer.produce.side_effect = Exception("Kafka send failed")
        MockProducer.return_value = mock_producer

        with pytest.raises(SystemExit):  # sys.exit(1) should trigger
            main()
