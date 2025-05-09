import streamlit as st
import pandas as pd
import plotly.express as px

st.title("2025-1 Midterm: 성적 시각화 (공통수학1)")

uploaded_file = st.file_uploader("📄 업무시스템 엑셀 파일 업로드", type=["xlsx"])

# 병합 반 리스트 (2칸 차지하는 반 번호)
merged_class_cols = {3: 3, 7: 8, 8: 10, 10: 12}  # 반: 사용 열 index (1부터 시작)
# 일반 반: 1~14에서 제외된 것들
normal_class_cols = {c: 2 + (c - 1) for c in range(1, 15) if c not in merged_class_cols}

# 병합 반은 가운데 열만 선택
merged_class_cols.update({k: v for k, v in merged_class_cols.items()})

if uploaded_file:
    df = pd.read_excel(uploaded_file, header=None)
    score_data = []

    for class_num in range(1, 15):
        if class_num in merged_class_cols:
            col_idx = merged_class_cols[class_num]
        else:
            col_idx = normal_class_cols[class_num]

        scores = df.iloc[7:34, col_idx]  # 27명 (C8:C34)
        for row_offset, val in enumerate(scores):
            student_no = row_offset + 1
            try:
                score = float(val)
                label = f"[{class_num}반 {student_no}번]"
                score_data.append({
                    "Class": class_num,
                    "StudentNo": student_no,
                    "Score": score,
                    "Label": label
                })
            except:
                continue

    result_df = pd.DataFrame(score_data)

    fig = px.scatter(
        result_df,
        x="Score",
        y="Class",
        hover_name="Label",
        title="2025-1 Midterm: Mathematics1",
        labels={"Score": "Score", "Class": "Class"}
    )
    fig.update_yaxes(autorange="reversed")
    st.plotly_chart(fig)
