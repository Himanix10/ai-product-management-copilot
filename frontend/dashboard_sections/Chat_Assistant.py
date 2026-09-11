import streamlit as st
from agents.chat_agent import ChatAgent
from backend.memory.conversation_memory import ConversationMemory


def _current_user():
    return st.session_state.get(
        "user_email",
        {"id": "anonymous"},
    )


def _run_chat(prompt: str):
    user_identifier = _current_user()
    clean_prompt = (prompt or "").strip()

    if not clean_prompt:
        return

    # Add user message to persistent conversation history
    ConversationMemory.add_message(
        role="user",
        content=clean_prompt,
        user={"id": user_identifier},
    )

    try:
        history = ConversationMemory.get_history(
            user={"id": user_identifier},
            limit=10,
        )

        result = ChatAgent().execute(
            {
                "prompt": clean_prompt,
                "user": {"id": user_identifier},
                "history": history,
            }
        )

        response = (
            result.get("response")
            or result.get("message")
            or "I could not process that request."
        )

    except Exception as exc:
        response = (
            "I’m sorry, I could not process that request right now.\n\n"
            f"Error: {exc}"
        )

    # Add assistant response to persistent conversation history
    ConversationMemory.add_message(
        role="assistant",
        content=response,
        user={"id": user_identifier},
    )


def render_chat_assistant():
    # Wrap section header and description inside a clean white container card
    with st.container(border=True):
        st.markdown(
            """
            <style>
            div[data-testid="stVerticalBlock"] > div > div[data-testid="stVerticalBlock"] {
                background-color: #ffffff !important;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        col_title, col_btn = st.columns([4, 1])
        with col_title:
            st.header("AI Product Copilot Chat")
            st.caption(
                "Ask about VOC feedback, pain points, feature demand, RICE priorities, "
                "PRDs, roadmaps, and analytics. Your conversation history is securely saved."
            )

        with col_btn:
            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
            if st.button("Clear History", use_container_width=True, key="clear_chat_page_btn"):
                ConversationMemory.clear_memory(user={"id": _current_user()})
                st.rerun()

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    # Fetch and render conversation history from database
    history = ConversationMemory.get_history(user={"id": _current_user()})

    if not history:
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(
                "Hi! I’m your AI Product Manager Copilot. "
                "What would you like to analyze or discuss today?"
            )
    else:
        for message in history:
            role = message["role"]
            avatar = "🤖" if role == "assistant" else "👤"
            with st.chat_message(role, avatar=avatar):
                st.markdown(message["content"])

    # Chat input box at the bottom
    prompt = st.chat_input(
        "Ask about feedback, initiatives, PRDs, roadmaps, or analytics...",
        key="chat_page_input_field",
    )

    if prompt:
        _run_chat(prompt)
        st.rerun()