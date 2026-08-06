import streamlit as st

from api_client import api_post

st.title("AI PRD Generator")
st.caption("Convert a validated product problem into a structured Product Requirements Document.")

with st.form("prd_form"):
    feature = st.text_input("Feature Name")
    problem = st.text_area("Problem Statement")
    users = st.text_input("Target Users", "Existing product users")
    goals = st.text_area("Goals")
    metrics = st.text_area("Success Metrics")
    stories = st.text_area("User Stories")
    acceptance = st.text_area("Acceptance Criteria")
    dependencies = st.text_area("Dependencies")
    risks = st.text_area("Risks")
    generate = st.form_submit_button("Generate PRD", type="primary")

if generate:
    if not feature.strip() or not problem.strip():
        st.error("Feature Name and Problem Statement are required.")
    else:
        try:
            r = api_post(
                "/api/agents/generate-prd",
                json={
                    "feature_name": feature,
                    "problem_statement": problem,
                    "target_users": users,
                    "goals": goals,
                    "success_metrics": metrics,
                    "user_stories": stories,
                    "acceptance_criteria": acceptance,
                    "dependencies": dependencies,
                    "risks": risks,
                },
                timeout=30,
            )
            r.raise_for_status()
            st.session_state.prd_result = r.json()
        except Exception as e:
            st.error(f"Backend error: {e}")

if "prd_result" in st.session_state:
    p = st.session_state.prd_result
    st.markdown(p["content"])
    st.download_button(
        "Download Markdown",
        p["content"],
        file_name=f"{p['title'].replace(' ', '_')}.md",
        mime="text/markdown",
    )
