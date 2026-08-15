import streamlit as st

BG = "#dfefff"
PRIMARY = "#4f46e5"
TEXT = "#1f2937"
MUTED = "#718096"


def apply_global_styles():
    st.markdown(
        f"""
        <style>
        :root {{
            --pm-bg: {BG};
            --pm-primary: {PRIMARY};
            --pm-text: {TEXT};
            --pm-muted: {MUTED};
        }}

        .stApp {{
            background: var(--pm-bg) !important;
            color: var(--pm-text);
        }}

        [data-testid="stHeader"] {{
            background: transparent !important;
        }}

        [data-testid="stToolbar"] {{
            right: 1rem;
        }}

        section[data-testid="stSidebar"] {{
            background: #ffffff !important;
            border-right: 1px solid #d8dee8;
        }}

        section[data-testid="stSidebar"] > div {{
            padding-top: 1.6rem;
        }}

        .block-container {{
            max-width: 100% !important;
            padding: 2.4rem 4.9rem 3rem 5.1rem !important;
        }}

        .pm-brand {{
            font-size: 1.05rem;
            font-weight: 700;
            color: #273244;
            margin-bottom: .25rem;
        }}

        .pm-copilot-label {{
            color: #6d5bd0;
            font-size: .67rem;
            font-weight: 800;
            letter-spacing: .06em;
            text-transform: uppercase;
        }}

        .pm-search-wrap {{
            margin: 0 0 2.35rem 0;
        }}

        .pm-page-title {{
            font-size: 2.55rem;
            line-height: 1.05;
            font-weight: 800;
            letter-spacing: -.035em;
            margin: 0 0 .6rem 0;
            color: #172235;
        }}

        .pm-page-subtitle {{
            color: #718096;
            font-size: .98rem;
            margin-bottom: 1.55rem;
        }}

        .pm-section-title {{
            font-size: 1.2rem;
            font-weight: 750;
            margin: .25rem 0 .8rem;
            color: #263447;
        }}

        div[data-testid="stTextInput"] input,
        div[data-testid="stTextArea"] textarea,
        div[data-testid="stNumberInput"] input,
        div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {{
            background: #ffffff !important;
            border-radius: 8px !important;
        }}

        div[data-testid="stTextInput"] input,
        div[data-testid="stTextArea"] textarea {{
            border-color: #c9d6e5 !important;
        }}

        button[kind="primary"] {{
            background: linear-gradient(90deg, #4338ca, #4f46e5) !important;
            border: none !important;
            border-radius: 8px !important;
        }}

        button[kind="secondary"] {{
            border-radius: 8px !important;
        }}

        div[data-testid="stMetric"] {{
            background: rgba(255,255,255,.62);
            border: 1px solid #c9d9e9;
            border-radius: 12px;
            padding: 1rem;
        }}

        div[data-testid="stDataFrame"] {{
            border-radius: 10px;
            overflow: hidden;
        }}

        .pm-card {{
            background: rgba(255,255,255,.58);
            border: 1px solid #c8d8e8;
            border-radius: 12px;
            padding: 1rem 1.05rem;
        }}

        .pm-road-card {{
            background: rgba(255,255,255,.52);
            border: 1px solid #c8d8e8;
            border-radius: 11px;
            padding: .95rem;
            min-height: 150px;
            margin-bottom: .85rem;
        }}

        .pm-road-title {{
            font-weight: 750;
            color: #25354b;
            margin-bottom: .75rem;
        }}

        .pm-user-card {{
            border: 1px solid #d8dee8;
            border-radius: 9px;
            padding: 1rem;
            margin-top: .8rem;
            background: #ffffff;
        }}

        .pm-chat-fallback {{
            background: #ffffff;
            border: 1px solid #d4dce7;
            border-radius: 12px;
            padding: 1rem;
        }}

        /* Make Streamlit's radio controls look like the video navigation. */
        section[data-testid="stSidebar"] div[role="radiogroup"] {{
            gap: .12rem;
        }}

        section[data-testid="stSidebar"] div[role="radiogroup"] label {{
            padding: .1rem 0 !important;
            color: #374151 !important;
            font-size: .88rem !important;
        }}

        section[data-testid="stSidebar"] div[role="radiogroup"] label > div:first-child {{
            width: 1rem !important;
            height: 1rem !important;
        }}

        @media (max-width: 900px) {{
            .block-container {{
                padding: 1.4rem 1.25rem 2rem !important;
            }}
            .pm-page-title {{ font-size: 2rem; }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_global_search():
    st.markdown('<div class="pm-search-wrap">', unsafe_allow_html=True)
    query = st.text_input(
        "Global search",
        placeholder="Search VOC feedback, pain points, PRDs, and initiatives...",
        label_visibility="collapsed",
        key="global_pm_search",
    )
    st.markdown('</div>', unsafe_allow_html=True)
    return query


def page_header(title: str, subtitle: str):
    st.markdown(f'<div class="pm-page-title">{title}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="pm-page-subtitle">{subtitle}</div>', unsafe_allow_html=True)