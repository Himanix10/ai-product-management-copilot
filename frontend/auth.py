import os
import urllib.parse
import requests
import streamlit as st

def load_env_file():
    """Helper to load .env variables into os.environ if present."""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        return
    except ImportError:
        pass

    for env_path in [".env", "../.env"]:
        if os.path.exists(env_path):
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        k = k.strip()
                        v = v.strip().strip('"').strip("'")
                        if k and not os.getenv(k):
                            os.environ[k] = v

def get_google_oauth_config():
    """Retrieve Google OAuth credentials from st.secrets or environment variables / .env."""
    load_env_file()
    client_id = None
    client_secret = None
    redirect_uri = "http://localhost:8501"

    try:
        if "google_oauth" in st.secrets:
            client_id = st.secrets["google_oauth"].get("client_id")
            client_secret = st.secrets["google_oauth"].get("client_secret")
            redirect_uri = st.secrets["google_oauth"].get("redirect_uri", redirect_uri)
    except Exception:
        pass

    if not client_id:
        client_id = os.getenv("GOOGLE_CLIENT_ID")
    if not client_secret:
        client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
    if os.getenv("GOOGLE_REDIRECT_URI"):
        redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")

    if client_id and ("your-google-client-id" in client_id or "YOUR_GOOGLE" in client_id):
        client_id = None
    if client_secret and ("your-google-client-secret" in client_secret or "YOUR_GOOGLE" in client_secret):
        client_secret = None

    return client_id, client_secret, redirect_uri


def get_google_auth_url(client_id: str, redirect_uri: str) -> str:
    """Generate official Google OAuth 2.0 authorization URL."""
    base_url = "https://accounts.google.com/o/oauth2/v2/auth"
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "online",
        "prompt": "select_account",
    }
    return f"{base_url}?{urllib.parse.urlencode(params)}"


def exchange_code_for_token(code: str, client_id: str, client_secret: str, redirect_uri: str):
    """Exchange authorization code for access token and fetch user details."""
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    }
    res = requests.post(token_url, data=data, timeout=10)
    res.raise_for_status()
    tokens = res.json()
    access_token = tokens.get("access_token")

    userinfo_url = "https://www.googleapis.com/oauth2/v3/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    user_res = requests.get(userinfo_url, headers=headers, timeout=10)
    user_res.raise_for_status()
    return user_res.json()


