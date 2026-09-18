import streamlit as st

def show_home():
    """홈 화면의 환영 인사와 주요 메뉴 바로가기 링크를 표시합니다."""
    st.title("🏠 홈 화면에 오신 것을 환영합니다!")
    st.write("여러 개의 파이썬 파일로 구성된 Streamlit 다중 페이지 애플리케이션입니다.")
    st.info("왼쪽 사이드바 메뉴를 이용하거나, 아래 바로가기 링크를 눌러 원하는 페이지로 이동할 수 있습니다.")
    st.divider()
    
    st.subheader("📌 주요 페이지 바로가기")
    st.page_link("dashboard.py", label="📊 대시보드 보러가기", icon="📈")
    st.page_link("login.py", label="🔐 구글 로그인 및 프로필 확인", icon="👤")
    st.page_link("settings.py", label="⚙️ 환경설정 변경하기", icon="🔧")

if __name__ == "__main__" or True:
    show_home()

