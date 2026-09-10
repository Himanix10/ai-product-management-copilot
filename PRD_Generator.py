import streamlit as st
from agents.prd_agent import PRDAgent
from backend.database.db import fetch_initiatives_db, fetch_prds_db


def render_prd_generator():
    st.title("PRD & Acceptance Criteria Generator")
    st.caption("Draft complete Product Requirement Documents with Agile User Stories and Acceptance Criteria using Generative AI")

    initiatives = fetch_initiatives_db()
    opts = initiatives["Title"].tolist() if not initiatives.empty else [
        "Dashboard Performance Optimization",
        "Automated Jira Integration",
        "Bulk Export Features"
    ]

    col1, col2 = st.columns([2, 1])
    with col1:
        selected_init = st.selectbox("Select Target Initiative", opts)
    with col2:
        target_user = st.text_input("Target User Persona", value="Enterprise Product Managers")

    problem = st.text_area(
        "Problem Statement",
        value=f"Customers reported operational friction and request improvements on {selected_init}."
    )
    requirements = st.text_area(
        "Functional Requirements",
        value="Real-time sync, sub-2s analytical query response, and automated error validation."
    )
    acceptance_criteria = st.text_area(
        "Custom Acceptance Criteria (Optional Checklist)",
        value="- [ ] Query response time completes in under 2.0 seconds.\n"
              "- [ ] Data is persisted reliably in the SQLite database.\n"
              "- [ ] User receives clear completion telemetry.\n"
              "- [ ] Automated unit test suite passes with 100% success."
    )

    if st.button("Generate PRD & Acceptance Criteria", type="primary"):
        with st.spinner("Generative AI Agent drafting specifications..."):
            agent = PRDAgent()
            res = agent.execute({
                "feature_name": selected_init,
                "target_user": target_user,
                "problem": problem,
                "requirements": requirements,
                "acceptance_criteria": acceptance_criteria
            })
            st.success("PRD and Acceptance Criteria saved to SQLite database successfully!")
            st.markdown(res["prd_markdown"])

    st.divider()
    st.subheader("Saved PRDs & Acceptance Criteria in Database")
    prds_df = fetch_prds_db()
    if not prds_df.empty:
        st.dataframe(prds_df, use_container_width=True)
    else:
        st.info("No PRD records found in the database.")