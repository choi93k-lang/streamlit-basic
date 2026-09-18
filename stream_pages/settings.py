import streamlit as st

def show_settings():
    """앱 환경설정을 변경할 수 있는 화면입니다."""
    st.title("⚙️ 환경설정")
    st.write("애플리케이션의 기본 환경을 설정할 수 있습니다.")
    st.divider()
    
    st.subheader("🎨 화면 스타일")
    theme_choice = st.radio(
        "테마 모드를 선택하세요",
        ["시스템 기본값", "라이트 모드", "다크 모드"],
        horizontal=True
    )
    
    st.subheader("🔔 알림 설정")
    email_notification = st.toggle("이메일 알림 받기", value=True)
    sound_alert = st.toggle("소리 알림 켜기", value=False)
    
    st.divider()
    save_button = st.button("설정 저장", type="primary")
    if save_button:
        st.success(f"설정이 저장되었습니다! (테마: {theme_choice}, 이메일 알림: {'켜짐' if email_notification else '꺼짐'})")

show_settings()
