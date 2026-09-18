# [구현 계획서] 파일 기반 다중 페이지(Multipage) 앱 및 Navigation 구성

Streamlit 공식 문서의 [st.navigation](https://docs.streamlit.io/develop/api-reference/navigation/st.navigation) 및 [st.Page](https://docs.streamlit.io/develop/api-reference/navigation/st.page)를 활용하여, 여러 개의 독립된 파이썬 파일로 페이지를 나누고 하나의 네비게이션 메뉴로 접근할 수 있는 다중 페이지 앱 구조를 구현하기 위한 계획입니다.

---

## 1. 구현 목표 및 구조

`stream_pages/` 폴더 내에 역할별 독립 페이지 파일들을 만들고, `main.py`가 컨트롤러가 되어 사이드바 메뉴로 각 파일에 접근할 수 있도록 연결합니다.

### 디렉터리 및 파일 구성 제안:
```text
stream_pages/
├── main.py          # [컨트롤러] st.navigation으로 모든 하위 페이지를 등록하고 실행
├── home.py          # [페이지 1] 홈 화면 (서비스 소개 및 st.page_link 링크 버튼)
├── login.py         # [페이지 2] 앞서 연동한 Google 로그인 및 사용자 프로필 화면
├── dashboard.py     # [페이지 3] 초보자 친화적 간단한 데이터 표 및 막대 차트 화면
└── settings.py      # [페이지 4] 앱 환경설정(테마, 알림 설정 등) 화면
```

---

## 2. 각 파일별 상세 역할

1. **`stream_pages/main.py` (메인 네비게이션 진입점)**:
   - `st.Page("home.py", title="홈", icon="🏠", default=True)`
   - `st.Page("dashboard.py", title="대시보드", icon="📊")`
   - `st.Page("login.py", title="구글 로그인", icon="🔐")`
   - `st.Page("settings.py", title="환경설정", icon="⚙️")`
   - `st.navigation`으로 "서비스"와 "계정 및 설정" 그룹으로 메뉴를 묶어 `pg.run()` 실행

2. **`stream_pages/home.py`**:
   - 환영 메시지 및 각 페이지로 이동하는 `st.page_link` 버튼 배치

3. **`stream_pages/login.py`**:
   - 구글 OAuth 로그인(`st.login`) 및 프로필 확인(`st.user`) 기능 분리 배치

4. **`stream_pages/dashboard.py`**:
   - 판다스 데이터프레임과 Streamlit 기본 차트(`st.bar_chart`)를 활용한 직관적인 데이터 시각화 화면

5. **`stream_pages/settings.py`**:
   - 라디오 버튼, 토글 스위치 등을 이용한 간단한 설정 화면

---

## 3. 세부 작업 단계

1. **사용자 검토 및 승인**
2. **하위 페이지 파일 생성**:
   - `stream_pages/home.py`
   - `stream_pages/login.py`
   - `stream_pages/dashboard.py`
   - `stream_pages/settings.py`
3. **메인 네비게이션 컨트롤러 작성**:
   - `stream_pages/main.py` 업데이트
4. **문법 및 동작 검증**:
   - `uv run streamlit run stream_pages/main.py` 실행 검증
5. **Git 커밋 및 결과 보고서(`WALKTHROUGH.md`) 작성**
