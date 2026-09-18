import streamlit as st

def show_login_page():
    st.header("로그인이 필요합니다")
    st.write("서비스를 이용하려면 아래 로그인 버튼을 눌러주세요.")
    
    login_button = st.button("로그인", type="primary")
    if login_button:
        st.login()

def show_user_profile():
    st.header("사용자 프로필")
    st.success(f"환영합니다, {st.user.name}님!")
    
    st.write("### 사용자 정보")
    st.write(f"- 이름: {st.user.name}")
    st.write(f"- 이메일: {st.user.email}")
    
    logout_button = st.button("로그아웃")
    if logout_button:
        st.logout()

def main():
    st.title("Streamlit 사용자 인증 (st.login / st.user)")
    
    if st.user.is_logged_in:
        show_user_profile()
    else:
        show_login_page()

if __name__ == "__main__":
    main()