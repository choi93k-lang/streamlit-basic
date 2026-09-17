import streamlit as st
import sqlite3
import pandas as pd
import os

st.set_page_config(page_title="채팅 기록 보관소", page_icon="📜", layout="wide")
st.title("📜 과거 채팅 내역 보관소")

DB_FILE = "chat_history.db"

# ==========================================
# 1. 데이터베이스 조회 함수들
# ==========================================

def check_db_exists():
    """DB 파일 및 테이블 존재 여부 확인"""
    if not os.path.exists(DB_FILE):
        return False
    return True


def get_chat_statistics():
    """전체 세션 수와 메시지 개수 통계 반환"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # 총 메시지 수
    cursor.execute("SELECT COUNT(*) FROM messages")
    total_messages = cursor.fetchone()[0]
    
    # 총 세션(대화방) 수
    cursor.execute("SELECT COUNT(DISTINCT session_id) FROM messages")
    total_sessions = cursor.fetchone()[0]
    
    conn.close()
    return total_sessions, total_messages


def get_all_sessions():
    """저장된 모든 대화 세션 목록 조회"""
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
        sessions.append({
            "id": row[0],
            "title": row[1] if row[1] else "제목 없는 대화",
            "date": row[2]
        })
    return sessions


def get_messages_by_session(session_id):
    """특정 세션의 모든 메시지 조회"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT role, content, created_at
        FROM messages
        WHERE session_id = ?
        ORDER BY id ASC
    """, (session_id,))
    rows = cursor.fetchall()
    conn.close()
    
    messages = []
    for row in rows:
        messages.append({
            "role": row[0],
            "content": row[1],
            "created_at": row[2]
        })
    return messages


def search_messages(keyword):
    """키워드가 포함된 메시지 검색"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT session_title, role, content, created_at
        FROM messages
        WHERE content LIKE ?
        ORDER BY id DESC
    """, (f"%{keyword}%",))
    rows = cursor.fetchall()
    conn.close()
    
    results = []
    for row in rows:
        results.append({
            "대화 제목": row[0],
            "역할": "사용자" if row[1] == "user" else "AI 어시스턴트",
            "내용": row[2],
            "작성 일시": row[3]
        })
    return results


def get_all_messages_as_dataframe():
    """전체 메시지 내역을 데이터프레임으로 변환"""
    conn = sqlite3.connect(DB_FILE)
    query = """
        SELECT id as 번호, session_id as 세션ID, session_title as 대화제목, 
               role as 역할, content as 내용, created_at as 일시
        FROM messages
        ORDER BY id DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


# ==========================================
# 2. 화면 UI 렌더링
# ==========================================

def main():
    if not check_db_exists():
        st.info("아직 저장된 대화 기록(`chat_history.db`)이 없습니다. app2.py에서 먼저 대화를 나눠보세요!")
        return

    # 1. 상단 통계 지표
    total_sessions, total_messages = get_chat_statistics()
    col_stat1, col_stat2 = st.columns(2)
    col_stat1.metric("총 대화 세션", f"{total_sessions}개")
    col_stat2.metric("총 메시지 수", f"{total_messages}개")

    st.divider()

    # 2. 탭으로 뷰 분리
    tab_session_view, tab_search_view, tab_table_view = st.tabs([
        "💬 대화방별 상세 보기",
        "🔍 키워드 검색",
        "📋 전체 데이터 표"
    ])

    # --- 탭 1: 대화방별 상세 보기 ---
    with tab_session_view:
        sessions = get_all_sessions()
        
        if not sessions:
            st.info("저장된 대화가 없습니다.")
        else:
            # 드롭다운 옵션 레이블 생성
            session_options = {s["id"]: f"{s['title']} ({s['date']})" for s in sessions}
            
            selected_session_id = st.selectbox(
                "확인할 대화방을 선택하세요",
                options=list(session_options.keys()),
                format_func=lambda sid: session_options[sid]
            )

            # 선택한 대화방의 메시지 렌더링
            messages = get_messages_by_session(selected_session_id)
            st.caption(f"총 {len(messages)}개의 메시지가 있습니다.")

            for msg in messages:
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])
                    st.caption(f"🕒 {msg['created_at']}")

    # --- 탭 2: 키워드 검색 ---
    with tab_search_view:
        search_keyword = st.text_input("검색할 단어를 입력하세요", placeholder="예: 파이썬, 날씨, 이미지")
        
        if search_keyword:
            search_results = search_messages(search_keyword)
            st.write(f"검색 결과: **{len(search_results)}**건")
            
            if search_results:
                df_results = pd.DataFrame(search_results)
                st.dataframe(df_results, use_container_width=True)
            else:
                st.warning("해당 키워드가 포함된 대화 내용이 없습니다.")

    # --- 탭 3: 전체 데이터 표 ---
    with tab_table_view:
        df_all = get_all_messages_as_dataframe()
        st.write(f"전체 메시지 목록 ({len(df_all)}건)")
        st.dataframe(df_all, use_container_width=True)


if __name__ == "__main__":
    main()
