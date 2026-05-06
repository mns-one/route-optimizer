from pydantic import BaseModel
from typing import Optional, List

class Coordinates(BaseModel):
    latitude: float
    longitude: float

class ApiCoordinatesObj(BaseModel):
    lat: float
    lng: float

class RouteNodeObj(BaseModel):
    index: int
    id: str
    name: str
    address: Optional[str]
    input_lat: float
    input_lng: float
    route_name: str
    lng: float
    lat: float

class PlaceMetadata(BaseModel):
    id: str
    name: str
    full_address: Optional[str]
    coordinates: Coordinates

class RouteRequest(BaseModel):
    places: List[PlaceMetadata]
    source_id: str    

class Timeline(BaseModel):
    stop_number: int
    node: RouteNodeObj
    next_duration_sec: int