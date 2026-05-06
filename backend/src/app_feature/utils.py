from .model import PlaceMetadata, ApiCoordinatesObj, RouteNodeObj, Timeline

def extract_coordinates(destinations: list[PlaceMetadata]) -> list[ApiCoordinatesObj]:
    coords_list = []

    for d in destinations:
        lat = d.coordinates.latitude
        lng = d.coordinates.longitude

        if lat is not None and lng is not None:
            coords_list.append(ApiCoordinatesObj(lat=lat, lng=lng))

    return coords_list

def get_duration_matrix(matrix_response: dict) -> list[list[float]]:
    return matrix_response.get("durations")

def build_nodes(route_matrix_data: dict, destinations: list[PlaceMetadata]) -> list[RouteNodeObj]:
    nodes: list[RouteNodeObj] = []

    for i, src in enumerate(route_matrix_data["sources"]):
        d = destinations[i]

        nodes.append(
            RouteNodeObj(
                index=i,
                id=d.id,
                name=d.name,
                address=d.full_address,
                input_lat=d.coordinates.latitude,
                input_lng=d.coordinates.longitude,
                route_name=src.get("name") or f"Point {i}",
                lng=src["location"][0],
                lat=src["location"][1],
            )
        )

    return nodes

def find_node_index_by_id(nodes: list[RouteNodeObj], source_id: str) -> int:
    for node in nodes:
        if node.id == source_id:
            return node.index

    raise ValueError("Source id not found")

def reorder_nodes(nodes: list[RouteNodeObj], route_order: list[int]) -> list[RouteNodeObj]:
    ordered_nodes = []

    for i in route_order:
        ordered_nodes.append(nodes[i])

    return ordered_nodes

def extract_optimal_coordinates(ordered_nodes: list[RouteNodeObj]) -> list[ApiCoordinatesObj]:
    optimized_coords = []

    for node in ordered_nodes:
        optimized_coords.append(ApiCoordinatesObj(lng=node.lng, lat=node.lat))

    return optimized_coords

def build_route_timeline(nodes: list[RouteNodeObj], route_order: list[int], durations: list[list[float]]) -> list[Timeline]:
    timeline = []

    for i, node_idx in enumerate(route_order):
        node = nodes[node_idx]

        if i < len(route_order) - 1:
            next_idx = route_order[i + 1]
            duration_sec = durations[node_idx][next_idx]
        else:
            duration_sec = None

        timeline.append({
            "stop_number": i + 1,
            "node": node.model_dump(),
            "next_duration_sec": duration_sec,
        })

    return timeline

def path_optimizer_algorithm(duration_matrix: list[list[float]], source: int) -> list[int]:
    n = len(duration_matrix)
    visited = [False] * n
    route = [source]
    visited[source] = True

    current = source

    for _ in range(n - 1):
        next_node = None
        min_cost = float("inf")

        for j in range(n):
            if not visited[j] and duration_matrix[current][j] < min_cost:
                min_cost = duration_matrix[current][j]
                next_node = j

        route.append(next_node)
        visited[next_node] = True
        current = next_node

    return route






    
