import streamlit as st

# 1. st.Page로 독립된 각 파이썬 파일들을 페이지로 등록합니다.
home_page = st.Page("home.py", title="홈", icon="🏠", default=True)
dashboard_page = st.Page("dashboard.py", title="판매 대시보드", icon="📊")
login_page = st.Page("login.py", title="구글 로그인", icon="🔐")
settings_page = st.Page("settings.py", title="환경설정", icon="⚙️")

# 2. st.navigation으로 카테고리별 사이드바 메뉴를 구성합니다.
app_navigation = st.navigation({
    "서비스": [home_page, dashboard_page],
    "계정 및 설정": [login_page, settings_page]
})

# 3. 네비게이션을 실행합니다.
app_navigation.run()
