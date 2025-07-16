#!/usr/bin/env python3
import os, json, uuid, threading
from confluent_kafka import DeserializingConsumer, SerializingProducer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.json_schema import JSONDeserializer
from confluent_kafka.serialization import StringSerializer
from jsonschema import validate, ValidationError
import structlog

from assignment.config import load_assignment_weights
from assignment.scoring import choose_best_driver

# ---------------------- CONFIG ---------------------- #
BASE_DIR = os.path.dirname(__file__)
SCHEMA_PATH = os.path.join(BASE_DIR, "schemas", "dispatch_task_schema.json")
SCHEMA_REGISTRY_URL = os.getenv("SCHEMA_REGISTRY_URL", "http://schema-registry:8081")
BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP")
TOPIC = os.getenv("DISPATCH_TOPIC")
DLQ_TOPIC = os.getenv("DLQ_TOPIC")
GROUP_ID = "dispatcher_group"
DEBUG = os.getenv("DEBUG")

# ----------------- LOGGING ------------------ #
structlog.configure(processors=[structlog.processors.JSONRenderer()])
log = structlog.get_logger(service="Dispatch-consumer")
PROCESSED_MESSAGES = 0
FAILED_MESSAGES = 0
MESSAGES_PUSHED_TO_DLQ = 0

# -------------- SCHEMA SETUP -------------- #
with open(SCHEMA_PATH) as f:
    schema_str = f.read()
    schema = json.loads(schema_str)

schema_registry_client = SchemaRegistryClient({"url": SCHEMA_REGISTRY_URL})

json_deserializer = JSONDeserializer(
    schema_str=schema_str,
    schema_registry_client=schema_registry_client,
    from_dict=lambda obj, ctx: obj
)

# ---------------- CONSUMER SETUP ---------------- #
def key_deserializer(data, ctx):
    return data.decode("utf-8") if data else None

consumer_config = {
    "bootstrap.servers": BOOTSTRAP,
    "group.id": GROUP_ID,
    "key.deserializer": key_deserializer,
    "value.deserializer": json_deserializer,
    "auto.offset.reset": "latest"
}
consumer = DeserializingConsumer(consumer_config)
consumer.subscribe([TOPIC])

# ---------------- DLQ PRODUCER ---------------- #
dlq_producer = SerializingProducer({
    "bootstrap.servers": BOOTSTRAP,
    "key.serializer": StringSerializer("utf_8"),
    "value.serializer": StringSerializer("utf_8")
})

# -------------- DRIVER POOL --------------- #
# Replace this with dynamic DB/service lookup in prod!
drivers = [
    {
        "id": "driver1",
        "location": {"lat": 40.1141, "lon": -88.2252},
        "current_tasks": 1,
        "rating": 4.8,
        "status": "available"
    },
    {
        "id": "driver2",
        "location": {"lat": 40.1020, "lon": -88.2350},
        "current_tasks": 0,
        "rating": 4.6,
        "status": "available"
    },
    {
        "id": "driver3",
        "location": {"lat": 40.1200, "lon": -88.2100},
        "current_tasks": 2,
        "rating": 5.0,
        "status": "busy"
    }
]

# Recently processed tasks (in-memory store for API)
recent_tasks = []
MAX_TASK_HISTORY = 100

# ---------------- BUSINESS LOGIC ---------------- #
def process_task(task, msg):
    global PROCESSED_MESSAGES, recent_tasks
    try:
        log.info("🚚 Dispatching task", task=task)
        PROCESSED_MESSAGES += 1

        weights = load_assignment_weights()
        best_driver, score = choose_best_driver(task, drivers, weights)

        if best_driver:
            task['assigned_driver'] = best_driver['id']
            print(f"🚚 Assigned task {task['task_id']} to {best_driver['id']} (score={score:.2f})")
            log.info("✅ Assignment", task_id=task['task_id'], driver_id=best_driver['id'], score=score)
            # Here you could update driver state/persist assignment
        else:
            task['assigned_driver'] = None
            print(f"❌ No suitable driver found for {task['task_id']}")
            log.warn("❌ No suitable driver found", task_id=task['task_id'])

        # Store recent task for API consumers
        recent_tasks.append(task)
        if len(recent_tasks) > MAX_TASK_HISTORY:
            recent_tasks.pop(0)

        consumer.commit(msg)
    except Exception as e:
        log.error("Consumer Logic Failed", error=str(e))

