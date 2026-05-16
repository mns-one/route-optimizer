from components.map_render import render_map
from components.search import display_search_area, display_search_results
from components.search_results import display_user_selection_menu
from components.find_route.route import find_route
from components.route_cards import display_route_timeline

def render_ui(st):
    render_map(st)
    display_route_timeline(st)
    display_search_area(st)
    display_search_results(st)
    display_user_selection_menu(st)
    find_route(st)
