# [구현 계획서] Streamlit 공식 User 인증 기능 (st.login / st.logout / st.user) 구현

Streamlit 공식 문서([Streamlit User API](https://docs.streamlit.io/develop/api-reference/user))를 기반으로, `app3.py`에 공식 사용자 인증 기능을 초보자가 이해하기 쉽고 직관적으로 작성하기 위한 계획입니다.

---

## 1. 개요 및 배경

Streamlit은 `st.login()`, `st.logout()`, `st.user`를 통해 표준 OIDC(OpenID Connect, 예: Google, Microsoft 등) 기반의 로그인 기능을 제공합니다.

- **`st.user.is_logged_in`**: 현재 사용자가 로그인되어 있는지 확인 (`True` / `False`)
- **`st.login()`**: 설정된 OIDC 공급자 로그인 화면으로 리다이렉트
- **`st.logout()`**: 로그아웃 후 사용자 세션/쿠키 초기화
- **`st.user`**: 로그인된 사용자의 정보(`name`, `email` 등)를 담은 객체

> [!IMPORTANT]
> **실제 작동 시 필요한 사전 요구사항**:
> 1. `authlib>=1.3.2` 라이브러리 설치 필요 (`uv add "streamlit[auth]"` 또는 `uv add authlib`)
> 2. `.streamlit/secrets.toml`에 OIDC Provider(Google, MS 등) 설정 필요 (`redirect_uri`, `cookie_secret`, `client_id`, `client_secret`, `server_metadata_url`)
> 3. 만약 이 설정이 없는 상태에서 `st.login()` 버튼을 누르면 설정 누락 오류가 발생합니다.

---

## 2. 사용자 검토 및 확인 필요 사항

`app3.py` 구현 방향에 대해 어떤 방식을 선호하시는지 확인이 필요합니다:

- **방안 1 (공식 문서 순수 표준 코드 - 권장)**:
  - Streamlit 공식 문서의 가장 기본적이고 직관적인 코드로 `app3.py`를 구성합니다.
  - 실제 구글 로그인 등을 연동할 수 있도록 `.streamlit/secrets.toml` 설정 예시 파일 안내를 함께 제공합니다.
- **방안 2 (공식 코드 + 모의 실습 안내 포함)**:
  - 공식 코드를 기본으로 하되, 실제 OIDC 설정 없이도 로컬에서 로그인 전/후 화면이 어떻게 바뀌는지 살펴볼 수 있는 가이드나 모의 토글 기능을 함께 구성합니다.

---

## 3. 세부 작업 단계 (구현 계획)

### 1단계: 필수 패키지 점검 및 설치
- `uv add "streamlit[auth]"` 명령어로 `authlib` 패키지 설치 진행

### 2단계: `app3.py` 코드 작성
- 기존의 불완전한 코드(`st.App`)를 정리하고 공식 문서 표준 구조로 작성:
  1. `show_login_section()`: 미로그인 상태일 때 로그인 안내 메시지 및 `st.login()` 버튼 제공
  2. `show_user_profile()`: 로그인 상태일 때 `st.user.name`, `st.user.email` 등 정보 표시 및 `st.logout()` 버튼 제공
  3. `main()`: `st.user.is_logged_in` 조건에 따라 위 두 함수 중 하나를 호출하는 단순한 진입점 구성

### 3단계: OIDC 설정 템플릿 안내 (`.streamlit/secrets.toml.example`)
- 구글(Google) OIDC 로그인을 바로 테스트해볼 수 있도록 설정 가이드 문서 제공

---

## 4. 검증 계획

1. **문법 및 패키지 검증**: `uv run python -m py_compile app3.py` 실행
2. **동작 테스트**: `uv run streamlit run app3.py` 실행하여 로그인 전 화면 정상 렌더링 확인
