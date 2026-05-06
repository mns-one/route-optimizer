import httpx
from fastapi import HTTPException
from src.utils.mapbox.search import get_place_data
from src.utils.mapbox.matrix import get_route_matrix
from src.utils.mapbox.directions import get_route_direction
from .model import PlaceMetadata
from .utils import extract_coordinates, get_duration_matrix, build_nodes, find_node_index_by_id, path_optimizer_algorithm, reorder_nodes, extract_optimal_coordinates, build_route_timeline


async def search_place(location: str) -> list[PlaceMetadata]:
    try:
        place_data = await get_place_data(location)
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=502,
            detail="Search provider returned an error response",
        ) from exc
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=503,
            detail="Unable to reach search provider",
        ) from exc
    
    return place_data
    
async def get_directions(source_id: str, destinations: list[PlaceMetadata]):

    #Get time/distance Matrix
    coordinates = extract_coordinates(destinations)

    try:
        route_matrix_data = await get_route_matrix(coordinates)
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=502,
            detail="Matrix provider returned an error response",
        ) from exc
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=503,
            detail="Unable to reach matrix provider",
        ) from exc

    duration_matrix = get_duration_matrix(route_matrix_data)
    if not duration_matrix:
        raise HTTPException(
            status_code=502,
            detail="Matrix response did not include duration data.",
        )
    

    #Run path optimizer algorithm
    nodes = build_nodes(route_matrix_data, destinations)
    source_index = find_node_index_by_id(nodes, source_id)

    optimal_route_order = path_optimizer_algorithm(duration_matrix, source_index)

    optimal_nodes_order = reorder_nodes(nodes, optimal_route_order)
    optimal_coordinates_order = extract_optimal_coordinates(optimal_nodes_order)
    

    #Fetch direction geometry n return optimized route
    try:
        route_direction = await get_route_direction(optimal_coordinates_order)
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=502,
            detail="Direction provider returned an error response",
        ) from exc
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=503,
            detail="Unable to reach direction provider",
        ) from exc    
    
    route_timeline = build_route_timeline(optimal_nodes_order, optimal_route_order, duration_matrix)
    
    route_data = {
        "timeline": route_timeline,
        "direction": route_direction,
    }

    return route_data
