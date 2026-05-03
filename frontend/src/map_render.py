import folium
from streamlit_folium import st_folium


def render_selected_points(selected_points):

    if not selected_points:
        m = folium.Map(location=(45.5236, -122.6750))
        st_folium(m, width=700, height=500)
    else:
        coords_list = [
            (p["coordinates"]["latitude"], p["coordinates"]["longitude"])
            for p in selected_points
        ]

        m = folium.Map(location=coords_list[0], zoom_start=12)

        for p in selected_points:
            folium.Marker(
                location=[p["coordinates"]["latitude"], p["coordinates"]["longitude"]],
                tooltip=f"{p['name']}",
                popup=f"{p['full_address']}",
                icon=folium.Icon(color="green")
            ).add_to(m)

        # auto-fit map bounds
        m.fit_bounds(coords_list)

        st_folium(m, width=700, height=500)
