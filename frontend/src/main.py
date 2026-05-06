import streamlit as st

from state.session_state import load_session_state
from components.main_ui import render_ui


load_session_state(st)

render_ui(st)

