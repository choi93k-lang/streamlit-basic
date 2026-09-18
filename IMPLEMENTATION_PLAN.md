# [구현 계획서] secrets.toml 대신 .env 환경변수 기반 인증 설정 전환

Streamlit 공식 사용자 인증 기능(`st.login`, `st.user`)에서 사용하는 Google OAuth 키 정보를 `.streamlit/secrets.toml` 대신 프로젝트 루트의 **`.env` 파일에서 불러와 사용하도록 전환**하는 계획입니다.

---

## 1. 개요 및 전환 배경

- **기존 방식**: `.streamlit/secrets.toml` 파일에 `[auth]` 섹션을 직접 작성하여 사용.
- **개선 방식**: 
  1. 프로젝트 표준 환경변수 파일인 **`.env`에 구글 인증 정보를 정의**.
  2. `python-dotenv` 라이브러리를 통해 `.env` 값을 읽어온 뒤, Streamlit 1.64 공식 기능인 `st.secrets.merge_programmatic_secrets()`를 통해 인증 설정에 자동 주입.
  3. `.streamlit/secrets.toml` 파일에 의존하지 않고 `.env` 단일 파일로 모든 환경변수(OpenAI API Key 및 Google Auth)를 일원화 관리.

---

## 2. 세부 변경 계획

### 1) `.env` 파일에 Google Auth 환경변수 추가
```env
OPENAI_API_KEY=...

# Streamlit Google OIDC 인증 설정
AUTH_REDIRECT_URI=http://localhost:8501/oauth2callback
AUTH_COOKIE_SECRET=your-random-cookie-secret-key
AUTH_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
AUTH_CLIENT_SECRET=your-google-client-secret
AUTH_SERVER_METADATA_URL=https://accounts.google.com/.well-known/openid-configuration
```

### 2) `stream_pages/main.py`에 `.env` 연동 로직 추가
- 진입점 상단에서 `load_dotenv()` 실행
- `st.secrets.merge_programmatic_secrets()` 함수로 `.env`의 인증 정보를 `auth` 섹션에 주입
- 초보자가 이해하기 쉽도록 간단한 헬퍼 함수(`load_auth_from_env()`)로 단일 기능 분리

### 3) `app2.py` (런처)에도 동일하게 `.env` 연동 지원
- `st.App(..., secrets=auth_secrets)` 방식으로 런처 실행 시에도 `.env` 기반 동작 보장

### 4) `.streamlit/secrets.toml` 정리
- `.env`로 완전 이전되었음을 확인한 후, 기존 `secrets.toml`의 중복 설정 정리

---

## 3. 검증 계획

1. **문법 검증**: `uv run python -m py_compile stream_pages/main.py app2.py`
2. **동작 검증**: `secrets.toml` 없이도 `uv run streamlit run stream_pages/main.py` 실행 시 Google 로그인 정상 연결 확인
