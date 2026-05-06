import requests
import streamlit as st

def handle_request_error(exc: Exception) -> None:
    if isinstance(exc, (requests.ConnectionError, requests.Timeout)):
        st.error("Server unreachable at the moment, try again later")
    elif isinstance(exc, requests.HTTPError):
        st.error("Server returned an error. Please try again later")
    elif isinstance(exc, requests.RequestException):
        st.error("Request failed. Please try again later")
    else:
        st.error("Unexpected error occurred. Please try again later")
