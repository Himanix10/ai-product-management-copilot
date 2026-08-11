import streamlit as st
import pandas as pd

def render_roadmap():
    st.title("Roadmap Planner")
    st.caption("Quarterly release timeline and tracking")

    roadmap_df = pd.DataFrame([
        {"Quarter": "Q1 2026", "Initiative": "UI Redesign & Modern Sidebar", "Status": "Completed"},
        {"Quarter": "Q2 2026", "Initiative": "RICE Priority Calculator Engine", "Status": "In Progress"},
        {"Quarter": "Q3 2026", "Initiative": "Jira Webhooks & PRD Exporter", "Status": "Planned"},
        {"Quarter": "Q4 2026", "Initiative": "AI Telemetry Predictions", "Status": "Under Review"}
    ])
    st.dataframe(roadmap_df, use_container_width=True)
