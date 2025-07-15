import * as React from "react";
import Map, { Marker, Popup } from "react-map-gl";
import "mapbox-gl/dist/mapbox-gl.css";

const MAPBOX_TOKEN = import.meta.env.VITE_MAPBOX_TOKEN;

export default function MapView({ drivers = [], tasks = [] }) {
  const [selectedTask, setSelectedTask] = React.useState(null);

  return (
    <Map
      initialViewState={{
        longitude: -88.2260,
        latitude: 40.1106,
        zoom: 12
      }}
      style={{ width: "100%", height: "80vh", borderRadius: "18px" }}
      mapStyle="mapbox://styles/mapbox/streets-v11"
      mapboxAccessToken={MAPBOX_TOKEN}
    >
      {/* Driver Markers */}
      {drivers.map((driver) => (
        <Marker
          key={driver.id}
          longitude={driver.location.lon}
          latitude={driver.location.lat}
          anchor="bottom"
        >
          <span style={{ fontSize: "1.5rem" }} role="img" aria-label="driver">
            🚗
          </span>
        </Marker>
      ))}

      {/* Task Markers */}
      {tasks.map((task) => (
        <Marker
          key={task.task_id}
          longitude={task.pickup.lon}
          latitude={task.pickup.lat}
          anchor="bottom"
          onClick={e => {
            e.originalEvent.stopPropagation();
            setSelectedTask(task);
          }}
        >
          <span style={{ fontSize: "1.5rem", cursor: "pointer" }} role="img" aria-label="task">
            📦
          </span>
        </Marker>
      ))}

      {selectedTask && (
        <Popup
          longitude={selectedTask.pickup.lon}
          latitude={selectedTask.pickup.lat}
          anchor="top"
          onClose={() => setSelectedTask(null)}
          closeOnClick={false}
        >
          <div>
            <strong>Task ID:</strong> {selectedTask.task_id} <br />
            <strong>Pickup:</strong> {selectedTask.pickup.lat}, {selectedTask.pickup.lon}
          </div>
        </Popup>
      )}
    </Map>
  );
}
