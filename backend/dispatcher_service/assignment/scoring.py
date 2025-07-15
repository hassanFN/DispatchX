import math

import os
import googlemaps
from time import sleep

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
if not GOOGLE_MAPS_API_KEY:
    raise EnvironmentError("❌ GOOGLE_MAPS_API_KEY not set in environment variables.")
gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)


from math import radians, cos, sin, asin, sqrt

def haversine(coord1, coord2):
    """
    Returns distance in kilometers between two geo coordinates.
    Coordinates are dicts with 'lat' and 'lon' in decimal degrees.
    """
    lat1, lon1 = coord1['lat'], coord1['lon']
    lat2, lon2 = coord2['lat'], coord2['lon']
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers
    return c * r
# Haversine distance function to calculate real-world distances


def compute_distance(pickup, driver_loc):
    """
    Compute Haversine (real-world geo) distance between pickup and driver, in km.
    """
    return haversine(pickup, driver_loc)

def estimate_eta(driver, pickup):
    """
    Get real ETA (in minutes) from Google Directions API.
    Fallback to base calculation if API fails.
    """
    origin = f"{driver['location']['lat']},{driver['location']['lon']}"
    dest = f"{pickup['lat']},{pickup['lon']}"

    try:
        result = gmaps.directions(origin, dest, mode="driving", departure_time="now")
        if result and 'legs' in result[0]:
            eta_sec = result[0]['legs'][0]['duration']['value']
            # Add overhead for driver's current tasks (simulate stops)
            return eta_sec / 60 + driver['current_tasks'] * 3
    except Exception as e:
        print(f"⚠️ Google Maps ETA failed: {e}")
        sleep(0.5)  # throttle if error loop
    # Fallback if error
    dist = compute_distance(pickup, driver['location'])
    return dist * 2 + driver['current_tasks'] * 3


def score_driver(task, driver, weights):
    """
    Calculate a composite score for the driver for this task.
    Higher score means better fit.
    """
    pickup = task['pickup']
    proximity = compute_distance(pickup, driver['location'])
    workload = driver['current_tasks']
    rating = driver['rating']
    available = 1 if driver['status'] == "available" else 0
    eta = estimate_eta(driver, pickup)

    return (
        weights['proximity'] * -proximity +     # Closer is better (negative for lower distance)
        weights['workload'] * -workload +       # Less workload is better
        weights['rating'] * rating +            # Higher rating is better
        weights['available'] * available +      # Only available drivers count
        weights['eta'] * -eta                   # Lower ETA is better
    )

def choose_best_driver(task, drivers, weights):
    """
    Return the available driver with the highest score, and their score.
    If no available driver, returns (None, None).
    """
    scored = []
    for driver in drivers:
        scored.append((score_driver(task, driver, weights), driver)) 
    scored.sort(reverse=True, key=lambda tup: tup[0]) #descending order, highest score first

    for score, driver in scored:
        if driver['status'] == "available": #only consider available drivers
            return driver, score
    return None, None
