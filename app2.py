import streamlit as st
import base64
import os
import sqlite3
from dotenv import load_dotenv
from openai import OpenAI

# .env 파일에서 환경변수 로드
load_dotenv()

st.set_page_config(page_title="AI 채팅 챗봇", page_icon="💬")
st.title("💬 OpenAI 채팅 (파일 & 이미지 첨부)")

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
# 2. 이미지 처리 및 팝업 대화상자 함수들
# ==========================================

def encode_image_to_base64(image_bytes):
    """이미지 바이트 데이터를 Base64 문자열로 변환"""
    return base64.b64encode(image_bytes).decode("utf-8")


@st.dialog("🖼️ 이미지 파일 첨부 (드래그 & 드롭)")
def open_image_upload_dialog():
    """이미지를 드래그 앤 드롭으로 첨부할 수 있는 팝업창"""
    st.write("이미지 파일을 아래 영역으로 **드래그하거나 클릭**하여 선택하세요.")
    
    uploaded_image = st.file_uploader(
        "이미지 선택",
        type=["png", "jpg", "jpeg", "webp"],
        label_visibility="collapsed"
    )
    
    if uploaded_image:
        st.image(uploaded_image, caption="선택한 이미지 미리보기", use_container_width=True)
        
        if st.button("✅ 이 이미지 첨부하기", use_container_width=True):
            # 세션에 이미지 데이터와 MIME 타입 저장
            st.session_state.attached_image_bytes = uploaded_image.getvalue()
            st.session_state.attached_image_type = uploaded_image.type
            st.session_state.attached_image_name = uploaded_image.name
            st.rerun()


def build_user_content(user_text, attached_doc):
    """텍스트, 문서, 첨부 이미지를 결합하여 OpenAI 메시지 포맷 생성"""
    full_text = user_text

    # 1. 텍스트/문서 파일이 있는 경우 내용 결합
    if attached_doc:
        doc_content = attached_doc.getvalue().decode("utf-8", errors="ignore")
        full_text = f"[첨부 문서: {attached_doc.name}]\n{doc_content}\n\n[질문]: {user_text}"

    # 2. 첨부된 이미지가 있는 경우 멀티모달 포맷 생성
    if "attached_image_bytes" in st.session_state and st.session_state.attached_image_bytes:
        base64_image = encode_image_to_base64(st.session_state.attached_image_bytes)
        mime_type = st.session_state.attached_image_type
        
        return [
            {"type": "text", "text": full_text},
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:{mime_type};base64,{base64_image}"
                }
            }
        ]

    return full_text


# ==========================================
# 3. 화면 UI 및 사이드바 함수
# ==========================================

def setup_sidebar():
    """사이드바 설정 (API Key, 모델, 대화 불러오기/초기화, 파일 첨부)"""
    with st.sidebar:
        st.header("⚙️ 설정 및 첨부")

        # 1. OpenAI API Key 상태 확인
        env_api_key = os.getenv("OPENAI_API_KEY", "")
        if env_api_key:
            st.success("✅ .env의 API Key 적용됨")
            api_key = env_api_key
        else:
            st.warning("⚠️ .env에 API Key가 없습니다.")
            api_key = st.text_input("OpenAI API Key", type="password", placeholder="sk-...")

        st.divider()

        # 2. 최신 AI 모델 선택
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
            index=0,
            help="최신 GPT-5.5 및 5.6 모델 중 원하는 모델을 선택하세요."
        )

        st.divider()

        # 3. 대화 내역 불러오기 및 초기화 버튼
        st.subheader("💬 대화 기록 관리")
        col_load, col_clear = st.columns(2)
        
        with col_load:
            if st.button("📥 불러오기", use_container_width=True, help="DB에서 이전 대화 기록을 불러옵니다"):
                st.session_state.messages = load_messages_from_db()
                st.rerun()

        with col_clear:
            if st.button("🗑️ 초기화", use_container_width=True, help="모든 대화 기록을 삭제합니다"):
                clear_chat_history()
                st.rerun()

        st.divider()

        # 4. 이미지 업로드 (팝업 활성화 버튼)
        st.subheader("📎 파일 및 이미지 첨부")
        
        if st.button("🖼️ 이미지 첨부 (드래그앤드롭 팝업)", use_container_width=True):
            open_image_upload_dialog()

        # 현재 첨부된 이미지 상태 표시
        if "attached_image_bytes" in st.session_state and st.session_state.attached_image_bytes:
            st.image(st.session_state.attached_image_bytes, caption=f"첨부됨: {st.session_state.attached_image_name}", use_container_width=True)
            if st.button("❌ 첨부 이미지 취소", use_container_width=True):
                st.session_state.attached_image_bytes = None
                st.session_state.attached_image_type = None
                st.session_state.attached_image_name = None
                st.rerun()

        # 5. 문서 파일 업로드 (독립 위젯)
        uploaded_doc = st.file_uploader(
            "📄 문서/텍스트 파일 첨부",
            type=["txt", "csv", "md", "json"],
            help="텍스트 기반 문서 파일을 선택하세요."
        )

        return api_key, selected_model, uploaded_doc


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

    # 앱 실행 시 세션 상태에 대화 목록이 없으면 생성
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 사이드바 설정 (API Key, 선택한 모델, 첨부 문서 파일)
    api_key, selected_model, uploaded_doc = setup_sidebar()

    # 대화 기록 화면 출력
    display_chat_history()

    # 채팅 입력창
    user_prompt = st.chat_input("질문이나 메시지를 입력하세요...")

    if user_prompt:
        if not api_key:
            st.error("OpenAI API Key가 설정되지 않았습니다!")
            return

        # 1. 사용자 메시지 구성 및 DB/세션 저장
        user_content = build_user_content(user_prompt, uploaded_doc)
        st.session_state.messages.append({"role": "user", "content": user_content})
        save_message_to_db("user", user_prompt)

        # 2. 화면에 사용자 메시지 즉시 표시
        with st.chat_message("user"):
            st.write(user_prompt)
            if "attached_image_bytes" in st.session_state and st.session_state.attached_image_bytes:
                st.image(st.session_state.attached_image_bytes, caption="첨부한 이미지")

        # 3. 첨부 이미지가 사용되었으므로 다음 질문을 위해 초기화
        if "attached_image_bytes" in st.session_state:
            st.session_state.attached_image_bytes = None
            st.session_state.attached_image_type = None
            st.session_state.attached_image_name = None

        # 4. OpenAI API 호출 및 스트리밍 답변 생성
        client = OpenAI(api_key=api_key)

        with st.chat_message("assistant"):
            stream_response = client.chat.completions.create(
                model=selected_model,
                messages=st.session_state.messages,
                stream=True
            )
            full_response = st.write_stream(stream_response)

        # 5. AI 답변 DB/세션 저장
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        save_message_to_db("assistant", full_response)


if __name__ == "__main__":
    main()
