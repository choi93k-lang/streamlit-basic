import streamlit as st

def show_login_page():
    """로그인 안내 및 로그인 버튼을 표시합니다."""
    st.header("🔐 로그인이 필요합니다")
    st.write("홈, 소개, 설정 등 서비스를 이용하시려면 먼저 로그인을 진행해주세요.")
    
    login_button = st.button("Google 계정으로 로그인", type="primary")
    if login_button:
        st.login()

def show_home_page():
    """홈 화면을 구성하고 페이지 링크와 페이지 전환 기능을 보여줍니다."""
    st.header("🏠 홈 페이지")
    user_name = st.user.get("name", "사용자")
    st.success(f"반갑습니다, {user_name}님!")
    
    st.write("Streamlit의 공식 Navigation API들을 체험해보는 메인 화면입니다.")
    st.divider()
    
    st.subheader("1. st.page_link 예제 (화면 링크 버튼)")
    st.write("클릭하면 다른 페이지로 바로 이동할 수 있는 링크 컴포넌트입니다:")
    st.page_link(about_page, label="소개 페이지로 이동하기", icon="ℹ️")
    st.page_link(settings_page, label="설정 페이지로 이동하기", icon="⚙️")
    
    st.divider()
    st.subheader("2. st.switch_page 예제 (코드로 페이지 이동)")
    st.write("버튼을 누르면 파이썬 코드가 실행되어 소개 페이지로 즉시 이동합니다:")
    move_button = st.button("🚀 소개 페이지로 즉시 점프하기")
    if move_button:
        st.switch_page(about_page)

def show_about_page():
    """서비스 소개 화면을 구성합니다."""
    st.header("ℹ️ 소개 페이지")
    st.write("이 페이지는 서비스 소개 화면입니다.")
    st.write("`st.navigation`과 `st.Page`를 사용하면 사이드바 메뉴가 자동으로 깔끔하게 생성됩니다.")
    st.divider()
    
    st.page_link(home_page, label="홈으로 돌아가기", icon="🏠")

def show_settings_page():
    """환경 설정 화면을 구성합니다."""
    st.header("⚙️ 설정 페이지")
    st.write("다양한 앱 환경 설정을 관리하는 화면 예시입니다.")
    
    theme_choice = st.selectbox("테마 선택", ["기본 테마", "다크 테마", "라이트 테마"])
    st.info(f"현재 선택된 테마: {theme_choice}")
    st.divider()
    
    # 계정 정보 및 로그아웃 버튼
    st.subheader("👤 계정 관리")
    st.write(f"- 이름: {st.user.get('name', '사용자')}")
    st.write(f"- 이메일: {st.user.get('email', '이메일 없음')}")
    logout_button = st.button("로그아웃")
    if logout_button:
        st.logout()
        
    st.divider()
    st.page_link(home_page, label="홈으로 돌아가기", icon="🏠")

# 1. 로그인 여부를 안전하게 확인합니다.
is_logged_in = st.user.get("is_logged_in", False)

# 2. st.Page를 사용하여 각 화면 함수를 페이지 객체로 정의합니다.
login_page = st.Page(show_login_page, title="로그인", icon="🔐")
home_page = st.Page(show_home_page, title="홈", icon="🏠", default=True)
about_page = st.Page(show_about_page, title="소개", icon="ℹ️")
settings_page = st.Page(show_settings_page, title="설정", icon="⚙️")

# 3. 로그인 여부에 따라 네비게이션 메뉴를 동적으로 분기합니다.
if not is_logged_in:
    # 로그인하지 않았을 때는 로그인 페이지만 노출하여 홈, 소개, 설정 접근을 차단합니다.
    app_navigation = st.navigation([login_page])
else:
    # 로그인 성공 시 모든 서비스 메뉴에 접근할 수 있도록 허용합니다.
    app_navigation = st.navigation({
        "메인 메뉴": [home_page, about_page],
        "환경 설정": [settings_page]
    })

# 4. 네비게이션 실행
app_navigation.run()
