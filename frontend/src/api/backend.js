const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || "http://localhost:8000";

export async function fetchTasks() {
  const res = await fetch(`${BACKEND_URL}/api/tasks`);
  return res.json();
}

export async function fetchDrivers() {
  const res = await fetch(`${BACKEND_URL}/api/drivers`);
  return res.json();
}
