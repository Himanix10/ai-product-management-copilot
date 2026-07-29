import streamlit as st

from utils.mock_data import get_feedback, get_features, get_roadmap
from utils.styling import inject_global_styles
from pages.dashboard import render as render_dashboard
from pages.chat_assistant import render as render_chat_assistant
from pages.feedback_explorer import render as render_feedback_explorer
from pages.feature_requests import render as render_feature_requests
from pages.prd_generator import render as render_prd_generator
from pages.roadmap import render as render_roadmap

st.set_page_config(
    page_title="AI PM Copilot",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_global_styles()

page_renderer = {
    "Dashboard": lambda: render_dashboard(get_feedback(), get_features()),
    "Chat Assistant": lambda: render_chat_assistant(get_features()),
    "Feedback Explorer": lambda: render_feedback_explorer(get_feedback()),
    "Feature Requests": lambda: render_feature_requests(get_features()),
    "PRD Generator": lambda: render_prd_generator(),
    "Roadmap": lambda: render_roadmap(get_roadmap()),
}

with st.sidebar:
    st.markdown(
        """
        <div style="display:flex;align-items:center;gap:0.55rem;margin-bottom:0.2rem;">
            <div style="width:30px;height:30px;border-radius:8px;background:#5B5FEF;
                        display:flex;align-items:center;justify-content:center;font-size:16px;">🧭</div>
            <div style="font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:1.05rem;color:#F4F6F8;">
                AI PM Copilot
            </div>
        </div>
        <div style="font-size:0.75rem;color:#6B7280;margin-bottom:1rem;">
            Multi-agent product discovery &amp; planning
        </div>
        """,
        unsafe_allow_html=True,
    )

selected_page = st.sidebar.radio(
    "Navigate",
    list(page_renderer.keys()),
    index=0,
    key="page_selector",
)

st.sidebar.markdown('<div class="pm-divider" style="border-color:#242938;"></div>', unsafe_allow_html=True)

page_renderer[selected_page]()
