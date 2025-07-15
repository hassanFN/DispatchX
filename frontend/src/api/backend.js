const BACKEND_URL = "http://localhost:YOUR_BACKEND_PORT"; // or wherever your API will run

export async function fetchTasks() {
  const res = await fetch(`${BACKEND_URL}/api/tasks`);
  return res.json();
}

export async function fetchDrivers() {
  const res = await fetch(`${BACKEND_URL}/api/drivers`);
  return res.json();
}
