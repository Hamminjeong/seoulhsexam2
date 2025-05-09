import streamlit as st
import pandas as pd
import plotly.express as px

st.title("2025-1 Midterm: Mathematics1")

# 엑셀 파일 업로드
uploaded_file = st.file_uploader("성적 엑셀 파일을 업로드하세요", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file, sheet_name=0)

    plot_data = []

    for class_idx in range(14):  # 1반 ~ 14반
        class_num = class_idx + 1
        col_index = 2 + class_idx  # C열부터 시작하므로 index=2
        scores = df.iloc[7:34, col_index]  # C9:C35 → index 7~33

        for row_offset, score in enumerate(scores):
            student_number = row_offset + 1  # 1번부터 시작
            try:
                score = float(score)
                label = f"[{class_num}반 {student_number}번]"
                plot_data.append({
                    "Class": class_num,
                    "StudentNo": student_number,
                    "Score": score,
                    "Label": label
                })
            except:
                continue  # NaN, '자퇴' 등 처리 불가 항목은 건너뜀

    # 시각화
    df_plot = pd.DataFrame(plot_data)
    fig = px.scatter(
        df_plot,
        x="Score",
        y="Class",
        hover_name="Label",
        title="2025-1 Midterm: Mathematics1",
        labels={"Score": "Score", "Class": "Class"}
    )
    fig.update_yaxes(autorange="reversed")  # 1반이 위로

    st.plotly_chart(fig)
