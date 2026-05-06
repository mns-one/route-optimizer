def display_user_selected_points(st):
    if not st.session_state.selected_points:
        st.session_state.source_id = None
        return

    st.subheader("Selected Points")

    for i, p in enumerate(st.session_state.selected_points):
        col1, col2 = st.columns([4, 1])

        with col1:
            st.write(p["name"], p["full_address"])

        with col2:
            if st.button("Remove", key=f"remove_{i}"):
                removed_id = p["id"]
                st.session_state.selected_points.pop(i)
                st.session_state.direction_result = []
                st.session_state.route_timeline = []

                if removed_id == st.session_state.source_id:
                    if st.session_state.selected_points:
                        st.session_state.source_id = st.session_state.selected_points[0]["id"]
                    else:
                        st.session_state.source_id = None

                st.rerun()

    source_options = {}
    for p in st.session_state.selected_points:
        label = f"{p['name']} - {p['full_address'] or ''}"
        source_options[label] = p["id"]

    source_ids = [p["id"] for p in st.session_state.selected_points]
    if st.session_state.source_id not in source_ids:
        st.session_state.source_id = source_ids[0]

    selected_source_index = source_ids.index(st.session_state.source_id)
    selected_source_label = st.radio(
        "Select Start point",
        options=list(source_options.keys()),
        index=selected_source_index,
        key="source_selector_radio",
    )
    st.session_state.source_id = source_options[selected_source_label]
    
