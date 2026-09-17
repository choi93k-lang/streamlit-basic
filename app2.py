import streamlit as st
import sqlite3
from datetime import datetime
from openai import OpenAI
from app2_history import show_history_page

# 페이지 기본 설정
st.set_page_config(page_title="AI 채팅 서비스", page_icon="💬", layout="wide")

DB_FILE = "chat_history.db"
DEFAULT_MODEL = "gpt-5.6-luna"
MAX_SESSION_TURNS = 100  # 세션당 최대 대화 수 (1회 = 질문1 + 답변1, 총 200개 메시지)
MAX_TOTAL_SESSIONS = 10  # DB에 보관할 최대 대화 세션 수


# ==========================================
# 1. SQLite 데이터베이스 관리 함수들
# ==========================================

def init_database():
    """데이터베이스 파일 및 세션별 대화 저장 테이블 생성 및 컬럼 확인"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # 기본 테이블 생성 (API Key는 절대 저장하지 않음)
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
    
    # 기존 테이블 컬럼 목록 확인 후 누락된 컬럼 자동 추가
    cursor.execute("PRAGMA table_info(messages)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if "session_id" not in columns:
        cursor.execute("ALTER TABLE messages ADD COLUMN session_id TEXT")
    if "session_title" not in columns:
        cursor.execute("ALTER TABLE messages ADD COLUMN session_title TEXT")

    conn.commit()
    conn.close()


def get_all_sessions():
    """DB에 저장된 대화 세션 목록 가져오기 (최신순, 최대 10개)"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT session_id, session_title, MAX(created_at) as last_time
        FROM messages
        GROUP BY session_id, session_title
        ORDER BY last_time DESC
        LIMIT ?
    """, (MAX_TOTAL_SESSIONS,))
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
    cursor.execute(
        "SELECT role, content FROM messages WHERE session_id = ? ORDER BY id ASC",
        (session_id,)
    )
    rows = cursor.fetchall()
    conn.close()
    
    saved_messages = []
    for row in rows:
        saved_messages.append({"role": row[0], "content": row[1]})
    return saved_messages


def save_message_to_db(session_id, session_title, role, content):
    """새 메시지를 세션 정보와 함께 DB에 저장 (API Key는 저장되지 않음)"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO messages (session_id, session_title, role, content) VALUES (?, ?, ?, ?)",
        (session_id, session_title, role, content)
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


def trim_session_messages(session_id):
    """
    한 세션당 최대 100회(질문+답변=200개 메시지)만 유지.
    200개를 초과하면 가장 오래된 메시지부터 차례대로 삭제합니다.
    """
    max_message_count = MAX_SESSION_TURNS * 2

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # 현재 세션의 전체 메시지 개수 조회
    cursor.execute("SELECT COUNT(*) FROM messages WHERE session_id = ?", (session_id,))
    total_count = cursor.fetchone()[0]
    
    if total_count > max_message_count:
        excess_count = total_count - max_message_count
        # 가장 오래된 메시지(id가 작은 것)부터 초과한 개수만큼 삭제
        cursor.execute("""
            DELETE FROM messages
            WHERE id IN (
                SELECT id FROM messages
                WHERE session_id = ?
                ORDER BY id ASC
                LIMIT ?
            )
        """, (session_id, excess_count))
        conn.commit()
        
    conn.close()


