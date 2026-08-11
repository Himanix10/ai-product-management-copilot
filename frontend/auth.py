import streamlit as st
import re
import urllib.parse
import requests

def init_auth():
    """Initialize session state variables for authentication state."""
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
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None

def get_google_auth_url():
    try:
        client_id = st.secrets["google_oauth"]["client_id"]
        redirect_uri = st.secrets["google_oauth"]["redirect_uri"]
    except Exception:
        client_id = "YOUR_GOOGLE_CLIENT_ID"
        redirect_uri = "http://localhost:8501"

    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent"
    }
    return f"https://accounts.google.com/o/oauth2/v2/auth?{urllib.parse.urlencode(params)}"

def handle_google_callback():
    query_params = st.query_params
    if "code" in query_params and not st.session_state.get("authenticated", False):
        code = query_params["code"]
        try:
            client_id = st.secrets["google_oauth"]["client_id"]
            client_secret = st.secrets["google_oauth"]["client_secret"]
            redirect_uri = st.secrets["google_oauth"]["redirect_uri"]

            token_url = "https://oauth2.googleapis.com/token"
            token_data = {
                "code": code,
                "client_id": client_id,
                "client_secret": client_secret,
                "redirect_uri": redirect_uri,
                "grant_type": "authorization_code",
            }
            token_res = requests.post(token_url, data=token_data)
            token_res.raise_for_status()
            access_token = token_res.json().get("access_token")

            if access_token:
                user_info_res = requests.get(
                    "https://www.googleapis.com/oauth2/v2/userinfo",
                    headers={"Authorization": f"Bearer {access_token}"}
                )
                user_info_res.raise_for_status()
                user_data = user_info_res.json()

                email = user_data.get("email")
                name = user_data.get("name", email.split("@")[0] if email else "User")

                st.session_state.authenticated = True
                st.session_state.user = {
                    "name": name,
                    "email": email,
                    "role": "Product Manager",
                    "auth_provider": "Google"
                }
                st.query_params.clear()
                st.rerun()
        except Exception as e:
            st.error(f"Google Authentication failed: {str(e)}")

def render_login():
    handle_google_callback()

    st.markdown("<h1 style='text-align: center;'>AI Product Manager</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748B;'>COPILOT WORKSPACE</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab_login, tab_signup = st.tabs(["Sign In", "Sign Up"])

        google_url = get_google_auth_url()
        google_button_html = f"""
        <a href="{google_url}" target="_self" style="text-decoration: none;">
            <div style="display: flex; align-items: center; justify-content: center; border: 1px solid #CBD5E1; border-radius: 8px; padding: 10px; background-color: #FFFFFF; cursor: pointer; margin-bottom: 15px;">
                <span style="color: #1E293B; font-weight: 600; font-size: 14px;">{{label}}</span>
            </div>
        </a>
        """

        with tab_login:
            st.markdown(google_button_html.format(label="Continue with Google"), unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #94A3B8; font-size: 12px;'>— OR —</p>", unsafe_allow_html=True)

            with st.form("login_form"):
                login_input = st.text_input("Username or Email", placeholder="user@enterprise.com")
                password = st.text_input("Password", type="password")
                submit_login = st.form_submit_button("Sign In", use_container_width=True, type="primary")

                if submit_login:
                    login_key = login_input.strip().lower()
                    user_db = st.session_state.user_db

                    if not login_key or not password:
                        st.error("Please fill in all required fields.")
                    elif login_key in user_db and user_db[login_key]["password"] == password:
                        user_info = user_db[login_key]
                        st.session_state.authenticated = True
                        st.session_state.user = {
                            "name": user_info.get("username", login_key),
                            "email": user_info.get("email", login_key),
                            "role": user_info.get("role", "Product Manager"),
                            "auth_provider": "Email"
                        }
                        st.success("Authentication successful!")
                        st.rerun()
                    else:
                        st.error("Invalid username/email or password.")

        with tab_signup:
            st.markdown(google_button_html.format(label="Sign Up with Google"), unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #94A3B8; font-size: 12px;'>— OR —</p>", unsafe_allow_html=True)

            with st.form("signup_form"):
                new_username = st.text_input("Username", placeholder="e.g. alex_pm")
                new_email = st.text_input("Email Address", placeholder="e.g. alex@enterprise.com")
                new_password = st.text_input("Password", type="password")
                confirm_password = st.text_input("Confirm Password", type="password")
                submit_signup = st.form_submit_button("Create Account", use_container_width=True, type="primary")

                if submit_signup:
                    username_clean = new_username.strip().lower()
                    email_clean = new_email.strip().lower()
                    user_db = st.session_state.user_db

                    if not username_clean or not email_clean or not new_password:
                        st.error("All fields are required.")
                    elif not validate_email(email_clean):
                        st.error("Please enter a valid email address.")
                    elif new_password != confirm_password:
                        st.error("Passwords do not match.")
                    elif len(new_password) < 6:
                        st.error("Password must be at least 6 characters long.")
                    elif username_clean in user_db or email_clean in user_db:
                        st.error("Username or email already registered.")
                    else:
                        account_data = {
                            "username": username_clean,
                            "email": email_clean,
                            "password": new_password,
                            "role": "Product Manager"
                        }
                        st.session_state.user_db[username_clean] = account_data
                        st.session_state.user_db[email_clean] = account_data
                        st.success("Account created successfully! Please switch to 'Sign In'.")

def render_sidebar():
    """Render persistent sidebar with Customer Feedback label."""
    with st.sidebar:
        st.markdown("<h3 style='margin-bottom: 0px;'>AI Product Manager</h3>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 11px; color: #6366F1; font-weight: 600; margin-top: -5px;'>COPILOT</p>", unsafe_allow_html=True)
        st.divider()

        page = st.radio(
            "Navigation",
            [
                "Dashboard",
                "Customer Feedback",
                "Customer Pain Points",
                "Prioritized Initiatives",
                "PRD Generator",
                "Roadmap Planner"
            ],
            key="navigation_radio_updated",
            label_visibility="collapsed"
        )

        st.divider()

        if st.session_state.user:
            st.caption("Settings")
            with st.container(border=True):
                user = st.session_state.user
                st.markdown(f"**{user.get('name', 'User')}**")
                st.caption(f"{user.get('email', '')}")
                st.caption(f"Provider: {user.get('auth_provider', 'Email')}")
                if st.button("Sign Out", use_container_width=True):
                    st.session_state.authenticated = False
                    st.session_state.user = None
                    st.rerun()

    return page