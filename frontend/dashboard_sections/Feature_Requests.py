import streamlit as st
import pandas as pd
from agents.feature_request_agent import FeatureRequestAgent
from agents.prioritization_agent import PrioritizationAgent
from backend.database.db import fetch_initiatives_db


def render_feature_requests():
    st.title("Feature Requests")
    st.caption("Analyze feature request demand velocity and calculate priority metrics")

    with st.container(border=True):
        st.subheader("Feature Demand & Feasibility Evaluator")
        req_text = st.text_input("Enter Feature Request Description", value="Add automated CSV export and Jira REST webhook sync")

        if st.button("Evaluate Demand Level", type="secondary"):
            fr_agent = FeatureRequestAgent()
            res = fr_agent.execute({"request": req_text})
            st.info(f"Demand Velocity: **{res.get('demand_level', 'Medium Demand')}** | Status: **{res.get('status', 'Analyzed')}**")

    st.divider()

    with st.form("feature_request_scoring_form"):
        st.subheader("Submit Scored Feature Request to Initiatives")
        name = st.text_input("Feature Name", value="Automated CSV/Excel Bulk Importer")
        desc = st.text_area("Problem / Description", value="Support managers require bulk review uploads directly into SQLite.")

        col1, col2, col3, col4 = st.columns(4)
        reach = col1.number_input("Reach (Users/Qtr)", value=4000.0, step=500.0)
        impact = col2.slider("Impact (0.5 to 3.0)", 0.5, 3.0, 2.5, step=0.5)
        confidence = col3.slider("Confidence (0.5 to 1.0)", 0.5, 1.0, 0.8, step=0.1)
        effort = col4.number_input("Effort (Person-Months)", value=1.5, min_value=0.5, step=0.5)

        if st.form_submit_button("Calculate RICE & Save to Initiatives", type="primary"):
            p_agent = PrioritizationAgent()
            res = p_agent.execute({"title": name, "reach": reach, "impact": impact, "confidence": confidence, "effort": effort})
            st.success(f"Initiative **{name}** added with RICE Score: **{res['score']}**")
            st.rerun()

    st.divider()
    st.subheader("Current Feature Initiatives")
    initiatives = fetch_initiatives_db()
    st.dataframe(initiatives, use_container_width=True)