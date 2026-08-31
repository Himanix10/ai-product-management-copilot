import streamlit as st
import pandas as pd
from backend.database.db import fetch_product_analytics_db


def render_product_analytics():
    st.title("Product Analytics and User Behavior")
    st.caption("Telemetry, user adoption, session durations, engagement, and product health tracking")

    df_metrics = fetch_product_analytics_db()

    # --- TOP TELEMETRY KPIS ---
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Daily Active Users (DAU)", "2,696", "+8.4% WoW")
    k2.metric("Monthly Active Users (MAU)", "7,985", "+14.2% MoM")
    k3.metric("DAU / MAU Engagement", "33.7%", "Healthy (SaaS Benchmark: >20%)")
    k4.metric("Feature Adoption Rate", "75.8%", "+5.2% vs Target")

    st.divider()

    # --- CHARTS ROW 1 ---
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**User Session Duration & Latency Trends (ms)**")
        session_df = pd.DataFrame({
            "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
            "Avg Session Duration (Mins)": [14.2, 16.5, 18.1, 15.4, 19.8, 11.2, 10.4],
            "P95 Query Latency (ms)": [240, 210, 190, 205, 180, 175, 170]
        }).set_index("Day")
        st.line_chart(session_df)

    with c2:
        st.markdown("**Feature Adoption by Core Module (%)**")
        adoption_df = pd.DataFrame({
            "Product Module": ["PRD Generator", "Roadmap Planner", "RICE Prioritizer", "Feedback Search", "Copilot Chat"],
            "Adoption Rate (%)": [82.5, 68.0, 74.5, 91.0, 88.5]
        }).set_index("Product Module")
        st.bar_chart(adoption_df)

    st.divider()

    # --- METRICS DATABASE TABLE ---
    st.subheader("Database Tracked Product Metrics")
    if not df_metrics.empty:
        st.dataframe(df_metrics, use_container_width=True)
    else:
        sample_metrics = pd.DataFrame([
            {"Metric Name": "Daily Active Users", "Category": "Engagement", "Current Value": "2,696", "Target Value": "2,315", "Unit": "Users", "Health Status": "Healthy"},
            {"Metric Name": "Monthly Active Users", "Category": "Engagement", "Current Value": "7,985", "Target Value": "8,073", "Unit": "Users", "Health Status": "Stable"},
            {"Metric Name": "Feature Adoption Rate", "Category": "Adoption", "Current Value": "75.8%", "Target Value": "76.0%", "Unit": "%", "Health Status": "Healthy"},
            {"Metric Name": "User Churn Rate", "Category": "Retention", "Current Value": "1.8%", "Target Value": "2.5%", "Unit": "%", "Health Status": "Healthy"},
            {"Metric Name": "P95 Query Latency", "Category": "Performance", "Current Value": "180", "Target Value": "250", "Unit": "ms", "Health Status": "Healthy"}
        ])
        st.dataframe(sample_metrics, use_container_width=True)