from utils.error_handler import handle_request_error
from components.search.state import run_search, add_place

def display_search_area(st):
    # render the search input form ui
    st.title("Search & Add Multi-points")

    query = st.text_input("Enter area", key="search_input")

    if st.button("Search") and query:
        try:
            run_search(st.session_state, query)
        except Exception as exc:
            handle_request_error(exc)

def display_search_results(st):
    # render the list of places fromm api response
    results = st.session_state.get("search_results", [])

    if not results:
        return

    st.subheader("Search Results")

    for idx, place in enumerate(results):
        label = f"{place['name']} - {place['full_address'] or ''}"
        col1, col2 = st.columns([4, 1])

        with col1:
            st.write(label)

        with col2:
            if st.button("Add", key=f"add_{idx}"):
                success, message = add_place(st.session_state, place)
                if success:
                    st.rerun()
                else:
                    st.warning(message)
