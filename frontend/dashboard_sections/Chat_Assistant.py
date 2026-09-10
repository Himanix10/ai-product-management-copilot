import streamlit as st

from agents.chat_agent import ChatAgent
from backend.memory.conversation_memory import ConversationMemory


def _current_user():
    return st.session_state.get(
        "user",
        {"id": "anonymous"},
    )


def _run_chat(prompt: str):

    user = _current_user()

    clean_prompt = (
        prompt or ""
    ).strip()

    if not clean_prompt:
        return

    ConversationMemory.add_message(
        role="user",
        content=clean_prompt,
        user=user,
    )

    try:

        history = ConversationMemory.get_history(
            user=user,
            limit=10,
        )

        result = ChatAgent().execute(
            {
                "prompt": clean_prompt,
                "user": user,
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
            "I’m sorry, I could not process "
            "that request right now.\n\n"
            f"Error: {exc}"
        )

    ConversationMemory.add_message(
        role="assistant",
        content=response,
        user=user,
    )


def render_chat_assistant():

    st.title("AI Product Copilot Chat")

    st.caption(
        "Ask about VOC feedback, pain points, "
        "feature demand, RICE priorities, "
        "PRDs, roadmaps, and analytics."
    )

    user = _current_user()

    _, top_right = st.columns([5, 1])

    with top_right:

        if st.button(
            "Clear Memory",
            use_container_width=True,
            key="clear_chat_page",
        ):

            ConversationMemory.clear_memory(
                user=user
            )

            st.rerun()

    history = ConversationMemory.get_history(
        user=user
    )

    if not history:

        with st.chat_message(
            "assistant",
            avatar="🤖",
        ):

            st.markdown(
                "Hi! I’m your AI Product Manager Copilot. "
                "What would you like to analyze?"
            )

    else:

        for message in history:

            role = message["role"]

            avatar = (
                "🤖"
                if role == "assistant"
                else "👤"
            )

            with st.chat_message(
                role,
                avatar=avatar,
            ):

                st.markdown(
                    message["content"]
                )

    prompt = st.chat_input(
        "Ask about feedback, initiatives, "
        "PRDs, roadmaps, or analytics...",
        key="chat_page_input",
    )

    if prompt:

        _run_chat(prompt)

        st.rerun()