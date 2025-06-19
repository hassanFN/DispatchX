from kafka import KafkaProducer

# point at the internal-only listener
producer = KafkaProducer(bootstrap_servers='kafka:9092')
producer.send('dispatch-tasks', b' New delivery task: #22319')
producer.flush()
print("✅ Test message sent")
