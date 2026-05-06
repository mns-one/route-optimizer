from fastapi import APIRouter, HTTPException, Request
from . import service
from .model import PlaceMetadata, RouteRequest
from .model import RouteRequest
from src.core.rate_limiter import limiter

router = APIRouter(
    prefix = '/app-feature',
    tags=['app_feature']
)

@router.get("/search")
@limiter.limit("10/minute")
@limiter.limit("30/day")
async def search_feature(request: Request, location: str):
    if len(location.strip()) < 2:
        raise HTTPException(
            status_code=400,
            detail="Location name too short",
        )
    
    search_result = await service.search_place(location)
    return search_result

@router.post("/direction")
@limiter.limit("5/minute")
@limiter.limit("10/day")
async def direction_feature(request: Request, payload: RouteRequest):

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
