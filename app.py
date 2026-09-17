import streamlit as st

st.title("텍스트 입력 예시")

# 1. 기본 텍스트 입력 (기본값 지정)
movie_title = st.text_input("영화 제목", value="기생충")
st.write(f"선택한 영화 제목: {movie_title}")

st.divider()

# 2. 이메일 입력 (type="email")
email = st.text_input("이메일 주소", type="email")
st.write(f"입력한 이메일: {email}")

st.divider()

# 3. 비밀번호 입력 (type="password")
password = st.text_input("비밀번호", type="password")
st.write(f"입력한 비밀번호: {password}")

st.divider()

# 4. 검색창 입력 (type="search", placeholder)
search_query = st.text_input("검색", type="search", placeholder="검색어를 입력하세요")
st.write(f"검색어: {search_query}")

st.divider()

# 5. 여러 줄 텍스트 입력 (st.text_area)
feedback = st.text_area("한 줄 평 및 소감", placeholder="자유롭게 작성해주세요")
st.write(f"작성한 내용: {feedback}")
