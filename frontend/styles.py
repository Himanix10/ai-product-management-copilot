import streamlit as st

BG = "#dfefff"
PRIMARY = "#4f46e5"


def apply_global_styles():
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

        html, body, [class*="css"] {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
            color: #000000 !important;
        }}

        /* App Canvas Background */
        .stApp {{
            background-color: {BG} !important;
            color: #000000 !important;
        }}

        [data-testid="stHeader"] {{
            background: transparent !important;
        }}

        /* ========================================================================= */
        /* INVERT SIDEBAR THEME: PURE WHITE BACKGROUND & SOLID BLACK TEXT            */
        /* ========================================================================= */
        section[data-testid="stSidebar"] {{
            background-color: #ffffff !important;
            border-right: 1px solid #d8dee8 !important;
        }}

        section[data-testid="stSidebar"] * {{
            color: #000000 !important;
            -webkit-text-fill-color: #000000 !important;
        }}

        section[data-testid="stSidebar"] div[role="radiogroup"] label,
        section[data-testid="stSidebar"] div[role="radiogroup"] label p,
        section[data-testid="stSidebar"] div[role="radiogroup"] label span {{
            color: #000000 !important;
            -webkit-text-fill-color: #000000 !important;
            font-weight: 700 !important;
            font-size: 0.93rem !important;
        }}

        /* ========================================================================= */
        /* BOTH SIDEBAR TOGGLE BUTTONS (<< INSIDE & >> OUTSIDE):                    */
        /* SOLID WHITE ROUNDED SQUARES WITH JET-BLACK CHEVRON ARROWS                 */
        /* ========================================================================= */
        [data-testid="stSidebarCollapsedControl"],
        [data-testid="collapsedControl"],
        [data-testid="stSidebarCollapseButton"],
        header[data-testid="stHeader"] {{
            visibility: visible !important;
            opacity: 1 !important;
        }}

        [data-testid="stSidebarCollapsedControl"] button,
        [data-testid="collapsedControl"] button,
        [data-testid="stSidebarCollapseButton"] button,
        button[data-testid="stSidebarCollapsedControl"],
        button[data-testid="stSidebarCollapseButton"],
        button[aria-label*="sidebar" i],
        header[data-testid="stHeader"] button {{
            background-color: #ffffff !important;
            background: #ffffff !important;
            border: 1.5px solid #cbd5e1 !important;
            border-radius: 10px !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.12) !important;
            width: 36px !important;
            height: 36px !important;
            min-width: 36px !important;
            min-height: 36px !important;
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
            padding: 0 !important;
            margin: 4px !important;
            cursor: pointer !important;
        }}

        [data-testid="stSidebarCollapsedControl"] svg,
        [data-testid="stSidebarCollapsedControl"] path,
        [data-testid="collapsedControl"] svg,
        [data-testid="collapsedControl"] path,
        [data-testid="stSidebarCollapseButton"] svg,
        [data-testid="stSidebarCollapseButton"] path,
        button[aria-label*="sidebar" i] svg,
        button[aria-label*="sidebar" i] path,
        header[data-testid="stHeader"] svg,
        header[data-testid="stHeader"] path {{
            fill: #000000 !important;
            stroke: #000000 !important;
            color: #000000 !important;
            filter: brightness(0) contrast(200%) !important;
            width: 18px !important;
            height: 18px !important;
        }}

        /* ========================================================================= */
        /* GENERAL TEXT & INPUT FIELDS                                               */
        /* ========================================================================= */
        div[data-testid="stWidgetLabel"] label,
        .stTextInput label,
        .stTextArea label,
        label, p, span {{
            color: #000000 !important;
        }}

        h1, h2, h3, h4 {{
            color: #000000 !important;
            font-weight: 800 !important;
        }}

        div[data-testid="stTextInput"] input,
        div[data-testid="stTextArea"] textarea {{
            background-color: #ffffff !important;
            color: #000000 !important;
            -webkit-text-fill-color: #000000 !important;
            border: 1.5px solid #475569 !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
        }}

        div[data-testid="stMetric"] {{
            background: rgba(255, 255, 255, 0.95) !important;
            border: 1px solid #c9d9e9 !important;
            border-radius: 14px !important;
            padding: 1.1rem 1.25rem !important;
        }}

        div[data-testid="stMetric"] [data-testid="stMetricValue"] {{
            color: #000000 !important;
            font-weight: 900 !important;
        }}

        .block-container {{
            max-width: 100% !important;
            padding: 1.5rem 3.5rem 4rem 3.5rem !important;
        }}

        /* Sign Out Button: Solid White Box with Readable Dark Text */
        section[data-testid="stSidebar"] button {{
            background-color: #ffffff !important;
            background: #ffffff !important;
            border: 1.5px solid #cbd5e1 !important;
            border-radius: 10px !important;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05) !important;
        }}

        section[data-testid="stSidebar"] button p,
        section[data-testid="stSidebar"] button span {{
            color: #000000 !important;
            -webkit-text-fill-color: #000000 !important;
            font-weight: 800 !important;
        }}

        section[data-testid="stSidebar"] button:hover {{
            background-color: #f8fafc !important;
            border-color: #94a3b8 !important;
        }}

        /* ========================================================================= */
        /* BOTTOM-RIGHT CHATBOT: PURE WHITE BOX & LARGE ROBOT ICON                   */
        /* ========================================================================= */
        div[data-testid="stPopover"] {{
            position: fixed !important;
            bottom: 25px !important;
            right: 25px !important;
            width: 60px !important;
            height: 60px !important;
            z-index: 999999 !important;
        }}

        div[data-testid="stPopover"] > button,
        div[data-testid="stPopover"] button {{
            width: 60px !important;
            height: 60px !important;
            min-width: 60px !important;
            min-height: 60px !important;
            border-radius: 14px !important;
            padding: 0 !important;
            border: 1.5px solid #cbd5e1 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            background-color: #ffffff !important;
            background: #ffffff !important;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12) !important;
            cursor: pointer !important;
        }}

        /* Make the robot emoji larger (2rem) and perfectly centered */
        div[data-testid="stPopover"] > button p,
        div[data-testid="stPopover"] > button span:not([data-baseweb="icon"]) {{
            font-size: 2rem !important;
            line-height: 1 !important;
            display: block !important;
            visibility: visible !important;
        }}

        /* Hide the dropdown/expand_more arrow icon entirely */
        div[data-testid="stPopover"] svg,
        div[data-testid="stPopover"] span[data-baseweb="icon"] {{
            display: none !important;
            visibility: hidden !important;
        }}

        /* ========================================================================= */
        /* CHAT INPUT TEXT VISIBILITY FIX                                            */
        /* ========================================================================= */
        div[data-testid="stChatInput"] textarea,
        div[data-testid="stChatInput"] input,
        textarea[aria-label*="chat" i] {{
            color: #000000 !important;
            -webkit-text-fill-color: #000000 !important;
            background-color: #ffffff !important;
        }}

        div[data-testid="stChatInput"] {{
            background-color: #ffffff !important;
            border: 1.5px solid #cbd5e1 !important;
            border-radius: 12px !important;
        }}
        /* ========================================================================= */
        /* CHATBOT POPOVER & MESSAGE TEXT COLOR: SOLID BLACK                         */
        /* ========================================================================= */
        div[data-testid="stPopoverBody"] {{
            background-color: #ffffff !important;
            color: #000000 !important;
        }}

        div[data-testid="stPopoverBody"] [data-testid="stChatMessage"] {{
            background-color: #f8fafc !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 10px !important;
            color: #000000 !important;
        }}

        div[data-testid="stPopoverBody"] [data-testid="stChatMessage"] p,
        div[data-testid="stPopoverBody"] [data-testid="stChatMessage"] span,
        div[data-testid="stPopoverBody"] [data-testid="stChatMessage"] div,
        div[data-testid="stPopoverBody"] .stMarkdown p {{
            color: #000000 !important;
            -webkit-text-fill-color: #000000 !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )