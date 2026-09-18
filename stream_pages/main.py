import os
import streamlit as st
from dotenv import load_dotenv

def setup_auth_secrets():
    """환경변수(.env)에서 Google OAuth 설정값을 읽어 Streamlit secrets에 주입합니다."""
    load_dotenv()
    
    auth_config = {
        "auth": {
            "redirect_uri": os.getenv("AUTH_REDIRECT_URI", "http://localhost:8501/oauth2callback"),
            "cookie_secret": os.getenv("AUTH_COOKIE_SECRET", ""),
            "client_id": os.getenv("AUTH_CLIENT_ID", ""),
            "client_secret": os.getenv("AUTH_CLIENT_SECRET", ""),
            "server_metadata_url": os.getenv("AUTH_SERVER_METADATA_URL", "https://accounts.google.com/.well-known/openid-configuration"),
        }
    }
    
    st.secrets.merge_programmatic_secrets(auth_config)

# 1. 앱 시작 시 .env로부터 인증 설정을 주입합니다.
setup_auth_secrets()

# 2. 로그인 여부를 안전하게 확인합니다.
is_logged_in = st.user.get("is_logged_in", False)

# 3. 각 파이썬 파일을 페이지 객체로 정의합니다.
login_page = st.Page("login.py", title="구글 로그인", icon="🔐")
home_page = st.Page("home.py", title="홈", icon="🏠", default=True)
dashboard_page = st.Page("dashboard.py", title="판매 대시보드", icon="📊")
settings_page = st.Page("settings.py", title="환경설정", icon="⚙️")

# 4. 로그인 여부에 따라 네비게이션 메뉴를 동적으로 구성합니다.
if not is_logged_in:
    app_navigation = st.navigation([login_page])
else:
    app_navigation = st.navigation({
        "서비스": [home_page, dashboard_page],
        "계정 및 설정": [settings_page, login_page]
    })

# 5. 네비게이션을 실행합니다.
app_navigation.run()
