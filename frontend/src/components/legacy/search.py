from utils.error_handler import handle_request_error
from api.app_feature_api import search_location

def is_duplicate(new_place, selected_points):
    return any(p["id"] == new_place["id"] for p in selected_points)

def display_search_area(st):
    st.title("Search & Add Multi-points")

    query = st.text_input("Enter area", key="search_input")

    if st.button("Search") and query:
        try:
            st.session_state.search_results = search_location(query)

        except Exception as exc:
            handle_request_error(exc)

def display_search_results(st):
    results = st.session_state.get("search_results", [])

    if results:
        st.subheader("Search Results")

        for idx, place in enumerate(results):
            label = f"{place['name']} - {place['full_address'] or ''}"

            col1, col2 = st.columns([4, 1])

            with col1:
                st.write(label)

            with col2:
                if st.button("Add", key=f"add_{idx}"):
                    if not is_duplicate(place, st.session_state.selected_points):
                        st.session_state.selected_points.append(place)
                        if st.session_state.source_id is None:
                            st.session_state.source_id = place["id"]
                        st.session_state.search_results = []
                        st.session_state.clear_search = True
                        st.rerun()
                    else:
                        st.warning("Location already selected!")