import streamlit as st

# 1. 로그인 여부를 안전하게 확인합니다 (secrets.toml 설정 기반)
is_logged_in = st.user.get("is_logged_in", False)

# 2. 각 파이썬 파일을 페이지 객체로 정의합니다.
login_page = st.Page("login.py", title="구글 로그인", icon="🔐")
home_page = st.Page("home.py", title="홈", icon="🏠", default=True)
dashboard_page = st.Page("dashboard.py", title="판매 대시보드", icon="📊")
settings_page = st.Page("settings.py", title="환경설정", icon="⚙️")

# 3. 로그인 여부에 따라 네비게이션 메뉴를 동적으로 구성합니다.
if not is_logged_in:
    # 미로그인 상태일 때는 오직 로그인 페이지만 노출하여 다른 페이지 접근을 차단합니다.
    app_navigation = st.navigation([login_page])
else:
    # 로그인 성공 시 모든 서비스 페이지 및 설정 페이지 접근을 허용합니다.
    app_navigation = st.navigation({
        "서비스": [home_page, dashboard_page],
        "계정 및 설정": [settings_page, login_page]
    })

# 4. 네비게이션을 실행합니다.
app_navigation.run()
