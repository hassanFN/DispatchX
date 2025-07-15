#modular

#ASSIGNMENT_WEIGHTS = {
#    "proximity": 1.0,       # Weight for proximity to pickup location 
#    "workload": 0.5,        # Weight for current workload of the driver
#    "rating": 2.0,          # Weight for driver rating
#    "available": 1000.0,    # Weight for availability of the driver
#    "eta": 0.2              # Weight for estimated time of arrival
#}



# The above defined dictionionary is used to calculate the score for each driver when assigning a task.
# It defines how much each factor influences the dispatch decision.
# For example, a driver's rating is considered twice as important as their proximity to the pickup location.
# Availability is given a very high weight to ensure that only available drivers are considered.


import json
import os

BASE_DIR = os.path.dirname(__file__)
WEIGHTS_FILE = os.path.join(BASE_DIR, "assignment_weights.json")

def load_assignment_weights():
    try:
        with open(WEIGHTS_FILE) as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ Failed to load assignment weights, using defaults: {e}")
        # Fallback to safe defaults
        return {
            "proximity": 1.0,
            "workload": 0.5,
            "rating": 2.0,
            "available": 1000.0,
            "eta": 0.2
        }
