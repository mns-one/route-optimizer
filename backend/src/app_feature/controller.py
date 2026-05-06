from fastapi import APIRouter, HTTPException
from . import service
from .model import PlaceMetadata, RouteRequest

router = APIRouter(
    prefix = '/app-feature',
    tags=['app_feature']
)

@router.get("/search")
async def search_feature(location: str):
    if len(location.strip()) < 2:
        raise HTTPException(
            status_code=400,
            detail="Location name too short",
        )
    
    search_result = await service.search_place(location)
    return search_result

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

    direction_result = await service.get_directions(source_id, destinations)

    return direction_result
