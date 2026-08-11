import streamlit as st
import re

def init_auth():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user" not in st.session_state:
        st.session_state.user = None
    if "user_db" not in st.session_state:
        st.session_state.user_db = {
            "admin": {"email": "user@enterprise.com", "password": "password123", "role": "Product Manager"},
            "user@enterprise.com": {"username": "admin", "password": "password123", "role": "Product Manager"}
        }

def validate_email(email: str) -> bool:
    return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email) is not None

def render_login():
    st.markdown("<h1 style='text-align: center;'>AI Product Manager</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748B;'>COPILOT WORKSPACE</p>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab_login, tab_signup = st.tabs(["Sign In", "Sign Up"])

        with tab_login:
            with st.form("login_form"):
                login_input = st.text_input("Username or Email", placeholder="user@enterprise.com")
                password = st.text_input("Password", type="password")
                if st.form_submit_button("Sign In", use_container_width=True, type="primary"):
                    login_key = login_input.strip().lower()
                    user_db = st.session_state.user_db
                    if login_key in user_db and user_db[login_key]["password"] == password:
                        st.session_state.authenticated = True
                        st.session_state.user = {
                            "name": user_db[login_key].get("username", login_key),
                            "email": user_db[login_key].get("email", login_key),
                            "role": "Product Manager"
                        }
                        st.success("Authentication successful!")
                        st.rerun()
                    else:
                        st.error("Invalid credentials.")

        with tab_signup:
            with st.form("signup_form"):
                new_username = st.text_input("Username", placeholder="e.g. alex_pm")
                new_email = st.text_input("Email", placeholder="e.g. alex@enterprise.com")
                new_password = st.text_input("Password", type="password")
                confirm_password = st.text_input("Confirm Password", type="password")
                if st.form_submit_button("Create Account", use_container_width=True, type="primary"):
                    u_clean = new_username.strip().lower()
                    e_clean = new_email.strip().lower()
                    if not u_clean or not e_clean or not new_password:
                        st.error("All fields are required.")
                    elif not validate_email(e_clean):
                        st.error("Please enter a valid email.")
                    elif new_password != confirm_password:
                        st.error("Passwords do not match.")
                    else:
                        acc = {"username": u_clean, "email": e_clean, "password": new_password, "role": "Product Manager"}
                        st.session_state.user_db[u_clean] = acc
                        st.session_state.user_db[e_clean] = acc
                        st.success("Account created! Switch to 'Sign In'.")

def render_sidebar():
    with st.sidebar:
        st.markdown("### AI Product Manager")
        st.caption("COPILOT WORKSPACE")
        st.divider()

        page = st.radio(
            "Navigation",
            ["Dashboard", "Customer Feedback", "Customer Pain Points", "Prioritized Initiatives", "PRD Generator", "Roadmap Planner"],
            key="nav_sidebar_radio",
            label_visibility="collapsed"
        )

        st.divider()
        if st.session_state.user:
            st.caption("User Session")
            with st.container(border=True):
                user = st.session_state.user
                st.markdown(f"**{user.get('name', 'User')}**")
                st.caption(f"{user.get('email', '')}")
                if st.button("Sign Out", use_container_width=True):
                    st.session_state.authenticated = False
                    st.session_state.user = None
                    st.rerun()
    return page
