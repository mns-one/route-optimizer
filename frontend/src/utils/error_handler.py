import requests
import streamlit as st

def handle_request_error(exc: Exception) -> None:
    
    if isinstance(exc, (requests.ConnectionError, requests.Timeout)):
        st.error("Server unreachable at the moment, try again later")

    elif isinstance(exc, requests.HTTPError):
        status_code = exc.response.status_code if exc.response is not None else None
        if status_code == 429:
            retry_after = exc.response.headers.get("Retry-After") if exc.response is not None else None
            if retry_after:
                st.error(f"Rate limit exceeded. Please try again after {retry_after} seconds.")
            else:
                st.error("Rate limit exceeded. Please try again later.")
        else:
            st.error("Server returned an error. Please try again later")

    elif isinstance(exc, requests.RequestException):
        st.error("Request failed. Please try again later")
    else:
        st.error("Unexpected error occurred. Please try again later")
