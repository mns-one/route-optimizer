import streamlit as st
import requests
import os
from dotenv import load_dotenv
from map_render import render_selected_points

load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL")
if not BACKEND_URL:
    raise ValueError("BACKEND_URL environment variable not set")

if "selected_points" not in st.session_state:
    st.session_state.selected_points = []

if "search_results" not in st.session_state:
    st.session_state.search_results = []

if "search_input" not in st.session_state:
    st.session_state.search_input = "" 

if "clear_search" not in st.session_state:
    st.session_state.clear_search = False

# state to clear search box after user selection
if st.session_state.get("clear_search"):
    st.session_state.search_input = ""
    st.session_state.clear_search = False



######  Map Render ###### 
render_selected_points(st.session_state.selected_points)


######  Location Search  ###### 
st.title("Search & Add Multi-points")

query = st.text_input("Enter area", key="search_input")

if st.button("Search") and query:
    try:
        response = requests.get(BACKEND_URL, params={"place_name": query}, timeout=5)
        response.raise_for_status()

        st.session_state.search_results = response.json()

    except Exception as e:
        st.error(f"Request failed: {e}")


###### Search results selection ###### 
def is_duplicate(new_place):
    return any(p["id"] == new_place["id"]
               for p in st.session_state.selected_points)

results = st.session_state.get("search_results", [])

if results:
    st.subheader("Search Results")

    for idx, place in enumerate(results):
        label = f"{place['name']} — {place['full_address'] or ''}"

        col1, col2 = st.columns([4, 1])

        with col1:
            st.write(label)

        with col2:
            if st.button("Add", key=f"add_{idx}"):
                if not is_duplicate(place):
                    st.session_state.selected_points.append(place)
                    st.session_state.search_results = []
                    st.session_state.clear_search = True
                    st.rerun()
                else:
                    st.warning("Location already selected!")    


######  Display User Selected points ###### 
if st.session_state.selected_points:
    st.subheader("Selected Points")

    for i, p in enumerate(st.session_state.selected_points):
        col1, col2 = st.columns([4, 1])

        with col1:
            st.write(p["name"], p["full_address"])

        with col2:
            if st.button("Remove", key=f"remove_{i}"):
                st.session_state.selected_points.pop(i)
                st.rerun()


###### Get Optimized Route ######
if len(st.session_state.selected_points) > 0:
    if st.button("Get Optimized Route"):
        st.write(st.session_state.selected_points)