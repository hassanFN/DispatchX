import os
import importlib
import types

import pytest

# Ensure API key so module imports (must look valid)
os.environ.setdefault("GOOGLE_MAPS_API_KEY", "AIza" + "X" * 35)

from dispatcher_service.assignment import scoring

# Patch google maps client to avoid network calls
class DummyGMaps:
    def directions(self, origin, dest, mode="driving", departure_time="now"):
        return [{"legs": [{"duration": {"value": 600}}]}]

scoring.gmaps = DummyGMaps()

def test_no_available_drivers():
    task = {"pickup": {"lat": 0.0, "lon": 0.0}, "task_id": "t1"}
    drivers = [
        {"id": "d1", "location": {"lat": 0.0, "lon": 0.0}, "current_tasks": 0, "rating": 5, "status": "busy"}
    ]
    weights = {"proximity":1, "workload":1, "rating":1, "available":1000, "eta":1}
    driver, score = scoring.choose_best_driver(task, drivers, weights)
    assert driver is None and score is None

def test_same_score_prefers_first():
    task = {"pickup": {"lat": 0.0, "lon": 0.0}, "task_id": "t1"}
    drivers = [
        {"id": "d1", "location": {"lat": 0.0, "lon": 0.0}, "current_tasks": 0, "rating": 5, "status": "available"},
        {"id": "d2", "location": {"lat": 0.0, "lon": 0.0}, "current_tasks": 0, "rating": 5, "status": "available"},
    ]
    weights = {"proximity":1, "workload":1, "rating":1, "available":1000, "eta":1}
    s1 = scoring.score_driver(task, drivers[0], weights)
    s2 = scoring.score_driver(task, drivers[1], weights)
    assert s1 == s2
    best, _ = scoring.choose_best_driver(task, drivers, weights)
    assert best["id"] == "d1"


def test_missing_data_raises():
    task = {"pickup": {"lat": 0.0, "lon": 0.0}, "task_id": "t1"}
    drivers = [
        {"id": "d1", "location": {"lat": 0.0, "lon": 0.0}, "current_tasks": 0, "rating": 5, "status": "available"},
        {"id": "d2", "current_tasks": 0, "rating": 5, "status": "available"},
    ]
    weights = {"proximity":1, "workload":1, "rating":1, "available":1000, "eta":1}
    with pytest.raises(KeyError):
        scoring.choose_best_driver(task, drivers, weights)
