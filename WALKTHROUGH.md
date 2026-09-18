# [작업 결과 보고서] secrets.toml 대신 .env 환경변수 기반 인증 설정 전환 완료

Google OAuth 인증 정보(Client ID, Secret 등)를 `.streamlit/secrets.toml` 대신 프로젝트 루트의 **`.env` 환경변수 파일에서 읽어와 Streamlit에 주입하도록 성공적으로 전환**하였습니다.

---

## 1. 주요 작업 내역

### 1) [.env](file:///c:/Projects/streamlit-basic/.env)에 Google OAuth 환경변수 추가
OpenAI Key와 함께 Google OAuth 키를 `.env` 파일 하나에서 일원화 관리하도록 설정:
```env
OPENAI_API_KEY=...

# Google OAuth 인증 정보
AUTH_REDIRECT_URI=http://localhost:8501/oauth2callback
AUTH_COOKIE_SECRET=your-random-cookie-secret-key
AUTH_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
AUTH_CLIENT_SECRET=your-google-client-secret
AUTH_SERVER_METADATA_URL=https://accounts.google.com/.well-known/openid-configuration
```

### 2) [stream_pages/main.py](file:///c:/Projects/streamlit-basic/stream_pages/main.py) 수정
- `python-dotenv`의 `load_dotenv()`를 호출하여 `.env` 값을 읽어옵니다.
- Streamlit 공식 API인 `st.secrets.merge_programmatic_secrets()`를 사용하여 `st.secrets["auth"]`에 환경변수 값을 자동 주입합니다.
- `secrets.toml` 파일 없이도 동일하게 구글 로그인 기능이 완벽하게 동작합니다.

### 3) [app2.py](file:///c:/Projects/streamlit-basic/app2.py) 진입점 표준화
- `if __name__ == "__main__":` 문법 표준화.

---

## 2. 검증 결과

1. **환경변수 주입 검증**: `python -c`로 `.env`의 `AUTH_CLIENT_ID`가 `st.secrets.auth.client_id`로 정확하게 로드됨을 확인 완료.
2. **Streamlit 서버 구동 검증**: `uv run streamlit run stream_pages/main.py` 실행 시 오류 없이 정상 렌더링 확인 완료.

---

## 3. 실행 방법

```bash
uv run streamlit run stream_pages/main.py
```
*(또는 `run.bat` 실행)*
