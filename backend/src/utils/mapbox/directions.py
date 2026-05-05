import httpx
import os
from dotenv import load_dotenv
from src.app_feature.model import ApiCoordinatesObj


load_dotenv()
token = os.getenv("MAPBOX_TOKEN")
if not token:
    raise ValueError("MAPBOX_TOKEN environment variable not set")

DIRECTION_BASE_URL = os.getenv("MAPBOX_DIRECTION_BASE_URL")
if not DIRECTION_BASE_URL:
    raise ValueError("MAPBOX_DIRECTION_BASE_URL environment variable not set")

async def get_route_direction(coordinates: list[ApiCoordinatesObj]):
    coord_str = ";".join(
        f"{c.lng},{c.lat}" for c in coordinates
    )

    url = f"{DIRECTION_BASE_URL}/{coord_str}"

    params = {
    "access_token": token,
    "geometries": "geojson"
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        return response.json()

