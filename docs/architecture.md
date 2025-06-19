# DispatchProX

🚀
## 🔧 Tech Stack
- **Kafka** for message queuing
- **Python** for service logic (consumer + producer)
- **Docker + Docker Compose** for container orchestration
- **Netcat (nc)** for Kafka health checks

## 📦 Architecture

## ⚙️ How It Works
1. `send_test.py` sends a message to the `dispatch-tasks` Kafka topic.
2. Kafka queues the message internally.
3. `dispatcher_service/app.py` (Python KafkaConsumer) receives and logs it.
4. `wait-for-kafka.sh` ensures startup ordering inside Docker.

## 🧪 Running Locally

```bash
docker-compose up --build


to send a message
docker-compose exec dispatcher_service python send_test.py

to view logs
docker-compose logs -f dispatcher_service

