import streamlit as st
import pandas as pd
import plotly.express as px

st.title("2025-1 Midterm: 성적 시각화 (이름 포함)")

score_file = st.file_uploader("📄 성적 엑셀 파일 업로드", type=["xlsx"], key="score")
name_file = st.file_uploader("📄 1학년 명렬표 업로드", type=["xlsx"], key="name")

# 반별 실제 열 인덱스 (0-based)
class_col_map = {
    1: 2,  2: 3,  3: 4,  4: 6,
    5: 7,  6: 8,  7: 9,  8: 11,
    9: 13, 10: 15, 11: 16, 12: 17,
    13: 18, 14: 19
}

if score_file and name_file:
    score_df = pd.read_excel(score_file, header=None)
    name_df = pd.read_excel(name_file, sheet_name='학년별명렬')
    name_data = name_df.iloc[4:, 1:15].reset_index(drop=True)

    combined_data = []

    for class_num, col_idx in class_col_map.items():
        scores = score_df.iloc[7:34, col_idx]
        for row_offset, val in enumerate(scores):
            student_no = row_offset + 1
            try:
                score = float(val)
                student_name = name_data.iloc[row_offset, class_num - 1]
                label = f"[{class_num}반 {student_no}번 {student_name}]"
                combined_data.append({
                    "Class": class_num,
                    "StudentNo": student_no,
                    "Score": score,
                    "Label": label
                })
            except:
                continue

    df = pd.DataFrame(combined_data)

    fig = px.scatter(
        df,
        x="Score",
        y="Class",
        hover_name="Label",
        title="2025-1 Midterm: Mathematics1 (with Names)",
        labels={"Score": "Score", "Class": "Class"}
    )
    fig.update_yaxes(autorange="reversed")
    st.plotly_chart(fig)

else:
    st.info("위의 두 개 엑셀 파일을 모두 업로드해 주세요.")
