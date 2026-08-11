import streamlit as st

def render_prioritized_initiatives():
    st.title("Prioritized Initiatives")
    st.caption("Evaluate initiatives using the RICE methodology (Reach × Impact × Confidence / Effort)")

    with st.container(border=True):
        title = st.text_input("Initiative Title", value="Dashboard Performance Optimization")
        
        col1, col2, col3, col4 = st.columns(4)
        reach = col1.number_input("Reach (Users/Qtr)", value=5000)
        impact = col2.slider("Impact (0.5 to 3.0)", 0.5, 3.0, 2.5, step=0.5)
        confidence = col3.slider("Confidence (0.5 to 1.0)", 0.5, 1.0, 0.8, step=0.1)
        effort = col4.number_input("Effort (Person-Months)", value=2.0, min_value=0.5, step=0.5)

        if st.button("Calculate RICE Score", type="primary"):
            if effort > 0:
                score = (reach * impact * confidence) / effort
                st.success(f"Calculated RICE Score for **{title}**: **{score:,.2f}**")
            else:
                st.error("Effort must be greater than zero.")
