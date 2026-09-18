import streamlit as st

def show_home_page():
    """홈 화면을 구성하고 페이지 링크와 페이지 전환 기능을 보여줍니다."""
    st.header("🏠 홈 페이지")
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
    
    st.page_link(home_page, label="홈으로 돌아가기", icon="🏠")

# 1. st.Page를 사용하여 각 화면 함수를 페이지 객체로 정의합니다.
home_page = st.Page(show_home_page, title="홈", icon="🏠", default=True)
about_page = st.Page(show_about_page, title="소개", icon="ℹ️")
settings_page = st.Page(show_settings_page, title="설정", icon="⚙️")

# 2. st.navigation으로 페이지들을 카테고리별로 묶어 메뉴를 구성합니다.
app_navigation = st.navigation({
    "메인 메뉴": [home_page, about_page],
    "환경 설정": [settings_page]
})

# 3. 네비게이션을 실행하여 선택된 페이지를 화면에 띄웁니다.
app_navigation.run()

