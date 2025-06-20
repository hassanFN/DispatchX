#!/usr/bin/env python3
import os
import sys
import json
from jsonschema import validate, ValidationError
from kafka import KafkaProducer

# ------- Configuration -------
BASE_DIR = os.path.dirname(__file__)
SCHEMA_PATH = os.path.join(BASE_DIR, "schemas", "dispatch_task_schema.json")
BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "kafka:9092")
TOPIC = os.getenv("DISPATCH_TOPIC", "dispatch-tasks")
# -----------------------------

def load_schema(path):
    with open(path) as f:
        return json.load(f)

def build_producer(bootstrap):
    return KafkaProducer(
        bootstrap_servers=bootstrap,
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )

def main():
    # Load and validate schema
    schema = load_schema(SCHEMA_PATH)

    # Example task payload
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

    # Validate payload
    try:
        validate(instance=task, schema=schema)
    except ValidationError as e:
        print(f"❌ Schema validation error: {e.message}")
        sys.exit(1)

    # Send to Kafka
    producer = build_producer(BOOTSTRAP)
    try:
        producer.send(TOPIC, task)
        producer.flush()
    except Exception as e:
        print(f"❌ Failed to send message to {BOOTSTRAP}/{TOPIC}: {e}")
        sys.exit(1)

    print(f"✅ Test message sent via {BOOTSTRAP} on topic '{TOPIC}'")

if __name__ == "__main__":
    main()
