import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import streamlit as st
from frontend.auth import init_auth, render_login, render_sidebar
from frontend.dashboard_sections import (
    render_dashboard_overview,
    render_customer_feedback,
    render_customer_pain_points,
    render_prioritized_initiatives,
    render_prd_generator,
    render_roadmap,
    render_chat_assistant
)
from agents.chat_agent import ChatAgent
from backend.memory.conversation_memory import ConversationMemory

st.set_page_config(
    page_title="AI Product Manager Copilot",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session Auth
init_auth()

def render_fixed_right_chatbot():
    st.markdown(
        """
        <style>
        div[data-testid="stPopover"] {
            position: fixed !important;
            bottom: 30px !important;
            right: 30px !important;
            width: 70px !important;
            height: 60px !important;
            z-index: 999999 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    with st.popover("Chat"):
        st.markdown("### AI PM Copilot")
        st.caption("Ask questions about VOC feedback, pain points, PRDs, or priorities.")
        st.divider()
        chat_history = ConversationMemory.get_history()
        for message in chat_history[-4:]:
            with st.chat_message(message["role"]):
                st.write(message["content"])
        if prompt := st.chat_input("Ask a question...", key="fixed_chat_input"):
            ConversationMemory.add_message("user", prompt)
            chat_agent = ChatAgent()
            res = chat_agent.execute({"prompt": prompt})
            ConversationMemory.add_message("assistant", res["response"])
            st.rerun()

if not st.session_state.get("authenticated", False):
    render_login()
else:
    selected_page = render_sidebar()
    st.text_input("Search VOC feedback, pain points, PRDs, and initiatives...", label_visibility="collapsed")
    
    if selected_page == "Dashboard":
        render_dashboard_overview()
    elif selected_page in ["Customer Feedback", "Feedback & VOC Ingestion"]:
        render_customer_feedback()
    elif selected_page == "Customer Pain Points":
        render_customer_pain_points()
    elif selected_page == "Prioritized Initiatives":
        render_prioritized_initiatives()
    elif selected_page == "PRD Generator":
        render_prd_generator()
    elif selected_page == "Roadmap Planner":
        render_roadmap()
    elif selected_page == "Chat Assistant":
        render_chat_assistant()
    else:
        render_dashboard_overview()
        
    render_fixed_right_chatbot()