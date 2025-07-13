#!/usr/bin/env python3
import os
import sys
import json
from jsonschema import validate, ValidationError
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.json_schema import JSONSerializer
from confluent_kafka import SerializingProducer
import uuid 
import structlog 


# -------------------------------
# 🔧 Configuration
# -------------------------------
BASE_DIR = os.path.dirname(__file__)
SCHEMA_PATH = os.path.join(BASE_DIR, "schemas", "dispatch_task_schema.json")
BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP")
TOPIC = os.getenv("DISPATCH_TOPIC")
SCHEMA_REGISTRY_URL = os.getenv("SCHEMA_REGISTRY_URL")


#--------------Struct Log config --------------------
structlog.configure(processors=[structlog.processors.JSONRenderer()])
log = structlog.get_logger(service="send_test")
correlation_id = str(uuid.uuid4())
#----------------------------------------------------

# -------------------------------
# ✅ Example payload (must match schema!)
# -------------------------------
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
        "lon": -88.2500,
        "test": 123
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





# -------------------------------
# 🧪 Schema validation function
# -------------------------------
def validate_task(task, schema_path):
    with open(schema_path) as f:
        schema = json.load(f)
    validate(instance=task, schema=schema)

# -------------------------------
# 🚀 Main logic
# -------------------------------
def main(TOPIC, SCHEMA_REGISTRY_URL):
    # ✅ Validate the task before sending
    try:
        validate_task(task, SCHEMA_PATH)
        log.info("✅ Schema validation succeeded", task=task["task_id"], correlation_id=correlation_id)
    except ValidationError as e:
        log.error("❌ Schema validation failed", error=e.message, correlation_id=correlation_id)
        sys.exit(1)

    # ✅ Load JSON schema as a string
    with open(SCHEMA_PATH) as f:
        schema_str = f.read() 

    # ✅ Create Schema Registry client
    schema_registry_conf = {"url": SCHEMA_REGISTRY_URL}
    schema_registry_client = SchemaRegistryClient(schema_registry_conf)

    # ✅ JSON serializer with schema + registry client
    def object_to_dict(obj, ctx):
        return obj
    
    def encode_utf8(key,ctx):
        return key.encode("utf-8")

    json_serializer = JSONSerializer(schema_str, schema_registry_client, to_dict=object_to_dict)

    # ✅ Kafka producer configuration
    producer_config = {
        "bootstrap.servers": BOOTSTRAP,
        "key.serializer": encode_utf8,    
        "value.serializer": json_serializer,
    }
    producer = SerializingProducer(producer_config)

    # ✅ Callback for delivery report
    def delivery_report(err, msg):
        if err is not None:
            log.error("❌ Delivery failed", error=str(err), topic=msg.topic(), key=msg.key().decode(), correlation_id=correlation_id)
            print("ERROR! could be the delivery_report function causing this")
        else:
           log.info("✅ Delivery succeeded", topic=msg.topic(), offset=msg.offset(), correlation_id=correlation_id)
        #log.info("✅ Delivery succeeded", topic=msg.topic(), key=msg.key().decode(), offset=msg.offset(), correlation_id=correlation_id)

    # ✅ Send the message
    try:
        producer.produce(
            topic=TOPIC,
            key=task["order_id"],
            value=task,
            headers=[("correlation_id", correlation_id.encode("utf-8"))],  
            on_delivery=delivery_report
        )
        log.info("📤 Message sent",  topic=TOPIC, task=task, correlation_id=correlation_id)  
        producer.flush()
    except Exception as e:
        log.error("❌ Failed to send message", error=str(e), correlation_id=correlation_id)
        sys.exit(1)

# -------------------------------
# 🏁 Run the main function
# -------------------------------



# ---- HTTP health server ----

from flask import Flask
import threading

app = Flask(__name__)

@app.route("/healthz")
def healthz():
    return "ok", 200

def start_http_server():
    app.run(host="0.0.0.0", port=8080)

# ---- App Entry ----
if __name__ == "__main__":
    threading.Thread(target=start_http_server, daemon=True).start()
    main(TOPIC, SCHEMA_REGISTRY_URL)