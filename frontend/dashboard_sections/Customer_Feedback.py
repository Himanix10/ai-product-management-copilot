import streamlit as st
import importlib
import backend.database.db as db_module

try:
    from backend.database.db import fetch_customer_feedback_db, insert_customer_feedback_db, get_feedback_categories_db
except ImportError:
    importlib.reload(db_module)
    from backend.database.db import fetch_customer_feedback_db, insert_customer_feedback_db, get_feedback_categories_db
from agents.ingestion_agent import IngestionAgent

def render_customer_feedback():
    st.title("Feedback Explorer")
    st.caption("Filter and inspect raw customer feedback records")
    col_s1, col_s2 = st.columns([3, 1])
    search_query = col_s1.text_input("Search Feedback Text...", placeholder="Filter keywords...")
    categories = ["All"] + get_feedback_categories_db()
    category = col_s2.selectbox("Filter Category", categories)
    voc_data = fetch_customer_feedback_db(category=category, search_query=search_query)
    st.dataframe(voc_data, use_container_width=True)
    with st.expander("➕ Ingest New Feedback Record"):
        with st.form("add_feedback_form"):
            src = st.selectbox("Source Channel", ["Zendesk", "Survey", "CRM", "Email", "GitHub"])
            u_role = st.text_input("User Persona/Role", value="Enterprise Lead")
            f_text = st.text_area("Feedback Narrative")
            cat_tag = st.selectbox("Category Tag", ["Feature Request", "Usability", "Bug", "Integration"])
            if st.form_submit_button("Submit Record to DB"):
                if f_text.strip():
                    ingest_agent = IngestionAgent()
                    res = ingest_agent.execute({"text": f_text, "category": cat_tag, "source": src, "user_type": u_role})
                    insert_customer_feedback_db(src, u_role, res["cleaned_text"], res["classified_category"])
                    st.success(f"Record saved into database! Sentiment Polarity: {res['sentiment_score']}")
                    st.rerun()