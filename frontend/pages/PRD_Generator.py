import streamlit as st


def render():
    st.markdown("<div class='section-heading'>PRD Generator</div>", unsafe_allow_html=True)
    st.markdown("<p class='section-subtitle'>Turn prioritized insights into a clear product requirements summary.</p>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### Suggested PRD")
    st.markdown(
        "**Problem:** Dashboard users report slow load times and difficulty finding insights."
    )
    st.markdown(
        "**Goal:** Improve dashboard speed, clarity, and trust, with a measurable reduction in load times."
    )
    st.markdown(
        "**Success metrics:** P95 dashboard load time under 2 seconds, satisfaction score above 85%."
    )
    st.markdown("**Key requirements:** performance tuning, export support, and better analytics UX.")
    st.markdown("</div>", unsafe_allow_html=True)
