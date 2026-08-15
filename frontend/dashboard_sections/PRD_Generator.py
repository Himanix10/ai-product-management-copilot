import streamlit as st
from agents.prd_agent import PRDAgent
from backend.database.db import fetch_initiatives_db

def render_prd_generator():
    st.title("PRD GENERATOR")
    st.caption("Automatically draft Product Requirement Documents using Gemini AI Agents")
    
    initiatives = fetch_initiatives_db()
    opts = initiatives["Title"].tolist() if not initiatives.empty else ["Dashboard Performance Optimization", "Automated Jira Integration", "Bulk Export Features"]
    selected_init = st.selectbox("Select Prioritized Initiative", opts)
    target_user = st.text_input("Target Persona", value="Enterprise Users")
    problem = st.text_area("Problem Statement", value=f"Customers reported friction on {selected_init}.")
    requirements = st.text_area("Requirements", value="Real-time sync, sub-2s query response, automated unit test coverage.")

    if st.button("Generate PRD with Gemini Agent", type="primary"):
        agent = PRDAgent()
        res = agent.execute({
            "feature_name": selected_init,
            "target_user": target_user,
            "problem": problem,
            "requirements": requirements
        })
        st.markdown(res["prd_markdown"])
        st.success("PRD saved to SQLite database successfully!")