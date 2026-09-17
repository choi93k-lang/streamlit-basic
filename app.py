import streamlit as st

st.title("텍스트 입력 기능 둘러보기")

# 1. 기본값과 안내 문구 (value, placeholder)
food = st.text_input("좋아하는 음식", value="떡볶이", placeholder="음식 이름을 적어주세요")
st.write(f"선택한 음식: {food}")

st.divider()

# 2. 도움말 툴팁과 아이콘 (help, icon)
movie = st.text_input("좋아하는 영화", icon="🎬", help="가장 감명 깊게 본 영화를 적어주세요!")
st.write(f"영화: {movie}")

st.divider()

# 3. 최대 글자 수 제한 (max_chars)
nickname = st.text_input("닉네임 (최대 5글자)", max_chars=5, placeholder="5글자 이하")
st.write(f"닉네임: {nickname}")

st.divider()

# 4. 비밀번호 입력 (type="password")
password = st.text_input("비밀번호", type="password")
st.write(f"입력한 비밀번호: {password}")

st.divider()

# 5. 비활성화된 입력창 (disabled)
st.text_input("수정 불가 안내", value="이 칸은 읽기 전용입니다", disabled=True)

st.divider()

# 6. 여러 줄 텍스트 입력과 높이 조절 (height)
memo = st.text_area("메모장", height=150, placeholder="여러 줄의 긴 글을 자유롭게 적어보세요")
st.write(f"메모 내용: {memo}")

st.divider()
st.header("숫자 입력 및 슬라이더 둘러보기")

# 1. 정수 숫자 입력 (최소값, 최대값, 증감 단위)
age = st.number_input("나이", min_value=0, max_value=120, value=25, step=1)
st.write(f"나이: {age}세")

# 2. 소수점 숫자 입력 (step=0.1, format="%.1f")
height = st.number_input("키 (cm)", min_value=100.0, max_value=250.0, value=170.5, step=0.1, format="%.1f")
st.write(f"키: {height}cm")

# 3. 기본 슬라이더
score = st.slider("점수 선택", min_value=0, max_value=100, value=50)
st.write(f"선택한 점수: {score}점")

# 4. 범위 선택 슬라이더 (시작값과 끝값 동시에 선택)
price_range = st.slider("희망 가격대 (원)", min_value=0, max_value=100000, value=(20000, 60000), step=5000)
st.write(f"선택한 가격 범위: {price_range[0]:,}원 ~ {price_range[1]:,}원")

# 5. 글자 옵션 슬라이더 (st.select_slider)
satisfaction = st.select_slider(
    "서비스 만족도",
    options=["매우 불만", "불만", "보통", "만족", "매우 만족"],
    value="보통"
)
st.write(f"만족도 결과: {satisfaction}")

st.divider()
st.header("선택 및 날짜/색상 위젯 둘러보기")

# 1. 라디오 버튼 (가로 정렬: horizontal=True)
transport = st.radio("이동 수단", options=["도보", "자전거", "대중교통", "자동차"], horizontal=True)
st.write(f"선택한 이동 수단: {transport}")

# 2. 선택 박스 (드롭다운)
city = st.selectbox("거주 지역", options=["서울", "부산", "대구", "인천", "대전", "광주"])
st.write(f"선택한 지역: {city}")

# 3. 다중 선택 (여러 개 선택 가능)
hobbies = st.multiselect("취미 (여러 개 선택)", options=["독서", "영화 감상", "운동", "게임", "여행"])
st.write(f"선택한 취미: {', '.join(hobbies)}")

# 4. 체크박스와 토글 스위치
agree = st.checkbox("이용약관에 동의합니다")
notifications = st.toggle("알림 켜기", value=True)
st.write(f"동의 여부: {agree} / 알림 설정: {notifications}")

# 5. 날짜 입력 (달력 팝업)
travel_date = st.date_input("여행 출발일")
st.write(f"출발일: {travel_date}")

# 6. 색상 선택기
favorite_color = st.color_picker("좋아하는 색상 고르기", value="#00f900")
st.write(f"선택한 색상 코드: {favorite_color}")
