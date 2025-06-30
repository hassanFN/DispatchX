#!/bin/bash

set -e

KAFKA_HOST=${KAFKA_BOOTSTRAP:-kafka:9092}
SCHEMA_REGISTRY_URL=${SCHEMA_REGISTRY_URL:-http://schema-registry:8081}

KAFKA_HOSTNAME=$(echo "$KAFKA_HOST" | cut -d':' -f1)
KAFKA_PORT=$(echo "$KAFKA_HOST" | cut -d':' -f2)

echo "🔄 Waiting for Kafka at $KAFKA_HOSTNAME:$KAFKA_PORT..."

# Wait for Kafka DNS and TCP port
while ! nc -z "$KAFKA_HOSTNAME" "$KAFKA_PORT"; do
  echo "⏳ Kafka not ready yet at $KAFKA_HOSTNAME:$KAFKA_PORT"
  sleep 1
done

echo "✅ Kafka is reachable"

# Wait for Schema Registry
echo "🔄 Waiting for Schema Registry at $SCHEMA_REGISTRY_URL..."

until curl --silent --fail "$SCHEMA_REGISTRY_URL" >/dev/null; do
  echo "⏳ Schema Registry not reachable yet..."
  sleep 1
done

echo "✅ Schema Registry is reachable"

# Run the actual service
echo "🚀 All services are ready — starting send_test.py"
exec python send_test.py

