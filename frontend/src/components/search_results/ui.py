from .state import remove_selected_point, update_source_id

def display_user_selection_menu(st):
    if not st.session_state.selected_points:
        update_source_id(st, None)  # update None to avoid NULL state
        return
    
    # render all user selected points in a list
    st.subheader("Selected Points")

    for i, p in enumerate(st.session_state.selected_points):
        col1, col2 = st.columns([4, 1])

        with col1:
            st.write(p["name"], p["full_address"])

        with col2:
            if st.button("Remove", key=f"remove_{i}"):  # button to remove a selected point
                removed_id = p["id"]
                remove_selected_point(st, removed_id, i)
                st.rerun()
    
    # render radio list for source selection
    source_options = {}
    for p in st.session_state.selected_points:
        label = f"{p['name']} - {p['full_address'] or ''}"
        source_options[label] = p["id"]

    source_ids = [p["id"] for p in st.session_state.selected_points]
    if st.session_state.source_id not in source_ids:
        update_source_id(st, source_ids[0])

    selected_source_index = source_ids.index(st.session_state.source_id)
    selected_source_label = st.radio(
        "Select Start point",
        options=list(source_options.keys()),
        index=selected_source_index,
        key="source_selector_radio",
    )
    update_source_id(st, source_options[selected_source_label])