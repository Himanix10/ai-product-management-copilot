import sys
import os

# Dynamically resolve and register project root directory to Python sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

import streamlit as st
from backend.main import run_backend_service
from auth import init_auth, render_login, render_sidebar
from dashboard_sections import (
    render_dashboard_overview,
    render_customer_feedback,
    render_customer_pain_points,
    render_prioritized_initiatives,
    render_prd_generator,
    render_roadmap
)

st.set_page_config(
    page_title="AI Product Manager Copilot",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Start backend database service directly
run_backend_service()

# Initialize session state authentication
init_auth()

def render_fixed_right_chatbot():
    st.markdown(
        """
        <style>
        div[data-testid="stPopover"] {
            position: fixed !important;
            bottom: 30px !important;
            right: 30px !important;
            width: 60px !important;
            height: 60px !important;
            z-index: 999999 !important;
        }
        div[data-testid="stPopover"] button {
            background: radial-gradient(circle at 35% 35%, #A7F3D0 0%, #38BDF8 60%, #0284C7 100%) !important;
            color: #FFFFFF !important;
            border-radius: 50% !important;
            width: 60px !important;
            height: 60px !important;
            border: 2px solid #FFFFFF !important;
            box-shadow: 0 6px 20px rgba(56, 189, 248, 0.6) !important;
        }
        div[data-testid="stPopoverBody"] {
            width: 360px !important;
            max-height: 480px !important;
            border-radius: 16px !important;
            padding: 14px !important;
            background-color: #FFFFFF !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    with st.popover("🤖"):
        st.markdown("### 🤖 AI PM Copilot")
        st.caption("Ask questions about VOC feedback, pain points, PRDs, or priorities.")
        st.divider()

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = [
                {"role": "assistant", "content": "Hi! I am your AI Workspace Copilot. How can I assist you today?"}
            ]

        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        if prompt := st.chat_input("Ask a question...", key="fixed_chat_input"):
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)

            with st.chat_message("assistant"):
                reply = f"AI Copilot: Evaluated '{prompt}'. Backend telemetry normal."
                st.write(reply)
                st.session_state.chat_history.append({"role": "assistant", "content": reply})

if not st.session_state.authenticated:
    render_login()
else:
    selected_page = render_sidebar()
    st.text_input("Search", label_visibility="collapsed", placeholder="Search VOC feedback, pain points, PRDs, and initiatives...")

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
    else:
        render_customer_feedback()

    render_fixed_right_chatbot()
