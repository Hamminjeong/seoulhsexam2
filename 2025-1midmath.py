import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

st.title("2025학년도 학생 성적 반별 분포표")

st.markdown("""
이 앱은 업무시스템에서 다운로드한 **지필평가 성적표**와 **1학년 명렬표**를 이용해 반별 성적 분포도를 제공합니다.
\n[성적 엑셀 파일] 받는 법: 나이스-지필평가조회-교과목별일람표조회-전체학급 
\n -한페이지출력에 체크, 엑셀파일 저장. 이때 일부 열을 삭제하여, 각 반이 하나의 열만 차지하도록 해주세요. (서울고 기준 F,K,M,P,U 열 삭제)
\n[명렬표 엑셀 파일]은 2행에 반, A열에 번, B6칸에 1반 1번 학생이 위치하게 해주세요.

**사용 방법:**
1. 성적 엑셀 파일 (.xlsx)을 업로드하세요.
2. 명렬표 엑셀 파일 (.xlsx)을 업로드하세요.
3. 시각화 결과를 확인하세요! 마우스 커서를 올리면 학생명을 확인할 수 있습니다.
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
        col_index = 2 + class_idx  # C열부터 시작
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

    # 반별 파스텔톤 색상 정의
    pastel_colors = {
        1: '#AEC6CF', 2: '#FFB347', 3: '#77DD77',
        4: '#CBAACB', 5: '#FFD1DC', 6: '#FFFACD',
        7: '#B0E0E6', 8: '#F5DEB3', 9: '#D8BFD8',
        10: '#E0BBE4', 11: '#FFDAC1', 12: '#C1E1C1',
        13: '#B5EAD7', 14: '#FF9AA2'
    }
    df["Color"] = df["Class"].map(pastel_colors)

    # 그래프 생성
    fig = go.Figure()

    # 산점도 추가
    fig.add_trace(go.Scatter(
        x=df["Score"],
        y=df["Class"],
        mode="markers",
        marker=dict(color=df["Color"], size=10, opacity=0.7),
        text=df["Label"],
        hoverinfo="text",
        name="학생 점수"
    ))

    # 상자그림 추가
    for c in sorted(df["Class"].unique()):
        class_df = df[df["Class"] == c]
        if len(class_df) >= 3:  # boxplot은 최소 3명 필요
            fig.add_trace(go.Box(
                y=[c] * len(class_df),
                x=class_df["Score"],
                name=f"{c}반",
                marker_color=pastel_colors[c],
                boxpoints='outliers',
                opacity=0.3,
                line=dict(width=1),
                showlegend=False,
                orientation='h'
            ))

    # 레이아웃 조정 (흐린 가로선 포함)
    fig.update_yaxes(
        tickmode="linear",
        dtick=1,
        autorange="reversed",
        gridcolor="lightgray",
        gridwidth=0.5
    )
    fig.update_layout(
        title="2025-1학기 수학 중간고사: 산점도 + 반별 상자그림",
        xaxis_title="점수",
        yaxis_title="반",
        height=700
    )

    st.plotly_chart(fig)

else:
    st.info("두 개의 엑셀 파일을 모두 업로드해 주세요.")
