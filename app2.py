import streamlit as st
import base64
import os
import sqlite3
from dotenv import load_dotenv
from openai import OpenAI

# .env 파일에서 환경변수 로드
load_dotenv()

st.set_page_config(page_title="AI 채팅 챗봇", page_icon="💬")
st.title("💬 OpenAI 채팅 (GPT-5.5+ 모델 지원)")

# ==========================================
# 1. SQLite 데이터베이스 관리 함수들
# ==========================================

DB_FILE = "chat_history.db"

def init_database():
    """데이터베이스 파일 및 대화 저장 테이블 생성"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT,
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def load_messages_from_db():
    """DB에서 이전 대화 기록 불러오기"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT role, content FROM messages ORDER BY id ASC")
    rows = cursor.fetchall()
    conn.close()
    
    saved_messages = []
    for row in rows:
        saved_messages.append({"role": row[0], "content": row[1]})
    return saved_messages


def save_message_to_db(role, content):
    """신규 메시지를 DB에 영구 저장"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    text_to_save = content if isinstance(content, str) else "[이미지 첨부 메시지]"
    
    cursor.execute("INSERT INTO messages (role, content) VALUES (?, ?)", (role, text_to_save))
    conn.commit()
    conn.close()


def clear_chat_history():
    """DB와 세션의 대화 내역 전체 삭제"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM messages")
    conn.commit()
    conn.close()
    st.session_state.messages = []


# ==========================================
# 2. 이미지 처리 함수
# ==========================================

def encode_image(image_file):
    """이미지 파일을 Base64 문자열로 변환"""
    return base64.b64encode(image_file.getvalue()).decode("utf-8")


def build_user_content(user_text, attached_file):
    """텍스트와 첨부파일을 결합하여 OpenAI 메시지 생성"""
    if not attached_file:
        return user_text

    # 텍스트 파일인 경우
    if attached_file.type == "text/plain":
        file_text = attached_file.getvalue().decode("utf-8")
        return f"[첨부 파일: {attached_file.name}]\n{file_text}\n\n[질문]: {user_text}"

    # 이미지 파일인 경우 (Vision 규격)
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


# ==========================================
# 3. 화면 UI 및 사이드바 함수
# ==========================================

def setup_sidebar():
    """사이드바 설정 (API Key, 모델 선택, 파일 첨부, 대화 초기화)"""
    with st.sidebar:
        st.header("⚙️ 설정 및 모델 선택")

        # 1. OpenAI API Key 확인
        env_api_key = os.getenv("OPENAI_API_KEY", "")

        if env_api_key:
            st.success("✅ .env의 API Key 적용됨")
            api_key = env_api_key
        else:
            st.warning("⚠️ .env에 API Key가 없습니다.")
            api_key = st.text_input("OpenAI API Key", type="password", placeholder="sk-...")

        st.divider()

        # 2. 최신 GPT-5.5 이상 모델 선택
        model_options = [
            "gpt-5.6-luna",    # (기본값) 빠르고 가벼운 고효율 모델
            "gpt-5.6-terra",   # 지능과 속도의 균형 모델
            "gpt-5.6-sol",     # 최신 플래그십 최고 성능 모델
            "gpt-5.5",         # GPT-5.5 표준 전문 작업 모델
            "gpt-5.5-pro",     # GPT-5.5 정밀 추론 모델
        ]

        selected_model = st.selectbox(
            "🤖 AI 모델 선택",
            options=model_options,
            index=0,  # 기본값: gpt-5.6-luna
            help="최신 GPT-5.5 및 5.6 모델 중 원하는 모델을 선택하세요."
        )

        st.divider()

        # 3. 이미지 및 텍스트 파일 첨부
        uploaded_file = st.file_uploader(
            "이미지 또는 텍스트 파일 첨부",
            type=["png", "jpg", "jpeg", "txt"]
        )

        if uploaded_file and uploaded_file.type.startswith("image/"):
            st.image(uploaded_file, caption="첨부된 이미지 미리보기", use_container_width=True)

        st.divider()

        # 4. 대화 기록 초기화 버튼
        if st.button("🗑️ 대화 기록 초기화", use_container_width=True):
            clear_chat_history()
            st.rerun()

        return api_key, selected_model, uploaded_file


def display_chat_history():
    """대화 내역 화면 렌더링"""
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]

        with st.chat_message(role):
            if isinstance(content, str):
                st.write(content)
            elif isinstance(content, list):
                for item in content:
                    if item.get("type") == "text":
                        st.write(item.get("text"))
                    elif item.get("type") == "image_url":
                        st.image(item.get("image_url", {}).get("url"), caption="첨부한 이미지")


# ==========================================
# 4. 메인 실행 로직
# ==========================================

def main():
    # DB 초기화
    init_database()

    # 앱 실행 시 DB에서 이전 대화 기록 불러오기 (최초 1회)
    if "messages" not in st.session_state:
        st.session_state.messages = load_messages_from_db()

    # 사이드바 설정 (API Key, 선택한 모델, 첨부 파일)
    api_key, selected_model, uploaded_file = setup_sidebar()

    # 대화 기록 화면 출력
    display_chat_history()

    # 채팅 입력창
    user_prompt = st.chat_input("질문이나 메시지를 입력하세요...")

    if user_prompt:
        if not api_key:
            st.error("OpenAI API Key가 설정되지 않았습니다!")
            return

        # 1. 사용자 메시지 구성 및 DB/세션 저장
        user_content = build_user_content(user_prompt, uploaded_file)
        st.session_state.messages.append({"role": "user", "content": user_content})
        save_message_to_db("user", user_prompt)

        # 2. 화면에 사용자 메시지 즉시 표시
        with st.chat_message("user"):
            st.write(user_prompt)
            if uploaded_file and uploaded_file.type.startswith("image/"):
                st.image(uploaded_file, caption="첨부한 이미지")

        # 3. OpenAI API 호출 및 스트리밍 답변 생성 (선택된 모델 사용)
        client = OpenAI(api_key=api_key)

        with st.chat_message("assistant"):
            stream_response = client.chat.completions.create(
                model=selected_model,
                messages=st.session_state.messages,
                stream=True
            )
            full_response = st.write_stream(stream_response)

        # 4. AI 답변 DB/세션 저장
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        save_message_to_db("assistant", full_response)


if __name__ == "__main__":
    main()
