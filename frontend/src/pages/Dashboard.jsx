import React from "react";
import Map from "../components/Map";

export default function Dashboard() {
  // For demo: replace with real data from backend
  const drivers = [
    { id: "driver1", location: { lat: 41.88, lon: -87.63 }, status: "available" },
    { id: "driver2", location: { lat: 41.85, lon: -87.68 }, status: "busy" },
  ];
  const tasks = [
    { task_id: "task1", pickup: { lat: 41.89, lon: -87.61 } },
    { task_id: "task2", pickup: { lat: 41.86, lon: -87.66 } },
  ];

  return (
    <div>
      <h1>Dispatch Dashboard</h1>
      <Map drivers={drivers} tasks={tasks} />
    </div>
  );
}
