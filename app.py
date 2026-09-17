import streamlit as st

st.title("스트림릿 시작")

name = st.text_input("이름",value="홍길동")
# st.text ("안녕하세요!")
st.write(f"{name}님 안녕하세요!")

st.divider()

# 1. 안내 문구(placeholder)가 있는 텍스트 입력
food = st.text_input("좋아하는 음식", placeholder="예: 피자, 떡볶이")
st.write(f"좋아하는 음식: {food}")

# 2. 비밀번호 입력 (입력 내용 숨김)
password = st.text_input("비밀번호", type="password")
st.write(f"입력한 비밀번호: {password}")

# 3. 최대 글자 수 제한 (max_chars)
nickname = st.text_input("닉네임 (최대 5글자)", max_chars=5)
st.write(f"닉네임: {nickname}")

# 4. 여러 줄 텍스트 입력 (text_area)
intro = st.text_area("자기소개")
st.write(f"자기소개 내용: {intro}")