import streamlit as st
import plotly.express as px
import pandas as pd

st.title("2025-1 중간고사 성적 시각화 (공통수학1)")

st.markdown("""
이 앱은 업무시스템에서 다운로드한 **지필평가 성적표**와 **1학년 명렬표**를 이용해
학생 개별 점수를 시각화해 줍니다. 각 점 위에 마우스를 올리면
`[반 번호 번 이름]` 형식으로 학생 정보를 확인할 수 있습니다.

**사용 방법:**
1. 성적 엑셀 파일 (.xlsx)을 업로드하세요.
2. 명렬표 엑셀 파일 (.xlsx)을 업로드하세요.
3. 시각화 결과를 확인하세요!
""")

# 파일 업로드
score_file = st.file_uploader("성적 엑셀 파일 (.xlsx)", type="xlsx", key="score")
name_file = st.file_uploader("명렬표 엑셀 파일 (.xlsx)", type="xlsx", key="name")

if score_file and name_file:
    score_df = pd.read_excel(score_file, sheet_name=0)
    name_df = pd.read_excel(name_file, sheet_name='학년별명렬')
    name_data = name_df.iloc[4:, 1:15].reset_index(drop=True)

    class_count = 14
    plot_data = []

    for class_idx in range(class_count):
        class_num = class_idx + 1
        col_index = 2 + class_idx  # C열부터
        scores = score_df.iloc[7:34, col_index]

        for row_offset, score in enumerate(scores):
            student_number = row_offset + 1
            try:
                score = float(score)
                student_name = name_data.iloc[row_offset, class_idx]
                label = f"[{class_num}반 {student_number}번 {student_name}]"
                plot_data.append({
                    "Class": class_num,
                    "StudentNo": student_number,
                    "Score": score,
                    "Label": label
                })
            except:
                continue

    df = pd.DataFrame(plot_data)

    fig = px.scatter(
        df,
        x="Score",
        y="Class",
        hover_name="Label",
        title="2025-1 Midterm: Mathematics1",
        labels={"Score": "Score", "Class": "Class"}
    )
    fig.update_yaxes(autorange="reversed")
    st.plotly_chart(fig)
else:
    st.info("두 개의 엑셀 파일을 모두 업로드해 주세요.")
