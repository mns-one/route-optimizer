from api.app_feature_api import search_location

def is_duplicate(new_place, selected_points):
    # check if place was already selected by user
    return any(p["id"] == new_place["id"] for p in selected_points)

def run_search(session_state, query):
    # call api and store response in state
    session_state.search_results = search_location(query)

def add_place(session_state, place):
    # insert and build list of all user selected places
    selected_points = session_state.selected_points

    if is_duplicate(place, selected_points):
        return False, "Location already selected!"

    selected_points.append(place)

    if session_state.source_id is None:
        session_state.source_id = place["id"]

    session_state.search_results = []
    session_state.clear_search = True
    return True, None
