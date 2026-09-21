import streamlit as st
import pandas as pd
from backend.database.db import fetch_customer_feedback_db, get_feedback_categories_db


def render_feedback_explorer():
    st.title("Feedback Explorer")
    st.caption("Granular search, customer feedback filtering, and thematic deep dives")

    col_s1, col_s2 = st.columns([3, 1])
    search_query = col_s1.text_input("Search feedback keywords...", placeholder="Filter keywords...", key="fe_search")
    categories = ["All"] + get_feedback_categories_db()
    category = col_s2.selectbox("Filter by Category", categories, key="fe_category")

    feedback_df = fetch_customer_feedback_db(category=category, search_query=search_query)

    if not feedback_df.empty:
        col1, col2, col3 = st.columns(3)
        col1.metric("Matching Feedback Records", len(feedback_df))
        if "Sentiment" in feedback_df.columns:
            pos = len(feedback_df[feedback_df["Sentiment"] == "Positive"])
            neg = len(feedback_df[feedback_df["Sentiment"] == "Negative"])
            col2.metric("Positive Sentiment", f"{pos} items")
            col3.metric("Negative Sentiment", f"{neg} items")

        st.divider()
        st.dataframe(feedback_df, use_container_width=True)
    else:
        st.info("No matching customer feedback found.")