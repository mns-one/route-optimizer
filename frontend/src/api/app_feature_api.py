import os
from dotenv import load_dotenv
import requests

load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL")
if not BACKEND_URL:
    raise ValueError("BACKEND_URL environment variable not set")

def search_location(query: str):
    search_url = f"{BACKEND_URL}/search"
    response = requests.get(search_url, params={"location": query}, timeout=5)
    response.raise_for_status()
    return response.json()

def get_optimal_route(selected_points, source_id: str):
    direction_url = f"{BACKEND_URL}/direction"
    payload = {
        "places": selected_points,
        "source_id": source_id,
    }
    response = requests.post(direction_url, json=payload, timeout=5)
    response.raise_for_status()
    return response.json()

