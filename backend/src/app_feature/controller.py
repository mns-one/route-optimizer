from fastapi import APIRouter
from . import service
from .model import PlaceMetadata

router = APIRouter(
    prefix = '/app-feature',
    tags=['app_feature']
)

@router.get("/search")
async def search_feature(place_name: str) -> list[PlaceMetadata]:
    if not place_name:
        return{"Message": "Enter a valid location..."}
    return await service.search_place(place_name)