def trim_old_sessions():
    """
    저장된 대화방(세션)이 10개를 초과하면 가장 오래된 세션부터 통째로 삭제합니다.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # 세션별 마지막 대화 시간 기준 최신순 정렬
    cursor.execute("""
        SELECT session_id, MAX(created_at) as last_time
        FROM messages
        GROUP BY session_id
        ORDER BY last_time DESC
    """)
    all_sessions = cursor.fetchall()
    
    # 10개를 초과하는 오래된 세션들 추출 후 삭제
    if len(all_sessions) > MAX_TOTAL_SESSIONS:
        old_sessions = all_sessions[MAX_TOTAL_SESSIONS:]
        for session in old_sessions:
            old_session_id = session[0]
            cursor.execute("DELETE FROM messages WHERE session_id = ?", (old_session_id,))
        conn.commit()
        
    conn.close()


# ==========================================
# 2. 대화 세션 및 로그인 상태 관리 함수들
# ==========================================

def start_new_chat():
    """새로운 대화 세션 시작"""
    st.session_state.current_session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    st.session_state.current_session_title = "새 대화"
    st.session_state.messages = []


def logout_user():
    """로그아웃 처리 (브라우저 메모리에서 Key 삭제 및 화면 새로고침)"""
    st.session_state.clear()
    st.rerun()


# ==========================================
# 3. 로그인 및 보안 안내 화면
# ==========================================

def show_login_page():
    """API Key 등록 및 보안 취약점 안내를 표시하는 로그인 화면"""
    st.markdown("<h2 style='text-align: center;'>🔐 OpenAI AI 채팅 서비스 입장</h2>", unsafe_allow_html=True)
    st.write("")

    # 중앙 카드 레이아웃 구성
    col_left, col_center, col_right = st.columns([1, 2, 1])
    
    with col_center:
        # 보안 취약점에 대한 주의 안내 메시지
        st.warning("""
        ### ⚠️ 보안 주의사항 안내
        * **공개 배포 웹앱 환경**: 본 사이트는 Streamlit Community Cloud에 배포된 공개 실습용 웹 애플리케이션입니다.
        * **민감 정보 입력 금지**: 대화창에 주민등록번호, 비밀번호, 계좌 정보 등 민감한 개인정보를 절대 입력하지 마세요.
        * **API Key 안전 보관**: 입력하신 API Key는 **데이터베이스(DB)나 서버 파일에 일절 저장되지 않으며**, 오직 현재 접속한 브라우저 세션 메모리에만 임시 유지됩니다.
        * **테스트용 키 권장**: 사용 후에는 사이드바의 **[로그아웃]**을 눌러 키를 메모리에서 즉시 파기할 수 있습니다.
        """)

        st.info("💡 **안내**: 서비스를 이용하려면 본인의 OpenAI API Key가 필요합니다. Key가 없으면 채팅이 동작하지 않습니다.")

        # API Key 입력 폼
        api_key_input = st.text_input(
            "🔑 OpenAI API Key 입력",
            type="password",
            placeholder="sk-...",
            help="OpenAI 계정에서 발급받은 API Key를 입력하세요."
        )

        login_button = st.button("🚀 채팅방 입장하기", use_container_width=True, type="primary")

        if login_button:
            if not api_key_input:
                st.error("API Key를 입력해야 입장할 수 있습니다.")
            elif not api_key_input.strip().startswith("sk-"):
                st.error("올바른 OpenAI API Key 형식(sk-...)이 아닙니다.")
            else:
                # Key를 브라우저 세션 메모리에만 보관 (DB 영구 저장 안 함)
                st.session_state["api_key"] = api_key_input.strip()
                st.session_state["is_logged_in"] = True
                start_new_chat()
                st.rerun()


# ==========================================
# 4. 화면 UI 및 사이드바 함수
# ==========================================

def setup_sidebar():
    """사이드바 설정 (Key 상태, 로그아웃, AI 모델, 새 대화 시작, 이전 대화 목록)"""
    with st.sidebar:
        st.header("⚙️ 설정 및 대화 목록")

        # 1. API Key 등록 상태 표시 (뒷 4자리만 마스킹 노출)
        user_key = st.session_state.get("api_key", "")
        if user_key:
            masked_key = user_key[:7] + "..." + user_key[-4:]
            st.success(f"🔑 Key 등록됨: `{masked_key}`")
        
        if st.button("🚪 로그아웃 (Key 파기)", use_container_width=True):
            logout_user()

        st.divider()

        # 2. 최신 AI 모델 선택 (기본값: gpt-5.6-luna)
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
            help="기본 모델은 빠르고 경제적인 gpt-5.6-luna 입니다."
        )

        st.divider()

        # 3. 새 대화 시작 및 이전 대화 목록 (최대 10개 보관)
        st.subheader("💬 대화 목록 (최대 10개)")

        if st.button("➕ 새 대화 시작", use_container_width=True):
            start_new_chat()
            st.rerun()

        # DB에서 저장된 최근 대화 세션 목록 불러오기
        saved_sessions = get_all_sessions()

        if saved_sessions:
            st.write(f"📂 저장된 대화 ({len(saved_sessions)}개)")
            
            session_titles = [s["title"] for s in saved_sessions]
            
            current_idx = 0
            for idx, s in enumerate(saved_sessions):
                if s["id"] == st.session_state.get("current_session_id"):
                    current_idx = idx
                    break

            selected_title = st.selectbox(
                "대화 선택",
                options=session_titles,
                index=current_idx,
                label_visibility="collapsed"
            )

            target_session = saved_sessions[session_titles.index(selected_title)]

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

        return selected_model


def display_chat_history():
    """순수 텍스트 대화 내역 화면 렌더링"""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])


# ==========================================
# 5. 메인 채팅 페이지 실행 로직
# ==========================================

def show_chat_page():
    # DB 초기화
    init_database()

    # 1. 로그인 여부 확인 (Key가 없으면 로그인 화면 출력 후 중단)
    if not st.session_state.get("is_logged_in") or not st.session_state.get("api_key"):
        show_login_page()
        return

    # 2. 앱 구동 시 현재 세션이 없으면 새 대화 세션 생성
    if "current_session_id" not in st.session_state:
        start_new_chat()

    # 3. 사이드바 설정
    selected_model = setup_sidebar()

    st.title("💬 OpenAI 채팅 (대화 세션 목록 지원)")

    # 현재 대화 세션 제목 및 턴 수 표시 (1턴 = 질문1 + 답변1)
    turn_count = len(st.session_state.messages) // 2
    st.caption(f"📌 **현재 대화:** {st.session_state.current_session_title} | 🔄 **대화 턴:** {turn_count}/{MAX_SESSION_TURNS}회 (100회 초과 시 가장 오래된 대화부터 자동 삭제)")

    # 대화 기록 화면 출력
    display_chat_history()

    # 채팅 입력창
    user_prompt = st.chat_input("질문이나 메시지를 입력하세요...")

    if user_prompt:
        # 첫 질문일 경우 세션 제목 자동 지정
        if st.session_state.current_session_title == "새 대화":
            new_title = user_prompt[:25] + ("..." if len(user_prompt) > 25 else "")
            st.session_state.current_session_title = new_title

        # 사용자 메시지 세션 및 DB 저장
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        save_message_to_db(
            st.session_state.current_session_id,
            st.session_state.current_session_title,
            "user",
            user_prompt
        )

        # 화면에 사용자 메시지 즉시 표시
        with st.chat_message("user"):
            st.write(user_prompt)

        # 세션 메모리에 임시 보관된 사용자 Key를 사용하여 OpenAI API 호출
        client = OpenAI(api_key=st.session_state["api_key"])

        with st.chat_message("assistant"):
            stream_response = client.chat.completions.create(
                model=selected_model,
                messages=st.session_state.messages,
                stream=True
            )
            full_response = st.write_stream(stream_response)

        # AI 답변 세션 및 DB 저장
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        save_message_to_db(
            st.session_state.current_session_id,
            st.session_state.current_session_title,
            "assistant",
            full_response
        )

        # 세션당 대화 수 제한(최대 100회) 및 전체 세션 수 제한(최대 10개) 적용
        trim_session_messages(st.session_state.current_session_id)
        trim_old_sessions()

        # 세션 상태의 messages 목록도 DB와 동일하게 최신 200개로 동기화
        if len(st.session_state.messages) > MAX_SESSION_TURNS * 2:
            st.session_state.messages = st.session_state.messages[-(MAX_SESSION_TURNS * 2):]


# ==========================================
# 6. 다중 페이지 내비게이션 실행
# ==========================================

chat_page = st.Page(show_chat_page, title="AI 채팅방", icon="💬", default=True)
history_page = st.Page(show_history_page, title="과거 채팅 내역 보관소", icon="📜")

pg = st.navigation([chat_page, history_page])
pg.run()
