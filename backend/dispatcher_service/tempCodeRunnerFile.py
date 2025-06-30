#!/usr/bin/env python3
import os
import json
from confluent_kafka import DeserializingConsumer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.json_schema import JSONDeserializer
from jsonschema import validate, ValidationError


# --------- CONFIGURATION --------- #
BASE_DIR = os.path.dirname(__file__)
SCHEMA_PATH = os.path.join(BASE_DIR, "schemas", "dispatch_task_schema.json")

SCHEMA_REGISTRY_URL = os.getenv("SCHEMA_REGISTRY_URL", "http://schema-registry:8081")
BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "kafka:9092")
TOPIC = os.getenv("DISPATCH_TOPIC", "dispatch-tasks")
GROUP_ID = "dispatcher_group"
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
# ----------------------------------


# --------- LOAD SCHEMA --------- #
with open(SCHEMA_PATH) as f:
    schema_str = f.read()
    schema = json.loads(schema_str)
# --------------------------------


# --------- SCHEMA REGISTRY CLIENT --------- #
schema_registry_conf = {
    "url": SCHEMA_REGISTRY_URL
}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)
# ------------------------------------------


# --------- DESERIALIZER --------- #
def dict_to_object(obj, ctx):
    return obj

json_deserializer = JSONDeserializer(
    schema_str=schema_str,
    schema_registry_client=schema_registry_client,
    from_dict=dict_to_object
)
# --------------------------------


# --------- CONSUMER CONFIG --------- #

def key_deserializer(data, ctx):
    if data is None:
        return None
    return data.decode("utf-8", errors="replace")

consumer_config = {
    "bootstrap.servers": BOOTSTRAP,
    "group.id": GROUP_ID,
    "key.deserializer": key_deserializer,
    "value.deserializer": json_deserializer,
    "auto.offset.reset": "latest"
}
consumer = DeserializingConsumer(consumer_config)
consumer.subscribe([TOPIC])
# ------------------------------------


def process_task(task):
    # Placeholder for your actual business logic
    print(f"🚚 Dispatching task {task['task_id']}... ✅")


print(f"📡 Connected to Kafka at {BOOTSTRAP}, schema registry at {SCHEMA_REGISTRY_URL}")
print(f"📬 Listening on topic: {TOPIC}...\n")

try:
    while True:
        msg = consumer.poll(timeout=1.0)

        if msg is None:
            continue

        if msg.error():
            print(f"❌ Kafka error: {msg.error()}")
            continue

        task = msg.value()
        if task is None:
            print("⚠️ No message deserialized")
            continue

        try:
            validate(instance=task, schema=schema)
            print(f"\n✅ Task {task['task_id']} is valid and ready to process")
            if DEBUG:
                print(f"📦 Task content: {json.dumps(task, indent=2)}")
            process_task(task)
        except ValidationError as e:
            print(f"❌ Task validation failed: {e.message}")
            continue

        print(f"📬 Metadata: topic={msg.topic()}, partition={msg.partition()}, offset={msg.offset()}, key={msg.key()}")

except KeyboardInterrupt:
    print("\n👋 Consumer shutdown initiated by user")

finally:
    consumer.close()
    print("✅ Consumer connection closed")