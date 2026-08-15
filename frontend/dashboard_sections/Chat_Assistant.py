import streamlit as st
from agents.chat_agent import ChatAgent
from backend.memory.conversation_memory import ConversationMemory

def render_chat_assistant():
    st.title("Dedicated Chat Assistant")
    st.caption("Interactive product copilot powered by Google Gemini and persistent SQLite conversation memory")
    
    col_a, col_b = st.columns([5, 1])
    with col_b:
        if st.button("Clear Memory", use_container_width=True):
            ConversationMemory.clear_memory()
            st.rerun()

    chat_history = ConversationMemory.get_history()
    for message in chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if prompt := st.chat_input("Ask about features, feedback, or roadmaps...", key="chat_page_input"):
        ConversationMemory.add_message("user", prompt)
        with st.chat_message("user"):
            st.write(prompt)
        with st.chat_message("assistant"):
            chat_agent = ChatAgent()
            res = chat_agent.execute({"prompt": prompt})
            reply = res["response"]
            st.write(reply)
            ConversationMemory.add_message("assistant", reply)