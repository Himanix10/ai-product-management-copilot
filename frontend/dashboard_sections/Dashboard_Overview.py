import streamlit as st

from agents.analytics_agent import AnalyticsAgent
from backend.database.db import (
    get_feedback_monthly_counts,
    get_pain_point_summary,
)


def render_dashboard_overview():

    st.title("Dashboard Overview")

    st.caption(
        "Real-time product metrics, customer feedback, "
        "pain points, initiatives and roadmap telemetry"
    )

    # ---------------------------------------------------------
    # DATABASE KPIs
    # ---------------------------------------------------------

    agent = AnalyticsAgent()
    metrics = agent.execute({})

    m1, m2, m3, m4, m5 = st.columns(5)

    m1.metric(
        "VOC FEEDBACK",
        f"{metrics['feedback_count']:,}",
    )

    m2.metric(
        "PAIN POINTS",
        f"{metrics['active_pain_points']:,}",
    )

    m3.metric(
        "INITIATIVES",
        f"{metrics['scored_initiatives']:,}",
    )

    m4.metric(
        "PRDs",
        f"{metrics['approved_prds']:,}",
    )

    m5.metric(
        "ROADMAP ACTIVE",
        f"{metrics['active_roadmap_items']:,}",
    )

    st.divider()

    # ---------------------------------------------------------
    # FEEDBACK TREND FROM DATABASE
    # ---------------------------------------------------------

    col_a, col_b = st.columns(2)

    with col_a:

        st.subheader(
            "Customer Feedback Volume Trend"
        )

        chart_data = get_feedback_monthly_counts()

        if chart_data.empty:

            st.info(
                "No timestamped feedback data available."
            )

        else:

            chart_data = chart_data.set_index(
                "Month"
            )

            st.line_chart(
                chart_data[
                    ["Feedback Volume"]
                ]
            )

    # ---------------------------------------------------------
    # PAIN POINT SUMMARY FROM DATABASE
    # ---------------------------------------------------------

    with col_b:

        st.subheader(
            "Customer Pain Points Summary"
        )

        pain_data = get_pain_point_summary()

        if pain_data.empty:

            st.info(
                "No pain-point data available."
            )

        else:

            pain_data = pain_data.set_index(
                "Pain Area"
            )

            st.bar_chart(
                pain_data[
                    ["Support Volume"]
                ]
            )

    # ---------------------------------------------------------
    # DATABASE STATUS
    # ---------------------------------------------------------

    st.divider()

    st.caption(
        "All dashboard KPIs and charts are loaded from SQLite "
        "database records."
    )