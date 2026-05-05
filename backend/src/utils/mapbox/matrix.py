import httpx
import os
from dotenv import load_dotenv
from src.app_feature.model import ApiCoordinatesObj

load_dotenv()
token = os.getenv("MAPBOX_TOKEN")
if not token:
    raise ValueError("MAPBOX_TOKEN environment variable not set")

MATRIX_BASE_URL = os.getenv("MAPBOX_MATRIX_BASE_URL")
if not MATRIX_BASE_URL:
    raise ValueError("MAPBOX_MATRIX_BASE_URL environment variable not set")


async def get_route_matrix(coordinates: list[ApiCoordinatesObj]):

    if not coordinates:
        raise ValueError("coordinates list is empty")

    coord_str = ";".join(
        f"{c.lng},{c.lat}" for c in coordinates
    )

    url = f"{MATRIX_BASE_URL}/{coord_str}"

    params = {
        "access_token": token,
        "approaches": ";".join(["curb"] * len(coordinates))
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        return response.json()
