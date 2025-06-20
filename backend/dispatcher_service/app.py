import os
import json
from jsonschema import validate, ValidationError
from kafka import KafkaConsumer

# Resolve schema path relative to this file
BASE_DIR = os.path.dirname(__file__)
SCHEMA_PATH = os.path.join(BASE_DIR, "schemas", "dispatch_task_schema.json")

# Load schema
with open(SCHEMA_PATH) as f:
    schema = json.load(f)

def safe_deserialize(v):
    try:
        return json.loads(v.decode("utf-8"))
    except Exception as e:
        print(f"❌ Skipping non-JSON message: {e}")
        return None

consumer = KafkaConsumer(
    "dispatch-tasks",
    bootstrap_servers="kafka:9092",
    value_deserializer=safe_deserialize,
    auto_offset_reset="latest",       # only new messages
    enable_auto_commit=True,
    group_id="dispatch_service_group"
)

print("🚀 Listening for messages on 'dispatch-tasks'...")

for msg in consumer:
    task = msg.value
    if task is None:
        continue

    print(f"📦 Received: {json.dumps(task)}")
    try:
        validate(instance=task, schema=schema)
        print(f"✅ Validated task {task['task_id']}, processing…")
    except ValidationError as e:
        print(f"❌ Schema validation failed for {task.get('task_id', '<no-id>')}: {e.message}")
        continue

    # … your dispatch logic …
