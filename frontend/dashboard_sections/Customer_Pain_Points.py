import streamlit as st
import importlib
import backend.database.db as db_module

try:
    from backend.database.db import fetch_pain_points_db, get_pain_point_severities_db
except ImportError:
    importlib.reload(db_module)
    from backend.database.db import fetch_pain_points_db, get_pain_point_severities_db

def render_customer_pain_points():
    st.title("Customer Pain Points")
    st.caption("Identify, categorize, and track recurring customer friction points across feedback channels")
    col_s1, col_s2 = st.columns([3, 1])
    search_query = col_s1.text_input("Filter pain points...", placeholder="Filter pain points keywords...")
    severities = ["All"] + get_pain_point_severities_db()
    severity = col_s2.selectbox("Filter Severity", severities)
    pain_points_data = fetch_pain_points_db(severity=severity, search_query=search_query)
    st.dataframe(pain_points_data, use_container_width=True)