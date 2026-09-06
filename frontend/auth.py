import sqlite3
import bcrypt
import re
import streamlit as st
from backend.config import config


def validate_email(email: str) -> bool:
    return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email) is not None


def validate_password_complexity(password: str) -> bool:
    return len(password) >= 6


def authenticate_user(login_key: str, password_raw: str):
    conn = sqlite3.connect(config.DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, username, email, password_hash, role FROM users WHERE username = ? OR email = ?",
        (login_key, login_key),
    )
    user = cursor.fetchone()
    conn.close()
    if user and bcrypt.checkpw(password_raw.encode("utf-8"), user[3].encode("utf-8")):
        return {
            "id": user[0],
            "username": user[1],
            "email": user[2],
            "role": user[4],
        }
    return None


def register_user(username: str, email: str, password_raw: str):
    conn = sqlite3.connect(config.DATABASE_PATH)
    cursor = conn.cursor()
    pwd_hash = bcrypt.hashpw(password_raw.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    try:
        cursor.execute(
            "INSERT INTO users (username, email, password_hash, role) VALUES (?, ?, ?, ?)",
            (username, email, pwd_hash, "Product Manager"),
        )
        conn.commit()
        return True, "Account registered successfully!"
    except sqlite3.IntegrityError:
        return False, "Username or Email already registered."
    finally:
        conn.close()


def init_auth():
    st.session_state.setdefault("authenticated", False)
    st.session_state.setdefault("user", None)


def render_login():
    st.markdown("<h1 style='text-align: center;'>COPILOT WORKSPACE</h1>", unsafe_allow_html=True)
    _, center, _ = st.columns([1, 2, 1])
    with center:
        tab_login, tab_signup = st.tabs(["Sign In", "Sign Up"])
        with tab_login:
            with st.form("login_form"):
                login_input = st.text_input("Username or Email", placeholder="pradeepthi or pradeepthi297@gmail.com")
                password = st.text_input("Password", type="password")
                if st.form_submit_button("Sign In", use_container_width=True, type="primary"):
                    user = authenticate_user(login_input.strip().lower(), password)
                    if user:
                        st.session_state.authenticated = True
                        st.session_state.user = user
                        st.rerun()
                    else:
                        st.error("Invalid credentials.")

        with tab_signup:
            with st.form("signup_form"):
                u_name = st.text_input("Username", placeholder="e.g. pradeepthi")
                email = st.text_input("Email", placeholder="e.g. user@enterprise.com")
                pwd = st.text_input("Password", type="password")
                if st.form_submit_button("Create Account", use_container_width=True, type="primary"):
                    if not u_name or not email or not pwd:
                        st.error("All fields are required.")
                    elif not validate_email(email):
                        st.error("Invalid email address.")
                    elif not validate_password_complexity(pwd):
                        st.error("Password must be at least 6 characters.")
                    else:
                        ok, msg = register_user(u_name.strip().lower(), email.strip().lower(), pwd)
                        if ok:
                            st.success(msg)
                        else:
                            st.error(msg)


def render_sidebar():
    with st.sidebar:
        st.markdown("### AI Product Manager")
        st.caption("COPILOT WORKSPACE")
        st.divider()

        pages = [
            "Dashboard",
            "Feedback & VOC Ingestion",
            "Customer Pain Points",
            "Prioritized Initiatives",
            "PRD Generator",
            "Roadmap Planner",
            "Chat Assistant",
        ]
        page = st.radio("Navigation", pages, key="nav_sidebar_radio", label_visibility="collapsed")

        st.divider()
        user = st.session_state.user or {}
        st.markdown(f"**{user.get('username', 'User')}** ({user.get('role', 'PM')})")
        st.caption(f"{user.get('email', '')}")
        st.caption("Provider: Email")
        if st.button("Sign Out", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user = None
            st.rerun()
    return page