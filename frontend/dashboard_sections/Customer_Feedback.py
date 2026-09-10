import streamlit as st
import pandas as pd
from backend.database.db import (
    fetch_customer_feedback_db,
    get_feedback_categories_db,
)


def render_customer_feedback():
    st.title("Feedback Explorer")
    st.caption("Filter and inspect raw customer feedback records")

    # Search & Category Filters
    col_s1, col_s2 = st.columns([3, 1])
    search_query = col_s1.text_input(
        "Search Feedback Text...",
        placeholder="Filter keywords...",
        key="feedback_search_input",
    )
    categories = ["All"] + get_feedback_categories_db()
    category = col_s2.selectbox(
        "Filter Category",
        categories,
        key="feedback_category_select",
    )

    # Fetch Ingested Records
    voc_data = fetch_customer_feedback_db(category=category, search_query=search_query)

    if not voc_data.empty:
        # High-level Ingestion Telemetry
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Records", len(voc_data))

        if "Sentiment" in voc_data.columns:
            pos_count = len(voc_data[voc_data["Sentiment"].astype(str).str.lower() == "positive"])
            neg_count = len(voc_data[voc_data["Sentiment"].astype(str).str.lower() == "negative"])
            neu_count = len(voc_data[voc_data["Sentiment"].astype(str).str.lower() == "neutral"])
            m2.metric("Positive Sentiment", pos_count)
            m3.metric("Negative Sentiment", neg_count)
            m4.metric("Neutral Sentiment", neu_count)

        st.divider()

        # Display Ingested Feedback Data Table
        st.dataframe(voc_data, use_container_width=True)
    else:
        st.info("No customer feedback records found matching your filter criteria.")