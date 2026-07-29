import streamlit as st

from utils.backend_bridge import run_chat_turn


def render(features):
    st.markdown("<div class='section-heading'>Chat Assistant</div>", unsafe_allow_html=True)
    st.markdown("<p class='section-subtitle'>Ask natural questions and get product guidance from your current dataset.</p>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    query = st.text_input("What would you like to ask?", value="What are the top product priorities?", key="chat_query")
    if st.button("Submit", key="chat_submit"):
        response = run_chat_turn(query)
        st.markdown(f"<div class='section-subtitle'>{response}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