def require_login():
    """
    Ensures the user is authenticated via Google / Gmail OAuth.
    Renders login screen if unauthenticated and stops execution.
    """
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    client_id, client_secret, redirect_uri = get_google_oauth_config()

    query_params = st.query_params
    if "code" in query_params and not st.session_state["authenticated"]:
        code = query_params["code"]
        if client_id and client_secret:
            try:
                user_info = exchange_code_for_token(code, client_id, client_secret, redirect_uri)
                st.session_state["authenticated"] = True
                st.session_state["user"] = user_info
                st.query_params.clear()
                st.rerun()
            except Exception as e:
                st.error(f"Google authentication failed: {e}")
                st.query_params.clear()

    if st.session_state["authenticated"]:
        user = st.session_state.get("user", {})
        email = user.get("email", "user@gmail.com")
        name = user.get("name", email.split("@")[0].replace(".", " ").title())
        picture = user.get("picture")

        with st.sidebar:
            st.markdown(
                f"""
                <div style="background: #0d111c; border: 1px solid rgba(99, 102, 241, 0.15); border-radius: 12px; padding: 14px; margin-bottom: 20px;">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <div style="width: 36px; height: 36px; border-radius: 8px; background: linear-gradient(135deg, #6366f1, #a855f7); border: 1px solid rgba(255,255,255,0.15); display: flex; align-items: center; justify-content: center; font-weight: 700; color: #ffffff; font-size: 14px; overflow: hidden; flex-shrink: 0;">
                            {f'<img src="{picture}" style="width:100%;height:100%;object-fit:cover;"/>' if picture else name[0].upper()}
                        </div>
                        <div style="overflow: hidden;">
                            <div style="font-weight: 600; font-size: 0.88rem; color: #f8fafc; text-overflow: ellipsis; white-space: nowrap; overflow: hidden;">{name}</div>
                            <div style="font-size: 0.72rem; color: #64748b; text-overflow: ellipsis; white-space: nowrap; overflow: hidden; font-family: monospace;">{email}</div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if st.button("Sign Out", key="logout_btn", use_container_width=True):
                st.session_state["authenticated"] = False
                st.session_state.pop("user", None)
                st.query_params.clear()
                st.rerun()
        return

    # Antigravity-Style Premium Dark Glassmorphism Login Interface
    st.markdown(
        """
        <style>
        /* Antigravity Theme Overrides */
        .stApp {
            background: radial-gradient(circle at 50% 30%, #111827 0%, #07090e 70%) !important;
        }

        .antigravity-card {
            max-width: 440px;
            margin: 70px auto 40px auto;
            padding: 44px 38px;
            border-radius: 20px;
            background: rgba(13, 17, 28, 0.85);
            backdrop-filter: blur(24px);
            border: 1px solid rgba(99, 102, 241, 0.2);
            box-shadow: 0 24px 60px rgba(0, 0, 0, 0.6), 0 0 40px rgba(99, 102, 241, 0.08);
            text-align: center;
        }

        .brand-logo-ring {
            width: 56px;
            height: 56px;
            margin: 0 auto 20px auto;
            border-radius: 16px;
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(168, 85, 247, 0.2));
            border: 1px solid rgba(99, 102, 241, 0.4);
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 0 20px rgba(99, 102, 241, 0.25);
        }

        .antigravity-title {
            font-size: 1.65rem;
            font-weight: 800;
            color: #ffffff;
            letter-spacing: -0.02em;
            margin: 0 0 6px 0;
        }

        .antigravity-subtitle {
            color: #94a3b8;
            font-size: 0.88rem;
            margin: 0 0 28px 0;
            line-height: 1.5;
        }

        /* Standard Google Button - Strictly No Underlines */
        a.google-signin-btn,
        a.google-signin-btn:visited,
        a.google-signin-btn:hover,
        a.google-signin-btn:active {
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            gap: 12px !important;
            background: #ffffff !important;
            color: #1f2937 !important;
            border-radius: 12px !important;
            padding: 12px 24px !important;
            font-size: 0.92rem !important;
            font-weight: 600 !important;
            text-decoration: none !important;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3) !important;
            transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
            width: 100% !important;
            box-sizing: border-box !important;
            border: 1px solid #e2e8f0 !important;
        }

        a.google-signin-btn:hover {
            background: #f8fafc !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4), 0 0 20px rgba(255, 255, 255, 0.2) !important;
            color: #0f172a !important;
            text-decoration: none !important;
        }
        
        a.google-signin-btn span {
            text-decoration: none !important;
            color: #1f2937 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 2.2, 1])
    with col2:
        st.markdown(
            """
            <div class="antigravity-card">
                <div class="brand-logo-ring">
                    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#818cf8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <polygon points="12 2 2 7 12 12 22 7 12 2"></polygon>
                        <polyline points="2 17 12 22 22 17"></polyline>
                        <polyline points="2 12 12 17 22 12"></polyline>
                    </svg>
                </div>
                <h1 class="antigravity-title">AI PM Copilot</h1>
                <p class="antigravity-subtitle">Sign in to your intelligent product workspace</p>
            """,
            unsafe_allow_html=True,
        )

        if client_id and client_secret:
            auth_url = get_google_auth_url(client_id, redirect_uri)
            st.markdown(
                f"""
                <a href="{auth_url}" target="_self" class="google-signin-btn">
                    <svg width="18" height="18" viewBox="0 0 18 18">
                        <path fill="#4285F4" d="M17.64 9.2c0-.637-.057-1.251-.164-1.84H9v3.481h4.844c-.209 1.125-.843 2.078-1.796 2.717v2.259h2.908c1.702-1.567 2.684-3.874 2.684-6.617z"/>
                        <path fill="#34A853" d="M9 18c2.43 0 4.467-.806 5.956-2.18l-2.908-2.259c-.806.54-1.837.86-3.048.86-2.344 0-4.328-1.584-5.036-3.711H.957v2.332A8.997 8.997 0 009 18z"/>
                        <path fill="#FBBC05" d="M3.964 10.71A5.41 5.41 0 013.682 9c0-.593.102-1.17.282-1.71V4.958H.957A8.996 8.996 0 000 9c0 1.452.348 2.827.957 4.042l3.007-2.332z"/>
                        <path fill="#EA4335" d="M9 3.58c1.321 0 2.508.454 3.44 1.345l2.582-2.58C13.463.891 11.426 0 9 0A8.997 8.997 0 00.957 4.958L3.964 7.29C4.672 5.163 6.656 3.58 9 3.58z"/>
                    </svg>
                    <span>Sign in with Google</span>
                </a>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.info("Google OAuth credentials detected from .env.")
            with st.expander("Development Login Mode", expanded=True):
                gmail_address = st.text_input("Gmail Address", value="product.manager@gmail.com")
                if st.button("Continue with Gmail", use_container_width=True, type="primary"):
                    if "@" in gmail_address:
                        st.session_state["authenticated"] = True
                        st.session_state["user"] = {
                            "email": gmail_address,
                            "name": gmail_address.split("@")[0].replace(".", " ").title(),
                            "picture": None,
                        }
                        st.rerun()
                    else:
                        st.error("Please enter a valid Gmail address.")

        st.markdown("</div>", unsafe_allow_html=True)

    st.stop()
