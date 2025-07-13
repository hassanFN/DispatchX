import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
from unittest.mock import patch, MagicMock 
from send_test_service.send_test import main,task 
import pytest 
from unittest.mock import ANY

TOPIC = "fake-topic"
SCHEMA_REGISTRY_URL = "http://fake-schema-registry"



def test_producer_send_success():
    global TOPIC
    global SCHEMA_REGISTRY_URL
    global BOOTSTRAP
    with patch("send_test_service.send_test.SerializingProducer") as MockProducer:      
        mock_producer = MagicMock()
        
        MockProducer.return_value = mock_producer
        
        main(TOPIC, SCHEMA_REGISTRY_URL)

        mock_producer.produce.assert_called_once_with(

            topic=TOPIC,
            key=task["order_id"],
            value=task,
            headers=ANY,
            on_delivery=ANY


        )

        mock_producer.flush.assert_called_once()


def test_send_producer_failure():
    global TOPIC
    global SCHEMA_REGISTRY_URL
    global BOOTSTRAP
    with patch("send_test_service.send_test.SerializingProducer") as MockProducer: 
        mock_producer = MagicMock()
        mock_producer.produce.side_effect = Exception("Kafka send failed")
        MockProducer.return_value = mock_producer 
        with pytest.raises(SystemExit):  # producer exits on failure
            main(TOPIC, SCHEMA_REGISTRY_URL)

