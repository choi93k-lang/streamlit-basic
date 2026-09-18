# [작업 결과 보고서] Streamlit 공식 User 인증 기능 구현 (`app3.py`)

Streamlit 공식 문서([Streamlit User API](https://docs.streamlit.io/develop/api-reference/user))에 따라, `app3.py`에 공식 인증 컴포넌트(`st.login`, `st.logout`, `st.user`)를 적용하였습니다.

---

## 1. 주요 변경 내역

### 1) 의존 패키지 설치
- Streamlit 공식 인증 모듈에 필요한 `authlib` 패키지를 `uv add "streamlit[auth]"`를 통해 설치 완료.

### 2) `app3.py` 구현
파이썬 초보자도 코드를 직관적으로 이해할 수 있도록 역할을 명확히 분리하여 단순하게 작성하였습니다.
- **`show_login_page()`**:
  - 미로그인 상태일 때 안내 메시지와 로그인 버튼(`st.button("로그인")`) 표시
  - 버튼 클릭 시 공식 API인 `st.login()` 호출
- **`show_user_profile()`**:
  - 로그인 성공 시 `st.user.name`, `st.user.email`을 통한 사용자 정보 출력
  - `st.button("로그아웃")` 클릭 시 `st.logout()` 호출
- **`main()`**:
  - `st.user.is_logged_in` 속성을 확인하여 로그인 전/후 화면을 전환

### 3) OIDC 설정 템플릿 제공 (`.streamlit/secrets.toml.example`)
- 향후 실제 Google 또는 기타 OIDC 제공자와 연동할 때 필요한 설정 파일 템플릿 생성.
- `.gitignore`에 `.streamlit/secrets.toml`이 이미 안전하게 등록되어 있어 비밀 정보가 노출되지 않도록 조치됨.

---

## 2. 검증 결과

1. **파이썬 문법 컴파일**: `uv run python -m py_compile app3.py` 통과 (오류 없음)
2. **Streamlit 서버 렌더링**: 로컬 서버에서 앱 구동 및 로그인 화면 정상 렌더링 확인

---

## 3. 실행 방법

터미널에서 아래 명령어를 실행하여 웹 화면을 확인하실 수 있습니다:
```bash
uv run streamlit run app3.py
```
