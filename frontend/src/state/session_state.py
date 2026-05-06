def load_session_state(st):
    if "selected_points" not in st.session_state:
     st.session_state.selected_points = []

    if "direction_result" not in st.session_state:
        st.session_state.direction_result = []

    if "route_timeline" not in st.session_state:
        st.session_state.route_timeline = []   

    if "search_results" not in st.session_state:
        st.session_state.search_results = []

    if "search_input" not in st.session_state:
        st.session_state.search_input = ""

    if "clear_search" not in st.session_state:
        st.session_state.clear_search = False

    if "source_id" not in st.session_state:
        st.session_state.source_id = None

    if st.session_state.get("clear_search"):
        st.session_state.search_input = ""
        st.session_state.clear_search = False

