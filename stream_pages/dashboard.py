import streamlit as st
import pandas as pd

def show_dashboard():
    """간단한 과일 판매 데이터 표와 차트를 표시하는 대시보드 화면입니다."""
    st.title("📊 과일 판매 대시보드")
    st.write("Streamlit의 데이터프레임과 기본 차트 컴포넌트를 활용한 화면입니다.")
    st.divider()
    
    # 초보자가 이해하기 쉬운 단순한 딕셔너리 데이터
    sales_data = {
        "과일": ["사과", "바나나", "오렌지", "포도", "딸기"],
        "판매량": [120, 85, 95, 60, 150]
    }
    
    df = pd.DataFrame(sales_data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 판매 현황 표")
        st.dataframe(df, use_container_width=True)
        
    with col2:
        st.subheader("📈 판매량 막대 차트")
        st.bar_chart(df.set_index("과일"))

show_dashboard()
