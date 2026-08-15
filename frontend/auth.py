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
    if user:
        stored_hash = user[3].encode("utf-8")
        if bcrypt.checkpw(password_raw.encode("utf-8"), stored_hash):
            return {"id": user[0], "username": user[1], "email": user[2], "role": user[4]}
    return None


def register_user(username: str, email: str, password_raw: str):
    conn = sqlite3.connect(config.DATABASE_PATH)
    cursor = conn.cursor()
    pwd_hash = bcrypt.hashpw(password_raw.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    try:
        cursor.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
            (username, email, pwd_hash),
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


def _google_button():
    if st.button("Continue with Google", use_container_width=True, key="google_login"):
        st.info("Google sign-in is a visual placeholder. Connect OAuth credentials to enable it.")


def render_login():
    st.markdown(
        """
        <style>
        .login-shell {
            width: 100%;
            max-width: 555px;
            margin: 5rem auto 0;
        }
        .login-brand {
            text-align: center;
            color: #667085;
            font-size: .88rem;
            letter-spacing: .01em;
            margin-bottom: 1.15rem;
        }
        .login-or {
            text-align: center;
            color: #94a3b8;
            font-size: .78rem;
            margin: 1rem 0;
        }
        .login-form-card {
            border: 1px solid #bfd0e1;
            border-radius: 8px;
            padding: .85rem .9rem .8rem;
            background: rgba(255,255,255,.05);
        }
        </style>
        <div class="login-shell">
            <div class="login-brand">COPILOT WORKSPACE</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    _, center, _ = st.columns([1, 2, 1])
    with center:
        login_tab, signup_tab = st.tabs(["Sign In", "Sign Up"])

        with login_tab:
            _google_button()
            st.markdown('<div class="login-or">— OR —</div>', unsafe_allow_html=True)
            with st.form("login_form", clear_on_submit=False):
                login_input = st.text_input(
                    "Username or Email",
                    placeholder="pradeepthi or pradeepthi297@gmail.com",
                )
                password = st.text_input("Password", type="password")
                if st.form_submit_button("Sign In", use_container_width=True, type="primary"):
                    login_key = login_input.strip().lower()
                    user = authenticate_user(login_key, password)
                    if user:
                        st.session_state.authenticated = True
                        st.session_state.user = user
                        st.rerun()
                    else:
                        st.error("Invalid credentials. Check your username/email and password.")

        with signup_tab:
            st.markdown('<div class="login-or">Create your Copilot Workspace account</div>', unsafe_allow_html=True)
            with st.form("signup_form"):
                new_username = st.text_input("Username", placeholder="e.g. pradeepthi")
                new_email = st.text_input("Email", placeholder="e.g. user@enterprise.com")
                new_password = st.text_input("Password", type="password")
                confirm_password = st.text_input("Confirm Password", type="password")
                if st.form_submit_button("Create Account", use_container_width=True, type="primary"):
                    u_clean = new_username.strip().lower()
                    e_clean = new_email.strip().lower()
                    if not u_clean or not e_clean or not new_password:
                        st.error("All fields are required.")
                    elif not validate_email(e_clean):
                        st.error("Please enter a valid email.")
                    elif not validate_password_complexity(new_password):
                        st.error("Password must be at least 6 characters.")
                    elif new_password != confirm_password:
                        st.error("Passwords do not match.")
                    else:
                        success, msg = register_user(u_clean, e_clean, new_password)
                        if success:
                            st.success(msg)
                        else:
                            st.error(msg)


def render_sidebar():
    with st.sidebar:
        st.markdown('<div class="pm-brand">AI Product Manager</div>', unsafe_allow_html=True)
        st.markdown('<div class="pm-copilot-label">COPILOT</div>', unsafe_allow_html=True)
        st.divider()

        pages = [
            "Dashboard",
            "Feedback & VOC Ingestion",
            "Customer Pain Points",
            "Prioritized Initiatives",
            "PRD Generator",
            "Roadmap Planner",
        ]
        page = st.radio(
            "Navigation",
            pages,
            key="nav_sidebar_radio",
            label_visibility="collapsed",
        )

        st.divider()
        st.caption("Settings")
        user = st.session_state.user or {}
        st.markdown(
            f"""
            <div class="pm-user-card">
                <div style="font-weight:750; color:#273244;">{user.get('username', 'User')}</div>
                <div style="margin-top:.55rem; color:#7590aa; text-decoration:underline;">{user.get('email', '')}</div>
                <div style="margin-top:.7rem; color:#7b8797; font-size:.82rem;">Provider: Email</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Sign Out", use_container_width=True, key="sign_out"):
            st.session_state.authenticated = False
            st.session_state.user = None
            st.rerun()
    return page