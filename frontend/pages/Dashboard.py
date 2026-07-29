import streamlit as st
import plotly.express as px

from utils.styling import render_card


def render(feedback, features):
    st.markdown("<div class='section-heading'>Dashboard</div>", unsafe_allow_html=True)
    st.markdown(
        "<p class='section-subtitle'>Use this workspace to review product health, feature momentum, and strategic direction.</p>",
        unsafe_allow_html=True,
    )

    render_card("Key Metrics", lambda: _render_metrics(feedback, features))

    fig = px.bar(
        features,
        x="Feature",
        y="RICE",
        color="Priority",
        title="Feature prioritization by RICE score",
        color_discrete_map={"P0": "#6366f1", "P1": "#a855f7", "P2": "#38bdf8"},
    )
    fig.update_layout(
        plot_bgcolor="rgba(15, 23, 42, 0.92)",
        paper_bgcolor="rgba(15, 23, 42, 0.92)",
        font_color="#e2e8f0",
    )

    render_card("Priority Scoreboard", lambda: st.plotly_chart(fig, use_container_width=True))
    render_card("Top Insights", lambda: st.write("Dashboard performance, authentication, and export workflows are the highest-impact areas right now."))


def _render_metrics(feedback, features):
    col1, col2, col3 = st.columns(3)
    col1.metric("Feedback Items", len(feedback), "Total items")
    col2.metric("High Priority", len(features[features["Priority"] == "P0"]), "P0 features")
    col3.metric("Average RICE", round(features["RICE"].mean(), 2), "score")
