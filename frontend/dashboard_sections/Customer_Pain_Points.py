import streamlit as st
from backend.database.db import fetch_pain_points_db

def render_customer_pain_points():
    st.title("Customer Pain Points")
    st.caption("Identify, categorize, and track recurring customer friction points across feedback channels")
    col_s1, col_s2 = st.columns([3, 1])
    search_query = col_s1.text_input("Filter pain points...", placeholder="Filter pain points keywords...")
    severity = col_s2.selectbox("Filter Severity", ["All", "High Friction", "Medium Friction", "Low Friction"])
    pain_points_data = fetch_pain_points_db(severity=severity, search_query=search_query)
    st.dataframe(pain_points_data, use_container_width=True)