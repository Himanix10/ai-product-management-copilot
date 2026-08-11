# frontend/app.py
import streamlit as st
from backend.database.db import get_db
from backend.database.models import Workspace

# Streamlit Page Config
st.set_page_config(page_title="AI Product Management Copilot", layout="wide")

# Initialize Workspace State
if "workspace_id" not in st.session_state:
    with get_db() as db:
        first_workspace = db.query(Workspace).first()
        st.session_state.workspace_id = first_workspace.id if first_workspace else 1

# Sidebar Navigation
st.sidebar.title("🚀 AI PM Copilot")
st.sidebar.write(f"Active Workspace ID: `{st.session_state.workspace_id}`")

page = st.sidebar.radio(
    "Navigation",
    ["PRD Generator", "Chat Assistant"]
)

# Render Corresponding Modules Directly
if page == "PRD Generator":
    from frontend.dashboard_sections.PRD_Generator import render_prd_generator
    render_prd_generator()

elif page == "Chat Assistant":
    from frontend.dashboard_sections.Chat_Assistant import render_chat_assistant
    render_chat_assistant()
