from pydantic import BaseModel

class PlaceMetadata(BaseModel):
    id: str
    name: str
    full_address: str | None
    coordinates: dict