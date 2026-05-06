from components.map import render_map
from components.search import display_search_area, display_search_results
from components.user_selection import display_user_selected_points
from components.route import find_route
from components.route_timeline import display_route_timeline

def render_ui(st):
    render_map(st)
    display_route_timeline(st)
    display_search_area(st)
    display_search_results(st)
    display_user_selected_points(st)
    find_route(st)
