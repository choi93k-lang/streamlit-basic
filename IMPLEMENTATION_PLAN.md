# [구현 계획서] 로그인 여부에 따른 동적 네비게이션(Conditional Navigation) 구현

Streamlit 공식 [Conditional Navigation](https://docs.streamlit.io/develop/concepts/multipage-apps/page-and-navigation) 패턴을 적용하여, 사용자가 **로그인하지 않은 상태에서는 다른 페이지(홈, 대시보드, 설정 등)에 접근할 수 없도록** 사이드바 메뉴 및 접근을 제한하는 계획입니다.

---

## 1. 구현 목표 및 핵심 로직

- **미로그인 상태 (`not is_logged_in`)**:
  - 사이드바 메뉴에 오직 **[로그인 페이지]**만 노출됩니다.
  - 홈, 대시보드, 환경설정 등 다른 페이지는 메뉴에 나타나지 않으며 접근이 차단됩니다.
- **로그인 상태 (`is_logged_in`)**:
  - 홈, 대시보드, 환경설정, 내 프로필(로그아웃) 등 모든 서비스 메뉴가 정상 노출되고 자유롭게 접근할 수 있습니다.

---

## 2. 변경할 파일 및 수정 내용

### [stream_pages/main.py](file:///c:/Projects/streamlit-basic/stream_pages/main.py) (수정)
메인 컨트롤러에서 `is_logged_in` 값을 확인하여 `st.navigation`에 전달할 페이지 목록을 동적으로 변경합니다:

```python
import streamlit as st

# 로그인 여부 확인 (미설정 시에도 에러 없이 False 반환)
is_logged_in = st.user.get("is_logged_in", False)

login_page = st.Page("login.py", title="로그인", icon="🔐")
home_page = st.Page("home.py", title="홈", icon="🏠")
dashboard_page = st.Page("dashboard.py", title="판매 대시보드", icon="📊")
settings_page = st.Page("settings.py", title="환경설정", icon="⚙️")

if not is_logged_in:
    # 1. 미로그인 시: 로그인 페이지만 네비게이션에 등록 (다른 페이지 원천 차단)
    app_navigation = st.navigation([login_page])
else:
    # 2. 로그인 성공 시: 모든 서비스 페이지 및 설정 페이지 접근 허용
    app_navigation = st.navigation({
        "서비스": [home_page, dashboard_page],
        "계정 및 설정": [settings_page, login_page]
    })

app_navigation.run()
```

---

## 3. 검증 계획

1. **로그인 전 상태 확인**:
   - `uv run streamlit run stream_pages/main.py` 실행 시 사이드바에 '로그인' 페이지만 노출되고 다른 페이지가 보이지 않는지 확인
2. **구글 로그인 완료 후 상태 확인**:
   - 구글 로그인 완료 시 사이드바에 '홈', '판매 대시보드', '환경설정' 메뉴가 활성화되는지 확인
3. **로그아웃 후 상태 확인**:
   - 로그아웃 클릭 시 즉시 다시 로그인 화면만 남는지 확인
