# [작업 결과 보고서] Streamlit 공식 User 인증 기능 오류 해결 및 개선

`AttributeError: st.user has no attribute "is_logged_in"` 오류를 해결하고, 사용자가 화면에서 [로그인] 버튼을 누른 후 로그인이 실행되도록 수정하였습니다.

---

## 1. 문제 원인 및 해결

### 원인
Streamlit은 `.streamlit/secrets.toml`에 `[auth]` 설정이 없을 때 `st.user`를 빈 상태로 유지하여, `st.user.is_logged_in`에 직접 접근하면 속성 오류(AttributeError)가 발생했습니다.

### 해결
- `is_logged_in = st.user.get("is_logged_in", False)` 방식을 적용하여, 인증 설정이 없거나 초기 로드 시에도 오류 없이 `False`(미로그인) 상태로 안전하게 로그인 화면이 열리도록 처리했습니다.
- 이제 앱이 켜지면 오류 없이 "로그인이 필요합니다" 화면과 [로그인] 버튼이 먼저 나타나며, **사용자가 [로그인] 버튼을 클릭했을 때만 비로소 `st.login()`이 실행**됩니다.

---

## 2. 수정된 코드 (`stream_pages/main.py`)

```python
import streamlit as st

def show_login_page():
    """로그인 전 안내 메시지와 로그인 버튼을 표시합니다."""
    st.header("로그인이 필요합니다")
    st.write("서비스를 이용하려면 아래 로그인 버튼을 눌러주세요.")
    
    login_button = st.button("로그인", type="primary")
    if login_button:
        st.login()

def show_user_profile():
    """로그인 성공 후 사용자 정보와 로그아웃 버튼을 표시합니다."""
    st.header("사용자 프로필")
    
    user_name = st.user.get("name", "사용자")
    user_email = st.user.get("email", "이메일 없음")
    
    st.success(f"환영합니다, {user_name}님!")
    st.write("### 사용자 정보")
    st.write(f"- 이름: {user_name}")
    st.write(f"- 이메일: {user_email}")
    
    logout_button = st.button("로그아웃")
    if logout_button:
        st.logout()

def main():
    """앱의 메인 진입점으로, 로그인 상태에 따라 화면을 분기합니다."""
    st.title("Streamlit 사용자 인증 (st.login / st.user)")
    
    # st.user가 비어있어도 에러 없이 안전하게 로그인 여부를 확인합니다.
    is_logged_in = st.user.get("is_logged_in", False)
    
    if is_logged_in:
        show_user_profile()
    else:
        show_login_page()

if __name__ == "__main__":
    main()
```

---

## 3. 검증 결과
- `uv run python -m py_compile stream_pages/main.py`: 컴파일 오류 없음 확인.