def handle_kafka_message(msg):
    global FAILED_MESSAGES, MESSAGES_PUSHED_TO_DLQ
    correlation_id = "unknown"
    if msg.headers() is not None:
        headers = msg.headers()
        if headers:
            for k, v in headers:
                if k == "correlation_id":
                    correlation_id = v.decode("utf-8")
                    break
    else:
        log.info("Message has no headers")

    if msg.error():
        log.error("❌ Kafka error", correlation_id=correlation_id, error=msg.error())
        FAILED_MESSAGES += 1
        send_to_dlq("Kafka message error", None, msg)
        MESSAGES_PUSHED_TO_DLQ += 1
        return

    task = msg.value()
    if task is None:
        log.warning("⚠️ No message value to deserialize", correlation_id=correlation_id)
        return

    try:
        validate(instance=task, schema=schema)
        log.info(f"✅ Task {task['task_id']} is valid", correlation_id=correlation_id)
        if DEBUG:
            log.info("🧪 Task (debug):", task_content=json.dumps(task, indent=2), correlation_id=correlation_id)
        process_task(task, msg)
    except ValidationError as e:
        log.error("❌ Task validation failed", error=e.message, correlation_id=correlation_id)
        FAILED_MESSAGES += 1
        send_to_dlq("Schema validation failed", task, msg)
        MESSAGES_PUSHED_TO_DLQ += 1

    log.info("📍 Task metadata", topic=msg.topic(), partition=msg.partition(), offset=msg.offset(), key=msg.key(), correlation_id=correlation_id)
    log.info("Metrics", FAILED_MESSAGES=FAILED_MESSAGES, MESSAGES_PUSHED_TO_DLQ=MESSAGES_PUSHED_TO_DLQ, PROCESSED_MESSAGES=PROCESSED_MESSAGES)

def send_to_dlq(error_message, raw_data, msg):
    dlq_payload = {
        "error_message": error_message,
        "error": msg.error() if msg.error else None,
        "raw_message": raw_data if raw_data else None,
        "metadata": {
            "topic": msg.topic(),
            "partition": msg.partition(),
            "offset": msg.offset()
        }
    }
    try:
        dlq_producer.produce(topic=DLQ_TOPIC, key="invalid_message", value=json.dumps(dlq_payload))
        dlq_producer.flush()
    except Exception as e:
        log.info(f"Failed to send dlq message", topic=DLQ_TOPIC, error=str(e))

# ---- HTTP health server ----
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/healthz")
def healthz():
    return "ok", 200

# ----- API Endpoints ----- #
@app.route("/api/drivers")
def api_drivers():
    return jsonify(drivers)


@app.route("/api/tasks")
def api_tasks():
    return jsonify(recent_tasks)

def start_http_server():
    app.run(host="0.0.0.0", port=8080)

# ---- MAIN ENTRY ----
def kafka_loop():
    print(f"📡 Connected to Kafka at {BOOTSTRAP}")
    print(f"📬 Listening on topic: {TOPIC}...\n")
    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is not None:
                handle_kafka_message(msg)
    except KeyboardInterrupt:
        print("\n👋 Consumer shutdown initiated by user")
    finally:
        consumer.close()
        print("✅ Consumer connection closed")

if __name__ == "__main__":
    # Start Flask in background thread
    threading.Thread(target=start_http_server, daemon=True).start()
    kafka_loop()
