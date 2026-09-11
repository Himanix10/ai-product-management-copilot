import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import streamlit as st
from frontend.auth import init_auth, render_login, render_sidebar
from frontend.styles import apply_global_styles
from frontend.dashboard_sections import (
    render_dashboard_overview,
    render_customer_feedback,
    render_customer_pain_points,
    render_prioritized_initiatives,
    render_prd_generator,
    render_roadmap,
    render_chat_assistant,
)
from agents.chat_agent import ChatAgent
from backend.memory.conversation_memory import ConversationMemory

# Page Configuration
st.set_page_config(
    page_title="AI Product Manager Copilot",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply Global Styles & Auth
apply_global_styles()
init_auth()

def render_fixed_right_chatbot():
    """Renders the bottom-right chatbot button as a solid white box

    containing the robot icon, with a clean popover body and active conversation history.
    """
    robot_svg = (
        "data:image/svg+xml;utf8,"
        "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'>"
        "<rect x='15' y='18' width='34' height='26' rx='8' fill='%23ffffff' />"
        "<rect x='19' y='22' width='26' height='14' rx='4' fill='%230f172a' />"
        "<circle cx='26' cy='29' r='3.2' fill='%2322d3ee' />"
        "<circle cx='38' cy='29' r='3.2' fill='%2322d3ee' />"
        "<rect x='28' y='39' width='8' height='2' rx='1' fill='%2394a3b8' />"
        "<path d='M32 18 V11 M29 11 h6' stroke='%2394a3b8' stroke-width='2.5' stroke-linecap='round' />"
        "<circle cx='32' cy='9' r='2' fill='%2338bdf8' />"
        "<rect x='11' y='27' width='3.5' height='8' rx='1.5' fill='%2338bdf8' />"
        "<rect x='49.5' y='27' width='3.5' height='8' rx='1.5' fill='%2338bdf8' />"
        "</svg>"
    )

    st.markdown(
        f"""
        <style>
        div[data-testid="stPopover"] {{
            position: fixed !important;
            bottom: 25px !important;
            right: 25px !important;
            width: 60px !important;
            height: 60px !important;
            max-width: 60px !important;
            max-height: 60px !important;
            margin: 0 !important;
            padding: 0 !important;
            z-index: 999999 !important;
        }}

        div[data-testid="stPopover"] > button {{
            width: 60px !important;
            height: 60px !important;
            border-radius: 14px !important;
            padding: 0 !important;
            border: 1.5px solid #cbd5e1 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            background-color: #ffffff !important;
            background: #ffffff !important;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12) !important;
            transition: all 0.2s ease-in-out !important;
            cursor: pointer !important;
        }}

        div[data-testid="stPopover"] > button::after {{
            content: "" !important;
            width: 38px !important;
            height: 38px !important;
            background-image: url("{robot_svg}") !important;
            background-size: contain !important;
            background-repeat: no-repeat !important;
            background-position: center !important;
            display: block !important;
        }}

        div[data-testid="stPopover"] > button p,
        div[data-testid="stPopover"] > button span {{
            display: none !important;
        }}

        div[data-testid="stPopover"] > button:hover {{
            background-color: #f8fafc !important;
            border-color: #94a3b8 !important;
            transform: scale(1.06) !important;
        }}

        div[data-testid="stPopoverBody"] {{
            width: 410px !important;
            max-height: 580px !important;
            border-radius: 16px !important;
            border: 1px solid #cbd5e1 !important;
            box-shadow: 0 14px 36px rgba(15, 23, 42, 0.18) !important;
            background: #ffffff !important;
            color: #000000 !important;
            padding: 1.25rem !important;
        }}

        /* Force chat input text to be clearly visible */
        div[data-testid="stPopoverBody"] div[data-testid="stChatInput"] textarea {{
            color: #000000 !important;
            -webkit-text-fill-color: #000000 !important;
            background-color: #ffffff !important;
        }}

        div[data-testid="stPopoverBody"] [data-testid="stChatMessage"] {{
            background-color: #f8fafc !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 10px !important;
            color: #000000 !important;
        }}

        div[data-testid="stPopoverBody"] [data-testid="stChatMessage"] p {{
            color: #000000 !important;
            -webkit-text-fill-color: #000000 !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    with st.popover("🤖"):
        st.markdown(
            """
            <div style='display: flex; align-items: center; gap: 8px; margin-bottom: 2px;'>
                <span style='font-size: 1.3rem;'>🤖</span>
                <span style='font-size: 1.15rem; font-weight: 800; color: #000000;'>AI PM Copilot</span>
            </div>
            <div style='color: #475569; font-size: 0.84rem; margin-bottom: 0.8rem;'>
                Ask questions about VOC feedback, pain points, PRDs, or priorities.
            </div>
            <hr style='margin: 0.5rem 0 1rem 0; border: none; border-top: 1px solid #cbd5e1;'>
            """,
            unsafe_allow_html=True,
        )

        user_identifier = st.session_state.get("user_email", "pradeepthi297@gmail.com")
        
        # Load conversation history from SQLite
        chat_history = ConversationMemory.get_history(user={"id": user_identifier})

        if not chat_history:
            with st.chat_message("assistant", avatar="🤖"):
                st.write(
                    "Hi! I am your AI Workspace Copilot. How can I assist you today?"
                )
        else:
            for message in chat_history:
                avatar = "🤖" if message["role"] == "assistant" else "👤"
                with st.chat_message(message["role"], avatar=avatar):
                    st.write(message["content"])

        if prompt := st.chat_input(
            "Ask a question...", key="fixed_right_chatbot_input_bar"
        ):
            ConversationMemory.add_message("user", prompt, user={"id": user_identifier})
            chat_agent = ChatAgent()
            res = chat_agent.execute({"prompt": prompt, "user": {"id": user_identifier}})
            bot_reply = res.get("response", "I could not process that request.")
            ConversationMemory.add_message("assistant", bot_reply, user={"id": user_identifier})
            st.rerun()
            
# Application Routing
if not st.session_state.get("authenticated", False):
    render_login()
else:
    selected_page = render_sidebar()

    st.text_input(
        "Global Search",
        placeholder="Search VOC feedback, pain points, PRDs, and initiatives...",
        label_visibility="collapsed",
        key="global_top_search_bar",
    )
    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

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
        render_dashboard_overview()

    render_fixed_right_chatbot()