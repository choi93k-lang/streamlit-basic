import streamlit as st
import base64
import os
import sqlite3
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

# .env 파일에서 환경변수 로드
load_dotenv()

st.set_page_config(page_title="AI 채팅 챗봇", page_icon="💬")
st.title("💬 OpenAI 채팅 (대화 세션 목록 지원)")

# ==========================================
# 1. SQLite 데이터베이스 관리 함수들
# ==========================================

DB_FILE = "chat_history.db"

def init_database():
    """데이터베이스 파일 및 세션별 대화 저장 테이블 생성"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            session_title TEXT,
            role TEXT,
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def get_all_sessions():
    """DB에 저장된 대화 세션 목록 가져오기 (최신순)"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT session_id, session_title, MAX(created_at) as last_time
        FROM messages
        GROUP BY session_id, session_title
        ORDER BY last_time DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    
    sessions = []
    for row in rows:
        sessions.append({"id": row[0], "title": row[1]})
    return sessions


def load_messages_by_session(session_id):
    """선택한 세션의 대화 내역 불러오기"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT role, content FROM messages WHERE session_id = ? ORDER BY id ASC", (session_id,))
    rows = cursor.fetchall()
    conn.close()
    
    saved_messages = []
    for row in rows:
        saved_messages.append({"role": row[0], "content": row[1]})
    return saved_messages


def save_message_to_db(session_id, session_title, role, content):
    """새 메시지를 세션 정보와 함께 DB에 저장"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    text_to_save = content if isinstance(content, str) else "[이미지 첨부 메시지]"
    
    cursor.execute(
        "INSERT INTO messages (session_id, session_title, role, content) VALUES (?, ?, ?, ?)",
        (session_id, session_title, role, text_to_save)
    )
    conn.commit()
    conn.close()


def delete_session_from_db(session_id):
    """선택한 대화 세션만 DB에서 삭제"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
    conn.commit()
    conn.close()


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

def start_new_chat():
    """새로운 대화 세션 시작"""
    st.session_state.current_session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    st.session_state.current_session_title = "새 대화"
    st.session_state.messages = []


def setup_sidebar():
    """사이드바 설정 (API Key, 모델, 새 대화 시작, 대화 목록 선택, 파일 첨부)"""
    with st.sidebar:
        st.header("⚙️ 설정 및 대화 목록")

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

        # 3. 새 대화 시작 및 이전 대화 목록 (ChatGPT 스타일)
        st.subheader("💬 대화 관리")

        if st.button("➕ 새 대화 시작", use_container_width=True):
            start_new_chat()
            st.rerun()

        # DB에서 저장된 대화 세션 목록 불러오기
        saved_sessions = get_all_sessions()

        if saved_sessions:
            st.write(f"📂 저장된 대화 ({len(saved_sessions)}개)")
            
            # 드롭다운에서 선택할 세션 목록
            session_titles = [s["title"] for s in saved_sessions]
            
            # 현재 선택된 세션 인덱스 찾기
            current_idx = 0
            for idx, s in enumerate(saved_sessions):
                if s["id"] == st.session_state.current_session_id:
                    current_idx = idx
                    break

            selected_title = st.selectbox(
                "대화 선택",
                options=session_titles,
                index=current_idx,
                label_visibility="collapsed"
            )

            # 선택한 세션 찾기
            target_session = saved_sessions[session_titles.index(selected_title)]

            # 버튼: 선택한 대화 불러오기 & 삭제하기
            col_load, col_del = st.columns(2)
            with col_load:
                if st.button("📥 불러오기", use_container_width=True):
                    st.session_state.current_session_id = target_session["id"]
                    st.session_state.current_session_title = target_session["title"]
                    st.session_state.messages = load_messages_by_session(target_session["id"])
                    st.rerun()

            with col_del:
                if st.button("🗑️ 삭제", use_container_width=True):
                    delete_session_from_db(target_session["id"])
                    start_new_chat()
                    st.rerun()

        st.divider()

        # 4. 이미지 및 문서 첨부
        st.subheader("📎 파일 및 이미지 첨부")

        if st.button("🖼️ 이미지 첨부 (드래그앤드롭 팝업)", use_container_width=True):
            open_image_upload_dialog()

        if "attached_image_bytes" in st.session_state and st.session_state.attached_image_bytes:
            st.image(st.session_state.attached_image_bytes, caption=f"첨부됨: {st.session_state.attached_image_name}", use_container_width=True)
            if st.button("❌ 첨부 이미지 취소", use_container_width=True):
                st.session_state.attached_image_bytes = None
                st.session_state.attached_image_type = None
                st.session_state.attached_image_name = None
                st.rerun()

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

    # 앱 구동 시 현재 세션이 없으면 새 대화 세션 생성
    if "current_session_id" not in st.session_state:
        start_new_chat()

    # 사이드바 설정 (API Key, 선택한 모델, 첨부 파일)
    api_key, selected_model, uploaded_doc = setup_sidebar()

    # 현재 대화 세션 제목 표시
    st.caption(f"📌 현재 대화: {st.session_state.current_session_title}")

    # 대화 기록 화면 출력
    display_chat_history()

    # 채팅 입력창
    user_prompt = st.chat_input("질문이나 메시지를 입력하세요...")

    if user_prompt:
        if not api_key:
            st.error("OpenAI API Key가 설정되지 않았습니다!")
            return

        # 1. 새 대화의 첫 질문일 경우, 질문 내용을 세션 제목으로 자동 지정
        if st.session_state.current_session_title == "새 대화":
            new_title = user_prompt[:25] + ("..." if len(user_prompt) > 25 else "")
            st.session_state.current_session_title = new_title

        # 2. 사용자 메시지 구성 및 DB/세션 저장
        user_content = build_user_content(user_prompt, uploaded_doc)
        st.session_state.messages.append({"role": "user", "content": user_content})
        save_message_to_db(
            st.session_state.current_session_id,
            st.session_state.current_session_title,
            "user",
            user_prompt
        )

        # 3. 화면에 사용자 메시지 즉시 표시
        with st.chat_message("user"):
            st.write(user_prompt)
            if "attached_image_bytes" in st.session_state and st.session_state.attached_image_bytes:
                st.image(st.session_state.attached_image_bytes, caption="첨부한 이미지")

        # 4. 첨부 이미지 1회 사용 후 초기화
        if "attached_image_bytes" in st.session_state:
            st.session_state.attached_image_bytes = None
            st.session_state.attached_image_type = None
            st.session_state.attached_image_name = None

        # 5. OpenAI API 호출 및 스트리밍 답변 생성
        client = OpenAI(api_key=api_key)

        with st.chat_message("assistant"):
            stream_response = client.chat.completions.create(
                model=selected_model,
                messages=st.session_state.messages,
                stream=True
            )
            full_response = st.write_stream(stream_response)

        # 6. AI 답변 DB/세션 저장
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        save_message_to_db(
            st.session_state.current_session_id,
            st.session_state.current_session_title,
            "assistant",
            full_response
        )


if __name__ == "__main__":
    main()
