# [구현 계획서] Streamlit Navigation 및 페이지 전환 API 구현

Streamlit 공식 문서([Streamlit Navigation API Reference](https://docs.streamlit.io/develop/api-reference/navigation))의 4가지 핵심 컴포넌트를 학습하고 체험할 수 있는 예제 페이지를 `stream_pages/` 디렉터리에 추가하기 위한 계획입니다.

---

## 1. 개요 및 학습 목표

Streamlit 최신 버전(1.36+ ~ 1.64+)의 공식 다중 페이지 네비게이션 핵심 API 4가지를 구현합니다:

1. **`st.Page`**: 각 페이지의 화면과 제목, 아이콘을 정의하는 객체 (파일 경로 또는 함수 지정 가능)
2. **`st.navigation`**: 정의된 페이지들을 사이드바 메뉴나 상단 탭으로 묶어 앱을 실행하는 컨트롤러
3. **`st.page_link`**: 사용자가 클릭하여 다른 페이지로 이동할 수 있는 시각적 링크 버튼
4. **`st.switch_page`**: 버튼 클릭이나 로직 처리 후 코드로 특정 페이지로 자동 이동시키는 함수

---

## 2. 제안 파일 구조 및 내용

### 1) 추가할 파일: `stream_pages/navigation_demo.py`
초보자가 여러 파일을 왔다 갔다 하지 않고도 핵심 개념을 한눈에 볼 수 있도록, **`st.Page(함수)`** 방식을 활용하여 가장 직관적으로 작성합니다.

- **`show_home_page()`**:
  - 홈 화면 소개
  - `st.page_link`: 소개 페이지로 이동하는 링크 버튼 예제
  - `st.switch_page`: 버튼을 누르면 코드로 바로 소개 페이지로 점프하는 예제
- **`show_about_page()`**:
  - 소개 화면 및 `st.page_link`를 통한 홈 복귀 링크 예제
- **`show_settings_page()`**:
  - 설정 화면
- **`main()`**:
  - `st.Page`로 위 3개 함수를 페이지로 등록
  - `st.navigation`으로 묶어 사이드바에 자동 메뉴를 생성하고 `pg.run()` 실행

---

## 3. 세부 작업 단계

1. **계획 검토 및 사용자 승인**
2. **`stream_pages/navigation_demo.py` 작성**:
   - `st.Page`, `st.navigation`, `st.page_link`, `st.switch_page` 구현
3. **문법 검증 및 동작 확인**:
   - `uv run python -m py_compile stream_pages/navigation_demo.py`
   - `uv run streamlit run stream_pages/navigation_demo.py`
4. **Git 커밋**: 작업 완료 후 로컬 커밋 및 결과 보고서(`WALKTHROUGH.md`) 작성
