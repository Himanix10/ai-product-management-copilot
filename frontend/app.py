import sys
import os

# Dynamically resolve and register current directory to Python sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

import streamlit as st
from auth import init_auth, render_login, render_sidebar
from dashboard_sections import (
    render_dashboard_overview,
    render_feedback_explorer,
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

# Initialize Session & Auth State
init_auth()

def render_fixed_right_chatbot():
    """Renders a small fixed circular robot avatar button anchored at the right side."""
    
    st.markdown(
        """
        <style>
        /* Fixed positioning container anchored to bottom right */
        div[data-testid="stPopover"] {
            position: fixed !important;
            bottom: 30px !important;
            right: 30px !important;
            width: 60px !important;
            height: 60px !important;
            min-width: 60px !important;
            max-width: 60px !important;
            z-index: 999999 !important;
        }

        /* Lock internal base element dimensions */
        div[data-testid="stPopover"] > div {
            width: 60px !important;
            height: 60px !important;
        }
        
        /* Style popover trigger into a circular cyan robot button */
        div[data-testid="stPopover"] button {
            background: radial-gradient(circle at 35% 35%, #A7F3D0 0%, #38BDF8 60%, #0284C7 100%) !important;
            color: #FFFFFF !important;
            border-radius: 50% !important;
            width: 60px !important;
            height: 60px !important;
            min-width: 60px !important;
            max-width: 60px !important;
            min-height: 60px !important;
            max-height: 60px !important;
            padding: 0px !important;
            margin: 0px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            border: 2px solid #FFFFFF !important;
            box-shadow: 0 6px 20px rgba(56, 189, 248, 0.6), 0 2px 6px rgba(0, 0, 0, 0.3) !important;
            transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out !important;
            cursor: pointer !important;
        }

        /* Center icon inside button */
        div[data-testid="stPopover"] button > div {
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            width: 100% !important;
            height: 100% !important;
            padding: 0 !important;
            margin: 0 !important;
        }

        div[data-testid="stPopover"] button p {
            font-size: 28px !important;
            margin: 0 !important;
            padding: 0 !important;
            line-height: 1 !important;
        }

        /* Hover animation */
        div[data-testid="stPopover"] button:hover {
            transform: scale(1.1) !important;
            box-shadow: 0 8px 25px rgba(56, 189, 248, 0.8) !important;
            border-color: #E0F2FE !important;
        }

        /* Popover Chat Box Container */
        div[data-testid="stPopoverBody"] {
            width: 360px !important;
            max-height: 480px !important;
            border-radius: 16px !important;
            padding: 14px !important;
            background-color: #FFFFFF !important;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25) !important;
            border: 1px solid #CBD5E1 !important;
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
                reply = f"AI Copilot: Evaluated request '{prompt}'. Processing workspace telemetry..."
                st.write(reply)
                st.session_state.chat_history.append({"role": "assistant", "content": reply})

if not st.session_state.authenticated:
    render_login()
else:
    selected_page = render_sidebar()

    st.text_input("Search", label_visibility="collapsed", placeholder="Search VOC feedback, pain points, PRDs, and initiatives...")

    # Main Router matching Customer Feedback
    if selected_page == "Dashboard":
        render_dashboard_overview()
    elif selected_page in ["Customer Feedback", "Feedback & VOC Ingestion"]:
        render_feedback_explorer()
    elif selected_page == "Customer Pain Points":
        render_customer_pain_points()
    elif selected_page == "Prioritized Initiatives":
        render_prioritized_initiatives()
    elif selected_page == "PRD Generator":
        render_prd_generator()
    elif selected_page == "Roadmap Planner":
        render_roadmap()
    else:
        render_feedback_explorer()

    # Always render the constant small circular chatbot button on the right side
    render_fixed_right_chatbot()