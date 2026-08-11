import streamlit as st
import pandas as pd

def render_dashboard_overview():
    st.title("Dashboard Overview")
    st.caption("Executive view of real-time product health metrics and telemetry")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("VOC Feedback Volume", "1,420", "+12%")
    m2.metric("Active Pain Points", "4 Clusters", "-1")
    m3.metric("Scored Initiatives", "3 Items", "RICE")
    m4.metric("Approved PRDs", "1 Draft", "Q3 2026")

    st.divider()
    st.subheader("Telemetry Insights")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("**Customer Feedback Sources**")
        st.bar_chart(pd.DataFrame({"Source": ["Zendesk", "Surveys", "CRM", "Email"], "Volume": [450, 320, 280, 370]}).set_index("Source"))
    with col_b:
        st.markdown("**Pain Point Severity Distribution**")
        st.bar_chart(pd.DataFrame({"Area": ["Performance", "PRD Export", "UI/UX", "Jira Sync"], "Tickets": [440, 370, 320, 270]}).set_index("Area"))
