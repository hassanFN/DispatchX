#!/usr/bin/env python3
import os
import sys
import json
from jsonschema import validate, ValidationError
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.json_schema import JSONSerializer
from confluent_kafka import SerializingProducer
from confluent_kafka import Producer 


# -------------------------------
# 🔧 Configuration
# -------------------------------
BASE_DIR = os.path.dirname(__file__)
SCHEMA_PATH = os.path.join(BASE_DIR, "schemas", "dispatch_task_schema.json")
BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "kafka:9092")
TOPIC = os.getenv("DISPATCH_TOPIC", "dispatch-tasks")
SCHEMA_REGISTRY_URL = os.getenv("SCHEMA_REGISTRY_URL", "http://schema-registry:8081")

# -------------------------------
# ✅ Example payload (must match schema!)
# -------------------------------
task = {
    "schema_version": 1,
    "task_id": "task-001",
    "order_id": "order-123",
    "will_deliver_order?": "NO! HEHEHEHE",
    "order_stolen_by_hacker?": "YES! HEHE"
}

# -------------------------------
# 🧪 Schema validation function
# ------------------------------

# -------------------------------
# 🚀 Main logic
# -------------------------------
def main():
    
    def encode_utf8(data,ctx):
        data_json = json.dumps(data)
        return data_json.encode("utf-8")
    
    def encode_utf8_key(data,ctx):
        return data.encode("utf-8")


    # ✅ Kafka producer configuration
    producer_config = {
        "bootstrap.servers": BOOTSTRAP
        }
    producer = Producer(producer_config)

    # ✅ Callback for delivery report
    def delivery_report(err, msg):
        if err is not None:
            print(f"❌ Delivery failed for record {msg.key()}: {err}")
        else:
            print(f"✅ Record {msg.key()} successfully produced to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")

    # ✅ Send the message
    try:
        producer.produce(
            topic=TOPIC,
            key= task["order_id"],
            value= encode_utf8(task, None),
            on_delivery=delivery_report
        )
        print(f"📤 Sending message to {TOPIC}: {task}")
        print("Message Sucessfully sent!!")
        producer.flush()
    except Exception as e:
        print(f"❌ Failed to send message to {BOOTSTRAP}/{TOPIC}: {e}")
        sys.exit(1)

# -------------------------------
# 🏁 Run the main function
# -------------------------------
if __name__ == "__main__":
    main()
