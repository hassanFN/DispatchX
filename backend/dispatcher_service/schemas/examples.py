# backend/dispatcher_service/schemas/examples.py

example_messages = {
    "happy_path": {
        "schema_version": 1,
        "task_id": "    ",
        "order_id": "order-123",
        "pickup": {
            "address": "123 Main St, Springfield, IL",
            "lat": 40.1123,
            "lon": -88.2284
        },
        "dropoff": {
            "address": "456 Elm St, Lincoln, IL",
            "lat": 40.1500,
            "lon": -88.2500
        },
        "timestamp": "2025-06-21T10:00:00Z",
        "status": "pending",
        "priority": "high",
        "assignee_id": None,
        "eta_minutes": 15,
        "instructions": "Leave at front door, ring bell twice",
        "metadata": {
            "fragile": True,
            "customer_notes": "Handle with care"
        }
    },
    "missing_status": {
        "schema_version": 1,
        "task_id": "task-002",
        "order_id": "order-124",
        "pickup": {
            "address": "789 Oak Ave, Peoria, IL",
            "lat": 40.6936,
            "lon": -89.5889
        },
        "dropoff": {
            "address": "321 Pine Rd, Decatur, IL",
            "lat": 39.8403,
            "lon": -88.9548
        },
        "timestamp": "2025-06-21T11:30:00Z"
    },
    "invalid_lat_eta": {
        "schema_version": 1,
        "task_id": "task-003",
        "order_id": 125,
        "pickup": {
            "address": "1600 Pennsylvania Ave NW, Washington, DC",
            "lat": 95.0000,
            "lon": -77.0365
        },
        "dropoff": {
            "address": "1 Infinite Loop, Cupertino, CA",
            "lat": 37.3317,
            "lon": -122.0302
        },
        "timestamp": "2025-06-21T12:45:00Z",
        "status": "assigned",
        "eta_minutes": "twenty",
        "metadata": {}
    }
}
