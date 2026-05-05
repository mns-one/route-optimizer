import httpx
import os
from dotenv import load_dotenv
from src.app_feature.model import PlaceMetadata

load_dotenv()
token = os.getenv("MAPBOX_TOKEN")
if not token:
    raise ValueError("MAPBOX_TOKEN environment variable not set")

SEARCH_BASE_URL = os.getenv("MAPBOX_SEARCH_BASE_URL")
if not SEARCH_BASE_URL:
    raise ValueError("MAPBOX_SEARCH_BASE_URL environment variable not set")


async def get_place_data(search_text: str) -> list[PlaceMetadata]:
    params = {
        "q": search_text,
        "limit": 3,
        "access_token": token
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(SEARCH_BASE_URL, params=params, timeout=5)
        response.raise_for_status()
        results = response.json()
    
        data = []

        for result in results.get("features", []):

            props = result.get("properties", {})

            parsed_result = PlaceMetadata(
                id=props.get("mapbox_id"),
                name=props.get("name"),
                full_address=props.get("full_address"),
                coordinates=props.get("coordinates", {}),
            )
            data.append(parsed_result)

        return data
