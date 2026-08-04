import streamlit as st
from pathlib import Path
import importlib.util

import auth
import importlib
importlib.reload(auth)
from auth import require_login

st.set_page_config(
    page_title="AI PM Copilot",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Minimalist High-Tech Dashboard Design System CSS (Icon-Free)
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Overall Background */
    .stApp {
        background-color: #07090e;
        color: #e2e8f0;
    }
    
    .block-container {
        max-width: 1480px;
        padding-top: 1.8rem;
        padding-bottom: 3rem;
    }
    
    /* Top Command Header */
    .dashboard-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding-bottom: 1rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.06);
        margin-bottom: 1.5rem;
    }
    
    .brand-tag {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        color: #6366f1;
        background: rgba(99, 102, 241, 0.08);
        border: 1px solid rgba(99, 102, 241, 0.25);
        padding: 4px 10px;
        border-radius: 4px;
        display: inline-block;
        margin-bottom: 8px;
    }
    
    .header-title {
        font-size: 2.1rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        color: #ffffff;
        margin: 0;
    }

    .header-desc {
        color: #94a3b8;
        font-size: 0.92rem;
        margin-top: 4px;
    }
    
    /* Clean Minimalist Tabs (Linear/Vercel style) */
    div[data-baseweb="tab-list"] {
        gap: 8px !important;
        background: #0d111c !important;
        padding: 6px !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        margin-bottom: 1.5rem !important;
    }

    button[data-baseweb="tab"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 0.88rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.2px !important;
        padding: 8px 18px !important;
        border-radius: 6px !important;
        color: #64748b !important;
        background: transparent !important;
        transition: all 0.15s ease !important;
        border: none !important;
    }
    
    button[data-baseweb="tab"]:hover {
        color: #e2e8f0 !important;
        background: rgba(255, 255, 255, 0.04) !important;
    }
    
    button[aria-selected="true"] {
        color: #ffffff !important;
        background: #1e293b !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
    }
    
    div[data-baseweb="tab-highlight"] {
        display: none !important;
    }
    
    /* Dark Surface Containers & Forms */
    div[data-testid="stForm"] {
        background: #0d111c;
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    }

    /* Metric Cards */
    [data-testid="stMetric"] {
        background: #0d111c;
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 10px;
        padding: 16px 20px;
    }
    
    [data-testid="stMetricLabel"] {
        color: #64748b;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }
    
    [data-testid="stMetricValue"] {
        color: #f8fafc;
        font-weight: 700;
        font-size: 1.5rem;
    }

    /* High-Tech Slate Buttons */
    div.stButton > button[kind="primary"],
    div.stFormSubmitButton > button {
        background: #4f46e5 !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        border-radius: 8px !important;
        padding: 8px 20px !important;
        box-shadow: 0 2px 8px rgba(79, 70, 229, 0.3) !important;
        transition: all 0.15s ease !important;
    }
    
    div.stButton > button[kind="primary"]:hover,
    div.stFormSubmitButton > button:hover {
        background: #4338ca !important;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.45) !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0b0e17 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.06) !important;
    }

    /* Input Controls */
    input, textarea, select {
        background-color: #07090e !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: #f1f5f9 !important;
        border-radius: 6px !important;
    }
    
    input:focus, textarea:focus, select:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 1px #6366f1 !important;
    }

    /* Dataframe Table Polish */
    div[data-testid="stDataFrame"] {
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 8px;
        overflow: hidden;
    }

    /* Custom Scrollbars */
    ::-webkit-scrollbar {
        width: 5px;
        height: 5px;
    }
    ::-webkit-scrollbar-track {
        background: #07090e;
    }
    ::-webkit-scrollbar-thumb {
        background: #1e293b;
        border-radius: 3px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

require_login()



section_names = [
    "Dashboard Overview",
    "Feedback Explorer",
    "Feature Requests",
    "PRD Generator",
    "Roadmap",
    "Chat Assistant",
]

section_map = {
    "Dashboard Overview": "Dashboard_Overview",
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
