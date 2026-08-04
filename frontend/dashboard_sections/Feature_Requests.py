import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API = "http://127.0.0.1:8000"
st.title("Feature Requests")
st.caption("RICE-based feature prioritization.")

with st.form("feature"):
    name = st.text_input("Feature Name")
    description = st.text_area("Problem / Feature Description")
    left, middle, right, extra = st.columns(4)
    reach = left.number_input("Reach", 0.0, 1000000.0, 5000.0, 100.0)
    impact = middle.number_input("Impact", 0.0, 10.0, 2.5, 0.1)
    confidence = right.number_input("Confidence", 0.0, 1.0, 0.8, 0.05)
    effort = extra.number_input("Effort", 0.1, 100.0, 2.0, 0.5)
    submit = st.form_submit_button("Calculate RICE & Prioritize", type="primary")

if submit:
    if not name.strip():
        st.error("Feature name is required.")
    else:
        try:
            r = requests.post(
                API + "/api/agents/prioritize",
                json={
                    "name": name,
                    "description": description,
                    "reach": reach,
                    "impact": impact,
                    "confidence": confidence,
                    "effort": effort,
                },
                timeout=20,
            )
            r.raise_for_status()
            st.session_state.last_priority = r.json()
        except Exception as e:
            st.error(f"Backend error: {e}")

if "last_priority" in st.session_state:
    q = st.session_state.last_priority
    st.success(f"Priority: {q['priority']} | RICE Score: {q['rice_score']}")
    st.write(q["recommendation"])

try:
    rows = requests.get(API + "/api/features", timeout=5).json()
except Exception:
    rows = []

if rows:
    df = pd.DataFrame(rows)
    st.plotly_chart(
        px.scatter(df, x="effort", y="reach", size="rice_score", color="priority", hover_name="name", title="Reach vs Effort"),
        use_container_width=True,
    )
    st.dataframe(
        df[["name", "reach", "impact", "confidence", "effort", "rice_score", "priority", "status"]],
        use_container_width=True,
        hide_index=True,
    )
