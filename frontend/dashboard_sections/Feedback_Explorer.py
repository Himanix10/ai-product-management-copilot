import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API = "http://127.0.0.1:8000"
st.title("Feedback Explorer")
st.caption("Ingestion → Theme Extraction → Clustering → Reporting")

uploaded = st.file_uploader("Upload feedback CSV or Excel", type=["csv", "xlsx", "xls"])
if uploaded and st.button("Analyze Feedback", type="primary"):
    try:
        with st.spinner("Running feedback agents..."):
            r = requests.post(
                API + "/api/agents/ingest-csv",
                files={"file": (uploaded.name, uploaded.getvalue(), uploaded.type)},
                timeout=60,
            )
            r.raise_for_status()
            st.session_state.feedback_result = r.json()
    except Exception as e:
        st.error(f"Backend connection or analysis failed: {e}")

res = st.session_state.get("feedback_result")
if res:
    st.success(f"Processed {res['record_count']:,} records from {res['filename']}.")
    st.subheader("AI Executive Summary")
    st.info(res["report"]["executive_summary"])
    left, right = st.columns(2)
    themes = pd.DataFrame(res["themes"])
    clusters = pd.DataFrame(res["clusters"])
    if not themes.empty:
        left.plotly_chart(px.bar(themes, x="theme", y="count", title="Detected Themes"), use_container_width=True)
    if not clusters.empty:
        right.plotly_chart(px.pie(clusters, names="cluster", values="mentions", title="Theme Clusters"), use_container_width=True)
    st.subheader("Data Preview")
    st.dataframe(pd.DataFrame(res["preview"]), use_container_width=True, hide_index=True)
else:
    st.info("Upload a CSV or Excel feedback file to begin.")
