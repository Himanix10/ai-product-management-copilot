import requests
import streamlit as st

DEFAULT_API_URL = "http://127.0.0.1:8000"


def get_api_url() -> str:
    return st.secrets.get("api_url", DEFAULT_API_URL)


def api_get(path: str, timeout: int = 20, **kwargs):
    url = f"{get_api_url()}{path}"
    return requests.get(url, timeout=timeout, **kwargs)


def api_post(path: str, json=None, timeout: int = 20, **kwargs):
    url = f"{get_api_url()}{path}"
    return requests.post(url, json=json, timeout=timeout, **kwargs)
