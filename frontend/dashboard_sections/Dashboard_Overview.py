import streamlit as st
import pandas as pd
import plotly.express as px

def render_dashboard_overview():
    st.title("Dashboard")
    st.caption("Real-time product metrics, customer feedback, and initiative telemetry")
    
    # Specific KPI terminology replacing vague labels
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("VOC FEEDBACK VOL", "1,420", delta="+12%")
    m2.metric("CUSTOMER PAIN POINTS", "4 Active", delta="Clusters")
    m3.metric("PRIORITIZED INITIATIVES", "3", delta="Scored")
    m4.metric("PRD SPECIFICATIONS", "1 Approved", delta="Draft")
    m5.metric("ROADMAP SCHEDULE", "Q3 2026", delta="Active")
    
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Customer Feedback Volume Trend")
        df_trend = pd.DataFrame({
            "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"],
            "Feedback Volume": [450, 620, 810, 980, 1150, 1300, 1420]
        })
        fig_line = px.line(df_trend, x="Month", y="Feedback Volume", markers=True, color_discrete_sequence=["#6366F1"])
        fig_line.update_layout(template="plotly_white", height=320)
        st.plotly_chart(fig_line, use_container_width=True)

    with col2:
        st.subheader("Customer Pain Points Summary")
        df_pain = pd.DataFrame({
            "Pain Point Area": ["Performance & Speed", "PRD Automation", "UI / UX Friction", "Integrations"],
            "Support Volume": [440, 370, 320, 270]
        })
        fig_bar = px.bar(df_pain, x="Support Volume", y="Pain Point Area", orientation="h", color="Support Volume", color_continuous_scale="Purples")
        fig_bar.update_layout(template="plotly_white", height=320, showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)