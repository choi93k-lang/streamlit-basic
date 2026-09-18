import streamlit as st

def show_login_section():
    """로그인 전 안내 메시지와 로그인 버튼을 표시합니다."""
    st.header("로그인이 필요합니다")
    st.write("구글 계정으로 로그인하려면 아래 버튼을 눌러주세요.")
    
    login_button = st.button("Google 계정으로 로그인", type="primary")
    if login_button:
        st.login()

def show_user_profile():
    """로그인 성공 후 사용자 정보와 로그아웃 버튼을 표시합니다."""
    st.header("사용자 프로필")
    
    user_name = st.user.get("name", "사용자")
    user_email = st.user.get("email", "이메일 없음")
    
    st.success(f"환영합니다, {user_name}님!")
    st.write("### 내 계정 정보")
    st.write(f"- **이름**: {user_name}")
    st.write(f"- **이메일**: {user_email}")
    
    logout_button = st.button("로그아웃")
    if logout_button:
        st.logout()

def show_login_page():
    """로그인 화면의 메인 진입점입니다."""
    st.title("🔐 Google 계정 인증")
    
    is_logged_in = st.user.get("is_logged_in", False)
    if is_logged_in:
        show_user_profile()
    else:
        show_login_section()

show_login_page()

