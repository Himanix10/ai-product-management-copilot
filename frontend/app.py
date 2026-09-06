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

init_auth()

def _handle_user_prompt(prompt_input: str):
    ConversationMemory.add_message("user", prompt_input)
    with st.spinner("Thinking..."):
        chat_agent = ChatAgent()
        res = chat_agent.execute({"prompt": prompt_input})
    ConversationMemory.add_message("assistant", res["response"])
    st.session_state["show_chat_popup"] = True
    st.rerun()


def _render_chat_body():
    hdr_col1, hdr_col2, hdr_col3 = st.columns([6, 2, 2])
    with hdr_col1:
        st.markdown(
            """
            <div style="display:flex; align-items:center; gap:9px;">
                <div style="background: linear-gradient(135deg, #3b82f6, #6366f1); border-radius:10px; width:34px; height:34px; display:flex; align-items:center; justify-content:center; font-size:17px; box-shadow:0 0 14px rgba(59, 130, 246, 0.55);">🤖</div>
                <div>
                    <div style="font-weight:700; color:#f8fafc; font-size:0.96rem; line-height:1.2;">AI Product Copilot</div>
                    <div style="font-size:0.72rem; color:#10b981; display:flex; align-items:center; gap:5px; margin-top:2px;">
                        <span style="display:inline-block; width:6px; height:6px; background:#10b981; border-radius:50%; box-shadow:0 0 6px #10b981;"></span>
                        Online • Powered by Gemini
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with hdr_col2:
        if st.button("Clear", key="popup_clear_mem_btn", help="Clear Conversation Memory", use_container_width=True):
            ConversationMemory.clear_memory()
            st.session_state["show_chat_popup"] = True
            st.rerun()
    with hdr_col3:
        if st.button("✕", key="popup_close_btn", help="Close Chatbot Window", use_container_width=True):
            st.session_state["show_chat_popup"] = False
            st.rerun()

    st.markdown("<hr style='border:none; border-top:1px solid rgba(255,255,255,0.12); margin:12px 0 14px 0;'/>", unsafe_allow_html=True)

    chat_history = ConversationMemory.get_history()

    if len(chat_history) <= 1:
        st.markdown("<div style='font-size:0.78rem; color:#94a3b8; margin-bottom:8px; font-weight:600;'>Suggested Prompts:</div>", unsafe_allow_html=True)
        chip_col1, chip_col2 = st.columns(2)
        with chip_col1:
            if st.button("🔴 Pain Points", key="chip_pain_points", use_container_width=True):
                _handle_user_prompt("Explain the top customer pain points")
        with chip_col2:
            if st.button("🚀 RICE Scores", key="chip_rice_initiatives", use_container_width=True):
                _handle_user_prompt("What are our prioritized initiatives and RICE scores?")

    for message in chat_history[-6:]:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    with st.form("popup_chat_form", clear_on_submit=True):
        user_text = st.text_input("Ask a question", placeholder="Ask VOC feedback, PRDs, roadmap...", label_visibility="collapsed")
        submitted = st.form_submit_button("Send ➔", use_container_width=True)

        if submitted and user_text.strip():
            _handle_user_prompt(user_text.strip())


def render_fixed_right_chatbot():
    if "show_chat_popup" not in st.session_state:
        st.session_state["show_chat_popup"] = False

    st.markdown(
        """
        <style>
        /* Glassmorphic Floating Toggle Button */
        div.stButton button[key="toggle_chat_popup_btn"],
        button[key="toggle_chat_popup_btn"],
        div[data-testid="stPopover"] {
            position: fixed !important;
            bottom: 24px !important;
            right: 24px !important;
            left: auto !important;
            top: auto !important;
            z-index: 999999 !important;
        }

        div.stButton button[key="toggle_chat_popup_btn"],
        button[key="toggle_chat_popup_btn"],
        div[data-testid="stPopover"] > button {
            background: linear-gradient(135deg, #2563eb 0%, #4f46e5 100%) !important;
            color: #ffffff !important;
            border: 1px solid rgba(255, 255, 255, 0.25) !important;
            border-radius: 30px !important;
            padding: 12px 24px !important;
            font-weight: 700 !important;
            font-size: 0.92rem !important;
            letter-spacing: 0.02em !important;
            box-shadow: 0 8px 25px rgba(37, 99, 235, 0.45), 0 0 15px rgba(79, 70, 229, 0.3) !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            cursor: pointer !important;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }

        div.stButton button[key="toggle_chat_popup_btn"]::before,
        button[key="toggle_chat_popup_btn"]::before,
        div[data-testid="stPopover"] > button::before {
            content: "";
            display: inline-block;
            width: 17px;
            height: 17px;
            margin-right: 8px;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23ffffff' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z'%3E%3C/path%3E%3C/svg%3E");
            background-repeat: no-repeat;
            background-position: center;
            background-size: contain;
        }

        div.stButton button[key="toggle_chat_popup_btn"]:hover,
        button[key="toggle_chat_popup_btn"]:hover,
        div[data-testid="stPopover"] > button:hover {
            background: linear-gradient(135deg, #1d4ed8 0%, #4338ca 100%) !important;
            border-color: rgba(255, 255, 255, 0.4) !important;
            color: #ffffff !important;
            transform: translateY(-3px) scale(1.03) !important;
            box-shadow: 0 12px 30px rgba(37, 99, 235, 0.6), 0 0 20px rgba(79, 70, 229, 0.5) !important;
        }

        @keyframes slideUpFade {
            0% {
                opacity: 0;
                transform: translateY(24px) scale(0.96);
            }
            100% {
                opacity: 1;
                transform: translateY(0) scale(1);
            }
        }

        /* Glassmorphic Floating Chat Panel */
        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .pm-chat-window-marker),
        div[data-testid="stPopoverBody"], div[data-testid="stPopoverContent"] {
            position: fixed !important;
            bottom: 84px !important;
            right: 24px !important;
            left: auto !important;
            top: auto !important;
            background: rgba(15, 23, 42, 0.94) !important;
            backdrop-filter: blur(18px) saturate(190%) !important;
            -webkit-backdrop-filter: blur(18px) saturate(190%) !important;
            color: #f8fafc !important;
            border: 1px solid rgba(255, 255, 255, 0.14) !important;
            border-radius: 20px !important;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.7), 0 0 2px rgba(255, 255, 255, 0.15) !important;
            padding: 18px !important;
            width: min(410px, calc(100vw - 32px)) !important;
            height: min(620px, calc(100vh - 116px)) !important;
            max-width: calc(100vw - 32px) !important;
            max-height: calc(100vh - 116px) !important;
            box-sizing: border-box !important;
            z-index: 999998 !important;
            overflow-y: auto !important;
            overscroll-behavior: contain !important;
            animation: slideUpFade 0.28s cubic-bezier(0.16, 1, 0.3, 1) forwards !important;
        }

        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .pm-chat-window-marker) div[data-testid="stChatMessage"] {
            padding: 10px 12px !important;
            border-radius: 12px !important;
            margin-bottom: 8px !important;
        }

        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .pm-chat-window-marker) div[data-testid="stForm"] {
            position: sticky !important;
            bottom: 0 !important;
            background: rgba(15, 23, 42, 0.98) !important;
            padding-top: 10px !important;
        }

        button[key="popup_clear_mem_btn"] {
            background: rgba(239, 68, 68, 0.15) !important;
            color: #fca5a5 !important;
            border: 1px solid rgba(239, 68, 68, 0.3) !important;
            border-radius: 8px !important;
            font-size: 0.75rem !important;
            padding: 4px 8px !important;
        }
        button[key="popup_clear_mem_btn"]:hover {
            background: rgba(239, 68, 68, 0.3) !important;
            color: #ffffff !important;
        }

        button[key="popup_close_btn"] {
            background: rgba(255, 255, 255, 0.1) !important;
            color: #cbd5e1 !important;
            border: 1px solid rgba(255, 255, 255, 0.15) !important;
            border-radius: 8px !important;
            font-size: 0.8rem !important;
            padding: 4px 8px !important;
        }
        button[key="popup_close_btn"]:hover {
            background: rgba(255, 255, 255, 0.25) !important;
            color: #ffffff !important;
        }

        button[key^="chip_"] {
            background: rgba(30, 41, 59, 0.8) !important;
            border: 1px solid rgba(255, 255, 255, 0.12) !important;
            color: #e2e8f0 !important;
            font-size: 0.76rem !important;
            border-radius: 10px !important;
            padding: 6px 10px !important;
            transition: all 0.2s ease !important;
        }
        button[key^="chip_"]:hover {
            background: rgba(59, 130, 246, 0.25) !important;
            border-color: rgba(59, 130, 246, 0.5) !important;
            color: #60a5fa !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    btn_label = "Close ✕" if st.session_state["show_chat_popup"] else "AI Copilot"
    if st.button(btn_label, key="toggle_chat_popup_btn"):
        st.session_state["show_chat_popup"] = not st.session_state["show_chat_popup"]
        st.rerun()

    if st.session_state["show_chat_popup"]:
        with st.container():
            st.markdown('<div class="pm-chat-window-marker"></div>', unsafe_allow_html=True)
            _render_chat_body()

if not st.session_state.get("authenticated", False):
    render_login()
else:
    selected_page = render_sidebar()
    
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

    if selected_page != "Chat Assistant":
        render_fixed_right_chatbot()