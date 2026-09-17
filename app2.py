import streamlit as st
import base64
from openai import OpenAI

st.set_page_config(page_title="AI 채팅 챗봇", page_icon="💬")
st.title("💬 OpenAI 채팅 및 파일 첨부")

# 1. 세션 상태(대화 기록) 초기화 함수
def init_chat_history():
    if "messages" not in st.session_state:
        st.session_state.messages = []


# 2. 사이드바 설정 함수 (API Key 및 파일 첨부)
def setup_sidebar():
    with st.sidebar:
        st.header("⚙️ 설정 및 파일 첨부")
        
        # OpenAI API Key 입력창
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            placeholder="sk-...",
            help="OpenAI API 키를 입력하세요. 화면을 새로고침하면 초기화됩니다."
        )
        
        st.divider()
        
        # 이미지 및 텍스트 파일 첨부
        uploaded_file = st.file_uploader(
            "이미지 또는 텍스트 파일 첨부",
            type=["png", "jpg", "jpeg", "txt"]
        )
        
        # 첨부된 파일이 이미지일 경우 미리보기
        if uploaded_file and uploaded_file.type.startswith("image/"):
            st.image(uploaded_file, caption="첨부된 이미지 미리보기", use_container_width=True)
            
        return api_key, uploaded_file


# 3. 이전 대화 기록 화면 출력 함수
def display_chat_history():
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        
        with st.chat_message(role):
            # 텍스트 또는 멀티모달 콘텐츠 출력
            if isinstance(content, str):
                st.write(content)
            elif isinstance(content, list):
                for item in content:
                    if item.get("type") == "text":
                        st.write(item.get("text"))
                    elif item.get("type") == "image_url":
                        st.image(item.get("image_url", {}).get("url"), caption="첨부한 이미지")


# 4. 이미지를 base64 형식으로 변환하는 함수
def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode("utf-8")


# 5. 사용자 메시지 구성 함수 (텍스트 + 첨부파일)
def build_user_content(user_text, attached_file):
    if not attached_file:
        return user_text

    # 텍스트 파일인 경우 파일 내용 읽어서 결합
    if attached_file.type == "text/plain":
        file_text = attached_file.getvalue().decode("utf-8")
        return f"[첨부 파일: {attached_file.name}]\n{file_text}\n\n[질문]: {user_text}"

    # 이미지 파일인 경우 멀티모달 포맷 생성
    if attached_file.type.startswith("image/"):
        base64_image = encode_image(attached_file)
        mime_type = attached_file.type
        return [
            {"type": "text", "text": user_text},
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:{mime_type};base64,{base64_image}"
                }
            }
        ]

    return user_text


# 6. 메인 실행 로직
def main():
    init_chat_history()
    api_key, uploaded_file = setup_sidebar()
    display_chat_history()

    # 채팅 입력창
    user_prompt = st.chat_input("질문이나 메시지를 입력하세요...")

    if user_prompt:
        # API Key 입력 여부 확인
        if not api_key:
            st.error("사이드바에서 OpenAI API Key를 먼저 입력해 주세요!")
            return

        # 1) 사용자 메시지 구성 및 기록 추가
        user_content = build_user_content(user_prompt, uploaded_file)
        st.session_state.messages.append({"role": "user", "content": user_content})

        # 2) 화면에 사용자 메시지 표시
        with st.chat_message("user"):
            if isinstance(user_content, str):
                st.write(user_content)
            elif isinstance(user_content, list):
                st.write(user_prompt)
                if uploaded_file:
                    st.image(uploaded_file, caption="첨부한 이미지")

        # 3) OpenAI API 호출 및 스트리밍 답변 생성
        client = OpenAI(api_key=api_key)

        with st.chat_message("assistant"):
            # 기본 모델은 규칙에 따라 gpt-5.6-luna 사용
            stream_response = client.chat.completions.create(
                model="gpt-5.6-luna",
                messages=st.session_state.messages,
                stream=True
            )
            # 스트리밍 텍스트 실시간 출력
            full_response = st.write_stream(stream_response)

        # 4) 어시스턴트 답변 기록 추가
        st.session_state.messages.append({"role": "assistant", "content": full_response})


if __name__ == "__main__":
    main()
