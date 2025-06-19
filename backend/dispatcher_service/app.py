from kafka import KafkaConsumer

TOPIC_NAME = 'dispatch-tasks'

consumer = KafkaConsumer(
    TOPIC_NAME,
    bootstrap_servers='kafka:9092',    # internal-only
    auto_offset_reset='earliest',
    group_id='dispatch-group'
)

print(f"🚀 Listening for messages on '{TOPIC_NAME}'...")

for message in consumer:
    print(f"📦 Received: {message.value.decode('utf-8')}")
