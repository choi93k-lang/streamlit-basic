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
