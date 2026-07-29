import streamlit as st


def render(feedback):
    st.markdown("<div class='section-heading'>Feedback Explorer</div>", unsafe_allow_html=True)
    st.markdown("<p class='section-subtitle'>Slice feedback by theme and segment to surface customer pain points.</p>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    filters = st.columns([1, 1])
    with filters[0]:
        theme = st.selectbox("Theme", options=["All"] + sorted(feedback["Theme"].unique().tolist()), key="theme_filter")
    with filters[1]:
        segment = st.selectbox("Segment", options=["All"] + sorted(feedback["Segment"].unique().tolist()), key="segment_filter")

    table = feedback
    if theme != "All":
        table = table[table["Theme"] == theme]
    if segment != "All":
        table = table[table["Segment"] == segment]

    st.dataframe(table, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
