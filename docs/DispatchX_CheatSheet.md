# 🛰️ DispatchX - Quickstart Cheat Sheet

This guide helps you (and your partner) get DispatchX running smoothly—step by step, with all the key commands, directory context, and sample outputs.

---

## 📁 1. Project Structure

```
DispatchX/                       ← project root
├── docker-compose.yml
├── backend/
│   └── dispatcher_service/
│       ├── app.py
│       ├── send_test.py
│       ├── validate_schema.py
│       ├── wait-for-kafka.sh
│       ├── requirements.txt
│       ├── Dockerfile
│       └── schemas/
│           ├── dispatch_task_schema.json
│           ├── examples.py
│           └── __init__.py
```

---

## ⚙️ 2. Prerequisites

- Docker & Docker Compose installed
- Python 3.10+ (for running local scripts)
- Optionally, set up a Python virtual environment in `backend/dispatcher_service/` and install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🚀 3. Start the Kafka + Dispatcher Stack

From the **project root** (`DispatchX/`):

```bash
docker-compose down         # Clean up any old containers
docker-compose up -d        # Start everything in detached mode
```

---

## ✅ 4. Validate the JSON Schema

From `backend/dispatcher_service/`:

```bash
cd backend/dispatcher_service
python validate_schema.py
```

**Expected Output:**

```
⏳ Starting validate_schema.py
📄 Loaded dispatch_task_schema.json successfully
🔍 example_messages keys: ['happy_path', 'missing_status', 'invalid_lat_eta']
▶️ Testing happy_path
happy_path: ✅ Validation passed
▶️ Testing missing_status
missing_status: ❌ Validation error: 'status' is a required property
▶️ Testing invalid_lat_eta
invalid_lat_eta: ❌ Validation error: 'twenty' is not of type 'integer'
```

---

## 📤 5. Send a Test Message (Producer)

---

### 🔹 B) From Inside the Container

```bash
docker-compose exec -T dispatcher_service sh -c "python send_test.py"
```

**You should see:**

```
✅ Test message sent via kafka:9092 on topic 'dispatch-tasks'
```

---

## 🪵 6. View Dispatcher Logs (Consumer)
  (in a separate termnial run the following to view logs):
  
```bash
docker-compose logs -f dispatcher_service
```

**You’ll see:**

```
🚀 Listening for messages on 'dispatch-tasks'...
📦 Received: { … your JSON payload … }
✅ Validated task task-001, processing…
```

---

## ⚠️ 7. Test Invalid Payloads

1. Edit `send_test.py` to remove `"status"` or change `"eta_minutes": "oops"`.
2. Re-run the test message (using step 5A or 5B).
3. Watch logs (step 6):

```
📦 Received: { … invalid payload … }
❌ Schema validation failed for task-002: 'status' is a required property
```

---

## 🗂️ 8. Directory Shortcuts

| Shortcut | Command |
|----------|---------|
| Project root | `cd /Users/hassan/DispatchX` |
| Service folder | `cd backend/dispatcher_service` |
| Validate schema | `python validate_schema.py` |
| Run producer | `python send_test.py` *(after setting `KAFKA_BOOTSTRAP`)* |
| Rebuild Container | `docker-compose build dispatcher_service`
                    | `docker-compose up -d` |

---

## 👾 Git Quick Workflow

1. **Stage all changes**
   ```bash
   git add .

2. **Commit with a message**
   ```bash
   git commit -m "Your descriptive commit message"

3. **Push to your remote (default)**
   ```bash
   git push

5. **Tip: Check your status before and after staging**
   ```bash
   git status

 6. **Pull from GitHub Repo to local device**
    ```bash
    git fetch
    git pull

---

Happy hacking! 💻🔁
