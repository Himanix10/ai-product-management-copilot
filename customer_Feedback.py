import streamlit as st
from backend.main import get_feedback_service, add_feedback_service

def render_customer_feedback():
    st.title("Customer Feedback")
    st.caption("Filter and inspect raw customer feedback records directly from backend SQLite DB")

    col_s1, col_s2 = st.columns([3, 1])
    search_query = col_s1.text_input("Search Feedback...", placeholder="Filter keywords...")
    category = col_s2.selectbox("Category", ["All", "Feature Request", "Usability", "Bug", "Integration"])

    # Query directly from Backend database
    voc_data = get_feedback_service(category=category, search=search_query)
    st.dataframe(voc_data, use_container_width=True)

    with st.expander("➕ Ingest New Feedback Record"):
        with st.form("add_feedback_form"):
            src = st.selectbox("Source Channel", ["Zendesk", "Survey", "CRM", "Email"])
            u_role = st.text_input("User Persona/Role", value="Enterprise Lead")
            f_text = st.text_area("Feedback Narrative")
            cat_tag = st.selectbox("Category Tag", ["Feature Request", "Usability", "Bug", "Integration"])
            
            if st.form_submit_button("Submit Record to DB"):
                if f_text.strip():
                    add_feedback_service(src, u_role, f_text, cat_tag)
                    st.success("Record saved into backend database successfully!")
                    st.rerun()
