## 🚀 DispatchX Overview

DispatchX is a distributed microservices platform using Kafka and Kubernetes, designed for real-time task dispatch, fault-tolerant workflows, and DevSecOps automation.

---

### 📁 Folder Structure

- `backend/` – Kafka-connected microservices
- `frontend/` – (Optional) UI dashboard
- `infra/` – Cloud infrastructure-as-code (Terraform for GCP + AWS)
- `docs/` – System architecture notes, meeting docs
- `.github/workflows/` – GitHub Actions for CI/CD

---

### 👯‍♂️ Team

- Hassan (@hassanFN)
- Loay (@pepedafrog22)

---

### ✅ Next Steps

- [ ] Set up Kafka microservice skeleton
- [ ] Write `docker-compose.yml` for local dev
- [ ] Start Terraform infra for GCP
- [ ] Add CI/CD via GitHub Actions

### 🚦 Assignment Algorithm

Incoming tasks are scored against each available driver using a weighted formula
defined in `backend/dispatcher_service/assignment/assignment_weights.json`.
The score favors drivers who are closer, less busy and highly rated:

```
score = (proximity * -distance_km)
        + (workload * -current_tasks)
        + (rating * driver_rating)
        + (available * availability_flag)
        + (eta * -estimated_minutes)
```

Only drivers with `status: "available"` are considered.  The driver with the
highest score is assigned to the task and the assignment is exposed via the
REST API.

### 🏃‍♂️ Running Locally

```
docker-compose up --build
```

The dispatcher service exposes HTTP endpoints on `http://localhost:8000`.
To run the React frontend:

```
cd frontend
npm install
npm run dev
```

The map will poll `/api/drivers` and `/api/tasks` every few seconds to show live
updates.
