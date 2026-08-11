import streamlit as st
import pandas as pd

def render_customer_pain_points():
    st.title("Customer Pain Points")
    st.caption("Identify, categorize, and track recurring customer friction points across feedback channels")
    
    col_s1, col_s2 = st.columns([3, 1])
    search_query = col_s1.text_input("Search Pain Points...", placeholder="Filter pain point keywords...")
    severity = col_s2.selectbox("Filter Severity", ["All", "High Friction", "Medium Friction", "Low Friction"])

    pain_points_data = pd.DataFrame([
        {"Cluster ID": "PP-101", "Pain Point Area": "Performance & Speed", "Impact Area": "Dashboard & Analytics", "Support Volume": 440, "Severity": "High Friction"},
        {"Cluster ID": "PP-102", "Pain Point Area": "PRD Automation", "Impact Area": "Document Exporting", "Support Volume": 370, "Severity": "High Friction"},
        {"Cluster ID": "PP-103", "Pain Point Area": "UI / UX Friction", "Impact Area": "Navigation Bar", "Support Volume": 320, "Severity": "Medium Friction"},
        {"Cluster ID": "PP-104", "Pain Point Area": "Integrations", "Impact Area": "Jira & Webhooks", "Support Volume": 270, "Severity": "Medium Friction"},
    ])

    if search_query:
        pain_points_data = pain_points_data[
            pain_points_data["Pain Point Area"].str.contains(search_query, case=False) |
            pain_points_data["Impact Area"].str.contains(search_query, case=False)
        ]

    if severity != "All":
        pain_points_data = pain_points_data[pain_points_data["Severity"] == severity]

    st.dataframe(pain_points_data, use_container_width=True)