import streamlit as st
import requests

API = "http://127.0.0.1:8000"
st.title("AI Product Manager Assistant")
st.caption("Ask about prioritization, PRDs, roadmaps, themes and product strategy.")

if "messages" not in st.session_state:
    st.session_state.messages = []

if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(str(message["content"]))

prompt = st.chat_input("Ask a product management question...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = requests.post(API + "/api/orchestrate", json={"prompt": prompt}, timeout=30)
            response.raise_for_status()
            result = response.json()
            answer = result.get("response", result)
            st.markdown(str(answer))
        except Exception as e:
            answer = f"Unable to reach backend. Start FastAPI first. Error: {e}"
            st.error(answer)

        st.session_state.messages.append({"role": "assistant", "content": answer})
