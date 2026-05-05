from fastapi import APIRouter, HTTPException
from . import service
from .model import PlaceMetadata, RouteRequest

router = APIRouter(
    prefix = '/app-feature',
    tags=['app_feature']
)

@router.get("/search")
async def search_feature(place_name: str) -> list[PlaceMetadata]:
    if not place_name:
        return{"Message": "Enter a valid location..."}
    return await service.search_place(place_name)

@router.post("/direction")
async def direction_feature(payload: RouteRequest):

    destinations = payload.places
    source_id = payload.source_id

    if len(destinations) <= 2:
        raise HTTPException(
            status_code=400,
            detail="At least 3 destination objects are required",
        )

    if not any(destination.id == source_id for destination in destinations):
        raise HTTPException(
            status_code=400,
            detail="source_id must match one of the destination object IDs",
        )

    directions = await service.get_directions(source_id, destinations)

    return directions
