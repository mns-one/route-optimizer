def remove_selected_point(st, point_id, idx):
    # pop point from list and empty route, direction state
    st.session_state.selected_points.pop(idx)
    st.session_state.direction_result = []
    st.session_state.route_timeline = []
    
    # if source point is removed, pick first point from list as new source
    if point_id == st.session_state.source_id:
        if st.session_state.selected_points:
            st.session_state.source_id = st.session_state.selected_points[0]["id"]
        else:
            st.session_state.source_id = None

def update_source_id(st, point_id):
    st.session_state.source_id = point_id
