import streamlit as st

def render_prioritized_initiatives():
    st.title("Prioritized Initiatives")
    st.caption("Evaluate and score product initiatives using the RICE methodology (Reach × Impact × Confidence / Effort)")

    with st.container(border=True):
        title = st.text_input("Initiative Title", value="Dashboard Performance Optimization")
        desc = st.text_area("Problem & Initiative Overview", value="Optimize database caching layer to reduce P95 analytical query latency.")

        col1, col2, col3, col4 = st.columns(4)
        reach = col1.number_input("Reach (Users/Quarter)", value=5000)
        impact = col2.slider("Impact (3.0 = High, 0.5 = Minimal)", 0.5, 3.0, 2.5, step=0.5)
        confidence = col3.slider("Confidence (0.5 = Low, 1.0 = High)", 0.5, 1.0, 0.8, step=0.1)
        effort = col4.number_input("Effort (Person-Months)", value=2.0, min_value=0.5, step=0.5)

        if st.button("Calculate RICE & Save Priority", type="primary"):
            score = (reach * impact * confidence) / effort
            st.success(f"Calculated RICE Score for initiative **{title}**: **{score:,.2f}**")