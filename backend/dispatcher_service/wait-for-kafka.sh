#!/bin/sh
echo "🔄 Waiting for Kafka DNS resolution..."

# Wait for DNS resolution
while ! getent hosts kafka; do
  sleep 1
done

echo "✅ DNS resolved for Kafka, waiting for port 9092..."

# Wait for Kafka port
while ! nc -z kafka 9092; do
  sleep 1
done

echo "✅ Kafka is up — starting app"
python app.py  
