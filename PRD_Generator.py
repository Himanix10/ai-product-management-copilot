import streamlit as st

def render_prd_generator():
    st.title("PRD Generator")
    st.caption("Draft structured Product Requirement Documents")

    with st.form("prd_form"):
        feature_name = st.text_input("Feature Name", value="Automated Jira Integration")
        target_user = st.text_input("Target Persona", value="Technical Product Managers")
        problem_statement = st.text_area("Problem Statement", value="Manual sync creates operational overhead.")
        requirements = st.text_area("Functional Requirements", value="- Real-time webhooks\n- Custom mapping for severity")

        if st.form_submit_button("Generate PRD Draft", type="primary"):
            st.subheader(f"PRD: {feature_name}")
            st.markdown(f"**Target Persona:** {target_user}")
            st.markdown(f"### Problem Statement\n{problem_statement}")
            st.markdown(f"### Key Requirements\n{requirements}")
