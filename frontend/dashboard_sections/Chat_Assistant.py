import streamlit as st

def render_chat_assistant():
    st.title("AI Chat Assistant")
    st.caption("Ask about prioritization, PRDs, roadmaps, themes and product strategy.")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "I am your AI PM Workspace Copilot. Try asking 'What are the main feedback themes?' or 'Show priorities'."}
        ]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt := st.chat_input("Ask a product management question..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            reply = f"AI PM Copilot: Evaluated '{prompt}'. Delegating task across sub-agents."
            st.write(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})