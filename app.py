import streamlit as st

st.title("Streamlit 기능 둘러보기")

# ==========================================
# 1. 입력 위젯 관련 함수들
# ==========================================

def show_text_widgets():
    """텍스트 입력 관련 위젯들"""
    food = st.text_input("좋아하는 음식", value="떡볶이", placeholder="음식 이름을 적어주세요")
    st.write(f"선택한 음식: {food}")

    movie = st.text_input("좋아하는 영화", icon="🎬", help="가장 감명 깊게 본 영화를 적어주세요!")
    st.write(f"영화: {movie}")

    nickname = st.text_input("닉네임 (최대 5글자)", max_chars=5, placeholder="5글자 이하")
    st.write(f"닉네임: {nickname}")

    password = st.text_input("비밀번호", type="password")
    st.write(f"입력한 비밀번호: {password}")

    st.text_input("수정 불가 안내", value="이 칸은 읽기 전용입니다", disabled=True)

    memo = st.text_area("메모장", height=120, placeholder="여러 줄의 긴 글을 자유롭게 적어보세요")
    st.write(f"메모 내용: {memo}")


def show_number_widgets():
    """숫자 및 슬라이더 관련 위젯들"""
    age = st.number_input("나이", min_value=0, max_value=120, value=25, step=1)
    st.write(f"나이: {age}세")

    height = st.number_input("키 (cm)", min_value=100.0, max_value=250.0, value=170.5, step=0.1, format="%.1f")
    st.write(f"키: {height}cm")

    score = st.slider("점수 선택", min_value=0, max_value=100, value=50)
    st.write(f"선택한 점수: {score}점")

    price_range = st.slider("희망 가격대 (원)", min_value=0, max_value=100000, value=(20000, 60000), step=5000)
    st.write(f"선택한 가격 범위: {price_range[0]:,}원 ~ {price_range[1]:,}원")

    satisfaction = st.select_slider(
        "서비스 만족도",
        options=["매우 불만", "불만", "보통", "만족", "매우 만족"],
        value="보통"
    )
    st.write(f"만족도 결과: {satisfaction}")


def show_selection_widgets():
    """선택 상자 및 날짜/색상 관련 위젯들"""
    transport = st.radio("이동 수단", options=["도보", "자전거", "대중교통", "자동차"], horizontal=True)
    st.write(f"선택한 이동 수단: {transport}")

    city = st.selectbox("거주 지역", options=["서울", "부산", "대구", "인천", "대전", "광주"])
    st.write(f"선택한 지역: {city}")

    hobbies = st.multiselect("취미 (여러 개 선택)", options=["독서", "영화 감상", "운동", "게임", "여행"])
    st.write(f"선택한 취미: {', '.join(hobbies)}")

    agree = st.checkbox("이용약관에 동의합니다")
    notifications = st.toggle("알림 켜기", value=True)
    st.write(f"동의 여부: {agree} / 알림 설정: {notifications}")

    travel_date = st.date_input("여행 출발일")
    st.write(f"출발일: {travel_date}")

    favorite_color = st.color_picker("좋아하는 색상 고르기", value="#00f900")
    st.write(f"선택한 색상 코드: {favorite_color}")


# ==========================================
# 2. 레이아웃 및 컨테이너 관련 함수들
# ==========================================

def show_columns_and_containers():
    """컬럼 분할과 컨테이너 박스"""
    st.subheader("컬럼 나누기 (st.columns)")
    left_col, right_col = st.columns(2)
    left_col.write("👈 왼쪽 칸 (칼럼 1)")
    right_col.write("👉 오른쪽 칸 (칼럼 2)")

    st.divider()
    st.subheader("테두리 컨테이너 (st.container)")
    with st.container(border=True):
        st.write("이 상자는 `border=True` 옵션이 들어간 테두리 컨테이너입니다.")
        st.write("관련된 내용들을 묶어 카드로 만들 때 좋습니다.")


def show_expanders_and_popovers():
    """접이식 상자와 팝오버 창"""
    st.subheader("접이식 상자 (st.expander)")
    with st.expander("상세 설명 보기 (클릭하여 열기)"):
        st.write("평소에는 숨겨져 있다가 클릭하면 열리는 아코디언 상자입니다.")

    st.divider()
    st.subheader("팝오버 상자 (st.popover)")
    with st.popover("⚙️ 설정 열기"):
        st.write("버튼을 누르면 그 자리에 레이어로 뜨는 설정 팝오버입니다.")
        st.checkbox("자동 저장 사용")


@st.dialog("알림 대화상자")
def open_modal_dialog():
    st.write("화면 중앙에 뜨는 모달 팝업창입니다!")
    st.text_input("이메일을 입력하세요")
    if st.button("닫기"):
        st.rerun()


def show_dialog_and_empty():
    """모달 팝업과 동적 교체 영역"""
    st.subheader("모달 팝업창 (st.dialog)")
    if st.button("팝업 대화상자 열기"):
        open_modal_dialog()

    st.divider()
    st.subheader("내용 교체 영역 (st.empty)")
    empty_area = st.empty()
    empty_area.info("현재 상태: 대기 중")
    if st.button("상태 업데이트"):
        empty_area.success("현재 상태: 완료되었습니다!")


# ==========================================
# 3. 고정 영역 (사이드바 & 푸터)
# ==========================================

def show_sidebar():
    with st.sidebar:
        st.header("사이드바 메뉴")
        st.write("왼쪽에 고정되는 사이드바 영역입니다.")
        st.text_input("사이드바 검색")


def show_bottom_bar():
    with st.bottom:
        st.caption("화면 맨 아래 고정되는 푸터 영역입니다.")


# ==========================================
# 4. 메인 화면 구성 및 계층형 탭 배치
# ==========================================

# 고정 영역 실행
show_sidebar()
show_bottom_bar()

# 1단계: 상단 대분류 선택 (가로 버튼)
main_category = st.radio(
    "카테고리 선택",
    options=["입력 위젯", "레이아웃 및 컨테이너"],
    horizontal=True,
    label_visibility="collapsed"
)

st.divider()

# 2단계: 대분류에 따라 하위 탭 분기
if main_category == "입력 위젯":
    tab_text, tab_number, tab_selection = st.tabs(["텍스트 입력", "숫자 및 슬라이더", "선택 및 기타"])

    with tab_text:
        show_text_widgets()

    with tab_number:
        show_number_widgets()

    with tab_selection:
        show_selection_widgets()

else:
    tab_columns, tab_expanders, tab_popups = st.tabs(["컬럼 & 컨테이너", "접이식 & 팝오버", "팝업 & 교체영역"])

    with tab_columns:
        show_columns_and_containers()

    with tab_expanders:
        show_expanders_and_popovers()

    with tab_popups:
        show_dialog_and_empty()
