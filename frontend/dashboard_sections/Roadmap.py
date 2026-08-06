import streamlit as st
import pandas as pd
import plotly.express as px

from api_client import api_post

st.title("Product Roadmap")
st.caption("Plan initiatives across quarters using AI recommendations.")

with st.form("roadmap"):
    feature = st.text_input("Feature / Initiative")
    priority = st.selectbox("Priority", ["High", "Medium", "Low"])
    status = st.selectbox("Status", ["Backlog", "Planned", "In Progress", "Testing", "Released"])
    owner = st.text_input("Owner", "Product Team")
    quarter = st.selectbox("Quarter", ["Q3 2026", "Q4 2026", "Q1 2027", "Q2 2027"])
    progress = st.slider("Progress", 0, 100, 0)
    submit = st.form_submit_button("Generate Recommendation", type="primary")

if submit:
    try:
        r = api_post(
            "/api/agents/roadmap",
            json={
                "feature_name": feature or "New Initiative",
                "priority": priority,
                "status": status,
                "owner": owner,
                "quarter": quarter,
                "progress": progress,
            },
            timeout=20,
        )
        r.raise_for_status()
        st.session_state.roadmap_item = r.json()
    except Exception as e:
        st.error(f"Backend error: {e}")

if "roadmap_item" in st.session_state:
    q = st.session_state.roadmap_item
    st.success(f"Recommended quarter: {q['recommended_quarter']}")
    st.write("Dependencies:", ", ".join(q["dependencies"]))
    st.dataframe(pd.DataFrame([q]), use_container_width=True, hide_index=True)

st.divider()
st.subheader("Roadmap Flow")
st.write("Backlog → Planned → In Progress → Testing → Released")
sample = pd.DataFrame({
    "Quarter": ["Q3 2026", "Q3 2026", "Q4 2026", "Q1 2027"],
    "Feature": ["Feedback Clustering", "RICE Prioritization", "AI PRD Generator", "Analytics"],
    "Progress": [100, 75, 45, 15],
})
st.plotly_chart(
    px.bar(
        sample,
        x="Feature",
        y="Progress",
        color="Quarter",
        title="Initiative Progress",
        template="plotly_dark",
        color_discrete_sequence=["#818cf8", "#c084fc", "#34d399", "#f472b6"]
    ),
    use_container_width=True
)
st.dataframe(sample, use_container_width=True, hide_index=True)
