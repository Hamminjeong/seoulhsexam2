import streamlit as st
import pandas as pd
import plotly.express as px

# 파일 업로드
st.title("1학년 반별 점수 분포 시각화")

score_file = st.file_uploader("성적 파일 업로드 (지필평가 교과목별 일람표_2025 1학기 중간고사 공통수학1.xlsx)", type=["xlsx"])
name_file = st.file_uploader("명렬표 파일 업로드 (1학년 명렬.xlsx)", type=["xlsx"])

if score_file and name_file:

    # 데이터 로드
    def load_data(score_file, name_file):
        score_df = pd.read_excel(score_file, sheet_name=0, header=5)
        name_df = pd.read_excel(name_file, sheet_name=0, header=4)
        return score_df, name_df

    # 점수 및 이름 매칭 처리
    def prepare_data(score_df, name_df):
        data = []
        for class_num in range(1, 15):
            score_col = score_df.columns[class_num + 1]  # C열부터 시작
            scores = score_df[score_col].dropna().tolist()
            try:
                names = name_df.iloc[:, class_num - 1].dropna().tolist()
            except:
                names = ["이름없음"] * len(scores)

            for idx, score in enumerate(scores):
                student_number = idx + 1
                if idx < len(names):
                    name = names[idx]
                else:
                    name = "이름없음"
                data.append({
                    "반": f"{class_num}반",
                    "점수": score,
                    "설명": f"{class_num}반 {student_number}번 {name}"
                })
        return pd.DataFrame(data)

    score_df, name_df = load_data(score_file, name_file)
    plot_df = prepare_data(score_df, name_df)

    fig = px.strip(
        plot_df,
        x="점수",
        y="반",
        hover_name="설명",
        orientation="h",
        stripmode="overlay",
        height=700
    )

    fig.update_traces(jitter=0.3, marker_size=8)
    fig.update_layout(
        xaxis_title="점수",
        yaxis_title="반",
        title="반별 점수 분포 (마우스를 올리면 학생 정보 표시)",
    )

    st.plotly_chart(fig)

else:
    st.info("위의 두 파일을 업로드하면 그래프가 생성됩니다.")
