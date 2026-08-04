import streamlit as st
from pathlib import Path
import importlib.util

from auth import require_login

st.set_page_config(page_title="AI PM Copilot", layout="wide")

st.markdown(
    """
    <style>
    .block-container{max-width:1400px;padding-top:1.5rem}
    [data-testid="stMetric"]{border:1px solid rgba(128,128,128,.25);border-radius:14px;padding:15px}
    </style>
    """,
    unsafe_allow_html=True,
)

require_login()

st.title("AI Product Manager Copilot")
st.subheader("Multi-agent product intelligence workspace")

section_names = [
    "Feedback Explorer",
    "Feature Requests",
    "PRD Generator",
    "Roadmap",
    "Chat Assistant",
]

section_map = {
    "Feedback Explorer": "Feedback_Explorer",
    "Feature Requests": "Feature_Requests",
    "PRD Generator": "PRD_Generator",
    "Roadmap": "Roadmap",
    "Chat Assistant": "Chat_Assistant",
}

tabs = st.tabs(section_names)

for tab, section_name in zip(tabs, section_names):
    with tab:
        module_name = section_map[section_name]
        module_path = Path(__file__).resolve().parent / "dashboard_sections" / f"{module_name}.py"
        if module_path.exists():
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        else:
            st.error(f"Section module not found: {module_path}")
