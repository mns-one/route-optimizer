def format_duration(seconds):
        if seconds is None:
            return None

        total_seconds = int(seconds)
        minutes, sec = divmod(total_seconds, 60)
        hours, minutes = divmod(minutes, 60)

        if hours > 0:
            return f"{hours}h {minutes}m {sec}s"
        if minutes > 0:
            return f"{minutes}m {sec}s"
        return f"{sec}s"

def display_route_timeline(st):
    # use directions data to build info card for each stop
    if not st.session_state.route_timeline:
        return
    
    st.subheader("Fastest Route")

    for stop in st.session_state.route_timeline:
        node = stop.get("node", {})
        stop_number = stop.get("stop_number", "-")
        name = node.get("name", "Unknown stop")
        address = node.get("address")

        with st.container(border=True):
            col1, col2 = st.columns([1, 10])

            with col1:
                st.markdown(f"**#{stop_number}**")

            with col2:
                st.markdown(f"**{name}**")
                if address:
                    st.caption(address)

            next_duration = format_duration(stop.get("next_duration_sec"))
            if next_duration is not None:
                st.caption(f"Travel to next stop: {next_duration}")
