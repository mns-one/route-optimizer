from src.utils.mapbox.search import get_places_async
from .model import PlaceMetadata

async def search_place(place: str) -> list[PlaceMetadata]:
    return await get_places_async(place)
    