# [구현 계획서] Streamlit secrets.toml 공식 인증 방식으로 복원

`.env`에서 인증 정보를 동적으로 주입하던 방식에서, Streamlit의 공식 표준 방식인 **`.streamlit/secrets.toml` 파일 기반 인증으로 다시 되돌리기** 위한 계획입니다.

---

## 1. 개요 및 복원 목표

- **복원 이유**: Streamlit 프레임워크가 기본적으로 지원하는 공식 표준 설정 방식(`.streamlit/secrets.toml`)을 사용하여 코드를 가장 단순하고 직관적으로 유지.
- **주요 변경**:
  1. `.streamlit/secrets.toml`에 Google OAuth 인증 설정(`[auth]`) 복원.
  2. `stream_pages/main.py`에서 불필요해진 `.env` 주입 코드(`load_dotenv`, `setup_auth_secrets`)를 제거하고 원래의 깔끔한 네비게이션 코드로 복원.

---

## 2. 세부 변경 계획

### 1) `.streamlit/secrets.toml` 파일 복원
```toml
[auth]
redirect_uri = "http://localhost:8501/oauth2callback"
cookie_secret = "your-random-cookie-secret-key"
client_id = "your-google-client-id.apps.googleusercontent.com"
client_secret = "your-google-client-secret"
server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration"
```
*(실제 로컬 파일에는 다운로드받으신 구글 JSON의 실제 키가 안전하게 입력됩니다.)*

### 2) `stream_pages/main.py` 코드 단순화 (복원)
- `setup_auth_secrets()` 함수 및 `load_dotenv` import 제거
- Streamlit이 자체적으로 `secrets.toml`을 읽어들이므로, 순수하게 페이지만 등록하고 실행하도록 단순화

---

## 3. 검증 계획

1. **문법 검증**: `uv run python -m py_compile stream_pages/main.py`
2. **동작 검증**: `uv run streamlit run stream_pages/main.py` 실행하여 Google 로그인 화면 정상 연결 확인
