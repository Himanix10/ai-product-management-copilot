import streamlit as st
import pandas as pd

def render_feedback_explorer():
    st.title("Customer Feedback")
    st.caption("Filter and inspect raw customer feedback records")
    
    col_s1, col_s2 = st.columns([3, 1])
    search_query = col_s1.text_input("Search Feedback...", placeholder="Filter keywords...")
    category = col_s2.selectbox("Category", ["All", "Feature Request", "Usability", "Bug", "Integration"])

    voc_data = pd.DataFrame([
        {"ID": 101, "Source": "Zendesk", "User": "Enterprise Lead", "Feedback": "Need faster PRD exports and bulk actions", "Category": "Feature Request"},
        {"ID": 102, "Source": "Survey", "User": "Product Mgr", "Feedback": "UI navigation is crisp and modern", "Category": "Usability"},
        {"ID": 103, "Source": "CRM", "User": "Tech Lead", "Feedback": "Add REST API webhooks for Jira synchronization", "Category": "Integration"},
        {"ID": 104, "Source": "Email", "User": "SaaS Founder", "Feedback": "Dashboard queries experience latency delays", "Category": "Bug"},
    ])

    if search_query:
        voc_data = voc_data[voc_data["Feedback"].str.contains(search_query, case=False)]

    if category != "All":
        voc_data = voc_data[voc_data["Category"] == category]

    st.dataframe(voc_data, use_container_width=True)