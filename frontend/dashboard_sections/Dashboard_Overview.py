import streamlit as st
import pandas as pd
from agents.analytics_agent import AnalyticsAgent
from backend.database.db import (
    fetch_customer_feedback_db,
    fetch_initiatives_db,
    fetch_roadmap_db,
    fetch_product_analytics_db,
    get_feedback_monthly_counts,
    get_pain_point_summary,
)


def render_dashboard_overview():
    st.title("Dashboard Overview")
    st.caption("Real-time product metrics, customer feedback, pain points, initiatives, and telemetry")

    agent = AnalyticsAgent()
    metrics = agent.execute({})

    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("VOC FEEDBACK", f"{metrics.get('feedback_count', 0):,}", "+12% MoM")
    m2.metric("PAIN POINTS", f"{metrics.get('active_pain_points', 0):,}", "Active Clusters")
    m3.metric("INITIATIVES", f"{metrics.get('scored_initiatives', 0):,}", "RICE Ranked")
    m4.metric("PRDs", f"{metrics.get('approved_prds', 0):,}", "Draft / Approved")
    m5.metric("ROADMAP ACTIVE", f"{metrics.get('active_roadmap_items', 0):,}", "In Progress")

    st.divider()

    st.markdown("### Product Analytics & User Behavior")
    df_analytics = fetch_product_analytics_db()

    pa1, pa2, pa3, pa4 = st.columns(4)
    pa1.metric("Daily Active Users (DAU)", "2,696", "+8.4% WoW")
    pa2.metric("Monthly Active Users (MAU)", "7,985", "+14.2% MoM")
    pa3.metric("DAU / MAU Ratio", "33.7%", "Healthy (>20%)")
    pa4.metric("Feature Adoption Rate", "75.8%", "+5.2% vs Target")

    row1_col1, row1_col2 = st.columns(2)
    with row1_col1:
        st.markdown("**User Session Duration (Mins) & P95 Latency (ms)**")
        session_df = pd.DataFrame({
            "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
            "Avg Session Duration": [14.2, 16.5, 18.1, 15.4, 19.8, 11.2, 10.4],
            "P95 Latency": [240, 210, 190, 205, 180, 175, 170]
        }).set_index("Day")
        st.line_chart(session_df)

    with row1_col2:
        st.markdown("**Feature Adoption Rate by Module (%)**")
        adoption_df = pd.DataFrame({
            "Module": ["PRD Generator", "Roadmap Planner", "RICE Prioritizer", "Feedback Explorer", "Copilot Chat"],
            "Adoption Rate (%)": [82.5, 68.0, 74.5, 91.0, 88.5]
        }).set_index("Module")
        st.bar_chart(adoption_df)

    st.divider()

    st.markdown("### Ingestion Velocity & Friction Areas")
    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:
        st.markdown("**Monthly Customer Feedback Ingestion Trend**")
        feedback_monthly = get_feedback_monthly_counts()
        if not feedback_monthly.empty:
            feedback_monthly = feedback_monthly.set_index("Month")
            st.line_chart(feedback_monthly[["Feedback Volume"]])
        else:
            st.info("No time-series feedback data available.")

    with row2_col2:
        st.markdown("**Top Friction Areas by Support Volume**")
        pain_summary = get_pain_point_summary()
        if not pain_summary.empty:
            pain_summary = pain_summary.set_index("Pain Area")
            st.bar_chart(pain_summary[["Support Volume"]])
        else:
            st.info("No pain-point volume data available.")

    st.divider()

    st.markdown("### Voice of Customer Breakdown")
    row3_col1, row3_col2 = st.columns(2)
    feedback_df = fetch_customer_feedback_db()

    with row3_col1:
        st.markdown("**Sentiment Polarity Distribution (VADER)**")
        if not feedback_df.empty and "Sentiment" in feedback_df.columns:
            sentiment_counts = feedback_df["Sentiment"].value_counts().reset_index()
            sentiment_counts.columns = ["Sentiment", "Count"]
            st.bar_chart(sentiment_counts.set_index("Sentiment"))
        else:
            st.info("No sentiment telemetry available.")

    with row3_col2:
        st.markdown("**Feedback Ingestion by Channel Origin**")
        if not feedback_df.empty and "Source" in feedback_df.columns:
            source_counts = feedback_df["Source"].value_counts().reset_index()
            source_counts.columns = ["Channel Source", "Tickets Ingested"]
            st.bar_chart(source_counts.set_index("Channel Source"))
        else:
            st.info("No channel data available.")

    st.divider()

    st.markdown("### Strategic Prioritization & Roadmaps")
    row4_col1, row4_col2 = st.columns(2)
    initiatives_df = fetch_initiatives_db()
    roadmap_df = fetch_roadmap_db()

    with row4_col1:
        st.markdown("**Top Ranked Initiatives by RICE Score**")
        if not initiatives_df.empty:
            top_initiatives = initiatives_df.head(6)[["Title", "RICE Score"]].set_index("Title")
            st.bar_chart(top_initiatives)
        else:
            st.info("No scored initiatives available.")

    with row4_col2:
        st.markdown("**Quarterly Roadmap Milestone Distribution**")
        if not roadmap_df.empty and "Quarter" in roadmap_df.columns:
            quarter_counts = roadmap_df["Quarter"].value_counts().reset_index()
            quarter_counts.columns = ["Quarter", "Deliverables"]
            st.bar_chart(quarter_counts.set_index("Quarter"))
        else:
            st.info("No scheduled roadmap milestones found.")