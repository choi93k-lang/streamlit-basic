import streamlit as st

st.title("Streamlit 위젯 둘러보기")

# 1. 텍스트 입력 위젯 함수
def show_text_widgets():
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

# 2. 숫자 및 슬라이더 위젯 함수
def show_number_widgets():
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

# 3. 선택 및 기타 위젯 함수
def show_selection_widgets():
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

# --- 탭 생성 및 배치 ---
tab_text, tab_number, tab_selection = st.tabs(["텍스트 입력", "숫자 및 슬라이더", "선택 및 기타"])

with tab_text:
    show_text_widgets()

with tab_number:
    show_number_widgets()

with tab_selection:
    show_selection_widgets()
