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
        score_df = pd.read_excel(score_file, sheet_name=0, header=5).iloc[:33]  # 학생 점수만
        name_df = pd.read_excel(name_file, sheet_name=0, header=4)
        return score_df, name_df

    # 점수 및 이름 매칭 처리
    def prepare_data(score_df, name_df):
        data = []
        for class_num in range(1, 15):
            score_col = score_df.columns[class_num + 1]  # C열부터 시작
            scores = score_df[score_col].dropna().tolist()
            try:
                names = name_df.iloc[1:, class_num - 1].dropna().tolist()  # 1행부터 학생 이름
            except:
                names = ["이름없음"] * len(scores)

            for idx, score in enumerate(scores):
                student_number = idx + 1
                name = names[idx] if idx < len(names) else "이름없음"
                data.append({
                    "반": f"{class_num}반",
                    "점수": score,
                    "반번호": class_num,
                    "설명": f"{class_num}반 {student_number}번 {name}"
                })
        return pd.DataFrame(data)

    score_df, name_df = load_data(score_file, name_file)
    plot_df = prepare_data(score_df, name_df)

    fig = px.strip(
        plot_df,
        x="점수",
        y="반번호",
        hover_name="설명",
        orientation="h",
        stripmode="overlay",
        height=750,
        color="반",
        color_discrete_sequence=px.colors.qualitative.Vivid
    )

    fig.update_traces(jitter=0.3, marker_size=8, opacity=0.8)
    fig.update_layout(
        xaxis=dict(title="Score", range=[0, 100], showgrid=True, gridcolor="lightgray"),
        yaxis=dict(title="Class (1 to 14)", autorange="reversed"),
        title={
            "text": "2025-1 Midterm: Mathematics1",
            "x": 0.5,
            "xanchor": "center",
            "font": {"size": 24}
        },
        plot_bgcolor="white",
        margin=dict(l=60, r=40, t=60, b=60),
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("위의 두 파일을 업로드하면 그래프가 생성됩니다.")
