from utils.error_handler import handle_request_error
from api.app_feature_api import get_optimal_route

def find_route(st):
    can_optimize = ""
    if len(st.session_state.selected_points) > 0:
        can_optimize = len(st.session_state.selected_points) >= 3 and st.session_state.source_id is not None

    if not can_optimize:
        st.info("Add at least 3 points and choose a source to optimize route.")

    if st.button("Get Fastest Route", disabled=not can_optimize):
        try:
            route_data = get_optimal_route(st.session_state.selected_points, st.session_state.source_id)
            st.session_state.direction_result = route_data.get("direction")
            st.session_state.route_timeline = route_data.get("timeline")
            st.rerun()
            
        except Exception as exc:
            handle_request_error(exc)