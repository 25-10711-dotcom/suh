import streamlit as st
import pandas as pd
from datetime import datetime

# 1. 페이지 기본 설정 및 타이틀
st.set_page_config(page_title="나만의 오운완 일지", page_icon="🏋️‍♂️", layout="centered")

# 2. 데이터 저장소 준비 (세션 상태에 기록 저장)
if "workout_records" not in st.session_state:
    st.session_state.workout_records = []

# 3. 화면 스타일 지정 (CSS)
st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #7c3aed, #4f46e5);
        padding: 30px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
    }
    .record-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #e2e8f0;
        margin-bottom: 15px;
    }
    .badge {
        background-color: #e0e7ff;
        color: #4338ca;
        padding: 4px 10px;
        border-radius: 8px;
        font-size: 0.8rem;
        font-weight: bold;
        margin-right: 10px;
    }
    .date-text {
        color: #94a3b8;
        font-size: 0.8rem;
    }
    </style>
""", unsafe_allow_html=True)

# 헤더 출력
st.markdown("""
    <div class="main-header">
        <h1 style="color: white; margin: 0; font-size: 1.8rem;">🏋️‍♂️ 오늘 운동 완료!</h1>
        <p style="color: #e0e7ff; margin: 5px 0 0 0; font-size: 0.9rem;">매일의 노력을 기록하세요</p>
    </div>
""", unsafe_allow_html=True)

# 4. 운동 입력 창 (Form)
with st.form("workout_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        date = st.date_input("날짜 선택", datetime.now())
    with col2:
        part = st.selectbox("운동 부위", ["전신 🔥", "상체(가슴/등) 📐", "하체(스쿼트) 🍗", "코어/복근 🍫", "유산소 🏃"])
        
    content = st.text_area("오늘의 운동 메모", placeholder="예: 벤치프레스 5세트, 런닝 30분 완료!")
    photo_file = st.file_uploader("인증샷 업로드 (선택)", type=["png", "jpg", "jpeg"])
    
    submit_button = st.form_submit_button("오운완 인증하기 💥", use_container_width=True)

# 5. 등록 버튼 로직
if submit_button:
    if not content.strip():
        st.error("오늘 어떤 운동을 했는지 내용을 입력해주세요!")
    else:
        photo_bytes = photo_file.read() if photo_file is not None else None
            
        new_record = {
            "id": datetime.now().timestamp(),
            "date": date.strftime("%Y-%m-%d"),
            "part": part,
            "content": content,
            "photo": photo_bytes
        }
        
        st.session_state.workout_records.insert(0, new_record)
        st.success("오늘의 오운완 기록 완료! 💪")
        st.rerun()

# 6. 저장된 기록 리스트 출력
st.markdown(f"### 나의 오운완 히스토리 (총 {len(st.session_state.workout_records)}회)", unsafe_allow_html=True)

if not st.session_state.workout_records:
    st.markdown("""
        <div style="text-align: center; padding: 40px; color: #94a3b8;">
            <p style="font-size: 2.5rem; margin-bottom: 5px;">😴</p>
            <p>아직 기록이 없습니다. 첫 운동을 기록해보세요!</p>
        </div>
    """, unsafe_allow_html=True)
else:
    for idx, rec in enumerate(st.session_state.workout_records):
        st.markdown(f"""
            <div class="record-card">
                <span class="badge">{rec['part']}</span>
                <span class="date-text">{rec['date']}</span>
                <p style="margin-top: 12px; color: #334155; white-space: pre-line; line-height: 1.5;">{rec['content']}</p>
            </div>
        """, unsafe_allow_html=True)
        
        if rec['photo']:
            st.image(rec['photo'], use_container_width=True)
            
        # ⚠️ 에러 났던 { 오타 부분을 깔끔하게 수정했습니다!
        if st.button("기록 삭제", key=f"del_{idx}"):
            st.session_state.workout_records.remove(rec)
            st.success("기록이 삭제되었습니다.")
            st.rerun()
