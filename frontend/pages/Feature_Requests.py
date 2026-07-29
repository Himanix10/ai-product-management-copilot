import streamlit as st


def render(features):
    st.markdown("<div class='section-heading'>Feature Requests</div>", unsafe_allow_html=True)
    st.markdown("<p class='section-subtitle'>Compare current feature ideas with RICE and priority rankings.</p>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.dataframe(features, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    with st.expander("Feature scoring details"):
        st.write(
            "RICE score = Reach × Impact × Confidence ÷ Effort. Higher scores indicate stronger product opportunities."
        )
