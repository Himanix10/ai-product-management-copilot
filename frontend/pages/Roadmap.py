import streamlit as st


def render(roadmap):
    st.markdown("<div class='section-heading'>Roadmap</div>", unsafe_allow_html=True)
    st.markdown("<p class='section-subtitle'>A timeline of upcoming product priorities and delivery phases.</p>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    for entry in roadmap:
        st.markdown(f"### {entry['quarter']}")
        for item in entry["items"]:
            st.markdown(f"- {item}")
        st.markdown("<div style='margin-bottom:16px;'></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
