import streamlit as st


def init_auth():
    """Initializes authentication session state."""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user_email" not in st.session_state:
        st.session_state.user_email = ""
    if "user_name" not in st.session_state:
        st.session_state.user_name = ""
    if "registered_users" not in st.session_state:
        st.session_state.registered_users = {
            "pradeepthi297@gmail.com": {
                "name": "pradeepthi297",
                "password": "password123",
            }
        }


def render_login():
    """Renders a high-contrast clean white card containing Login and Sign Up tabs."""
    st.markdown(
        """
        <style>
        div[data-testid="stVerticalBlock"] label p,
        div[data-testid="stVerticalBlock"] span,
        div[data-testid="stVerticalBlock"] h1,
        div[data-testid="stVerticalBlock"] h3,
        div[data-testid="stVerticalBlock"] p,
        button[data-baseweb="tab"] p {
            color: #000000 !important;
            -webkit-text-fill-color: #000000 !important;
            font-weight: 700 !important;
        }

        div[data-testid="stButton"] button {
            background-color: #ffffff !important;
            background: #ffffff !important;
            color: #000000 !important;
            -webkit-text-fill-color: #000000 !important;
            border: 1.5px solid #cbd5e1 !important;
            border-radius: 10px !important;
            font-weight: 800 !important;
            box-shadow: 0 2px 6px rgba(0,0,0,0.05) !important;
        }

        div[data-testid="stButton"] button:hover {
            background-color: #f8fafc !important;
            border-color: #94a3b8 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 1.3, 1])

    with col2:
        st.markdown(
            """
            <div style='text-align: center; margin-bottom: 1.5rem; margin-top: 2rem;'>
                <h1 style='font-size: 2.2rem; font-weight: 900; color: #000000; margin-bottom: 0.2rem;'>AI Product Manager</h1>
                <p style='color: #475569; font-size: 1rem; font-weight: 600;'>Workspace Copilot & Intelligence Hub</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.container(border=True):
            st.markdown(
                """
                <style>
                div[data-testid="stVerticalBlock"] > div > div[data-testid="stVerticalBlock"] {
                    background-color: #ffffff !important;
                }
                </style>
                """,
                unsafe_allow_html=True,
            )

            auth_tab_login, auth_tab_signup = st.tabs(
                ["Sign In", "Create Account"]
            )

            with auth_tab_login:
                st.markdown(
                    "<div style='height: 10px;'></div>", unsafe_allow_html=True
                )
                login_email = st.text_input(
                    "Email Address",
                    placeholder="name@example.com",
                    key="login_email_input",
                )
                login_password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="••••••••",
                    key="login_password_input",
                )

                st.markdown(
                    "<div style='height: 10px;'></div>", unsafe_allow_html=True
                )

                if st.button(
                    "Sign In",
                    key="btn_signin_submit",
                    use_container_width=True,
                ):
                    users = st.session_state.registered_users
                    if (
                        login_email in users
                        and users[login_email]["password"] == login_password
                    ):
                        st.session_state.authenticated = True
                        st.session_state.user_email = login_email
                        st.session_state.user_name = users[login_email]["name"]
                        st.success("Successfully logged in!")
                        st.rerun()
                    else:
                        st.error(
                            "Invalid email address or password. Please try again."
                        )

            with auth_tab_signup:
                st.markdown(
                    "<div style='height: 10px;'></div>", unsafe_allow_html=True
                )
                signup_name = st.text_input(
                    "Full Name / Username",
                    placeholder="e.g. Pradeepthi",
                    key="signup_name_input",
                )
                signup_email = st.text_input(
                    "Email Address",
                    placeholder="name@example.com",
                    key="signup_email_input",
                )
                signup_password = st.text_input(
                    "Create Password",
                    type="password",
                    placeholder="At least 6 characters",
                    key="signup_password_input",
                )

                st.markdown(
                    "<div style='height: 10px;'></div>", unsafe_allow_html=True
                )

                if st.button(
                    "Create Account",
                    key="btn_signup_submit",
                    use_container_width=True,
                ):
                    if not signup_email or not signup_password or not signup_name:
                        st.error("Please fill in all required fields.")
                    elif signup_email in st.session_state.registered_users:
                        st.error(
                            "An account with this email already exists. Please sign in."
                        )
                    else:
                        st.session_state.registered_users[signup_email] = {
                            "name": signup_name,
                            "password": signup_password,
                        }
                        st.session_state.authenticated = True
                        st.session_state.user_email = signup_email
                        st.session_state.user_name = signup_name
                        st.success(
                            "Account created successfully! Welcome to your workspace."
                        )
                        st.rerun()


def render_sidebar():
    """Renders the sidebar navigation and user settings box."""
    with st.sidebar:
        st.markdown(
            """
            <div style='padding-top: 0.5rem; margin-bottom: 1rem;'>
                <h2 style='font-size: 1.35rem; font-weight: 800; color: #000000; margin-bottom: 0;'>AI Product Manager</h2>
                <p style='font-size: 0.75rem; font-weight: 700; color: #64748b; letter-spacing: 0.05em; text-transform: uppercase;'>Copilot</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # "Chat Assistant" successfully removed from navigation list
        selected_page = st.radio(
            "Navigation",
            [
                "Dashboard",
                "Feedback & VOC Ingestion",
                "Customer Pain Points",
                "Prioritized Initiatives",
                "PRD Generator",
                "Roadmap Planner",
            ],
            label_visibility="collapsed",
        )

        st.markdown(
            "<div style='margin-top: 4rem; margin-bottom: 1rem;'></div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<p style='font-size: 0.8rem; font-weight: 800; color: #000000; margin-bottom: 0.5rem;'>Settings</p>",
            unsafe_allow_html=True,
        )

        user_name = st.session_state.get(
            "user_name", "pradeepthi297"
        )
        user_email = st.session_state.get(
            "user_email", "pradeepthi297@gmail.com"
        )

        st.markdown(
            f"""
            <div style='background: #ffffff; border: 1.5px solid #cbd5e1; border-radius: 12px; padding: 0.85rem 1rem; margin-bottom: 0.75rem; box-shadow: 0 2px 6px rgba(0,0,0,0.04);'>
                <div style='font-weight: 800; font-size: 0.95rem; color: #000000; margin-bottom: 0.2rem;'>{user_name}</div>
                <div style='font-weight: 600; font-size: 0.8rem; color: #334155; word-break: break-all; margin-bottom: 0.3rem;'>{user_email}</div>
                <div style='font-weight: 600; font-size: 0.785rem; color: #475569;'>Provider: Email</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("Sign Out", use_container_width=True, key="sidebar_signout_btn"):
            st.session_state.authenticated = False
            st.session_state.user_email = ""
            st.session_state.user_name = ""
            st.rerun()

        return selected_page