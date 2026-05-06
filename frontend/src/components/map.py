import folium
from streamlit_folium import st_folium

def render_map(st):
    m = folium.Map(location=(22.5937, 78.9629), zoom_start=5)

    render_marker(m, st.session_state.selected_points)
    render_route(m, st.session_state.direction_result)

    st_folium(m, width=700, height=500)

def render_marker(m, selected_points):
    if not selected_points:
        return

    if selected_points:
        coords_list = [
            (p["coordinates"]["latitude"], p["coordinates"]["longitude"])
            for p in selected_points
        ]

        for p in selected_points:
            folium.Marker(
                location=[p["coordinates"]["latitude"], p["coordinates"]["longitude"]],
                tooltip=f"{p['name']}",
                popup=f"{p['full_address']}",
                icon=folium.Icon(color="green")
            ).add_to(m)

        m.fit_bounds(coords_list)

def render_route(m, directions_data):
    if not directions_data:
        return

    routes = directions_data.get("routes", [])
    if not routes:
        return

    route = routes[0].get("geometry")
    if not route:
        return

    folium.GeoJson(
        route,
        style_function=lambda x: {
            "color": "blue",
            "weight": 5,
            "opacity": 0.8
        }
    ).add_to(m)
