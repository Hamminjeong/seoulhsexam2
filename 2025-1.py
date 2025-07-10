import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(layout="wide")

# 파일 업로드
uploaded_file = st.file_uploader("엑셀 파일을 업로드하세요", type=["xlsx"])

if uploaded_file:
    xls = pd.ExcelFile(uploaded_file)

    # 시트 불러오기
    midterm_df = xls.parse("중간고사", header=None)
    final_df = xls.parse("기말고사", header=None)

    def extract_scores(df, exam_name):
        반정보 = df.iloc[0, 1:15].values  # B1:O1
        번호정보 = df.iloc[1:32, 0].values  # A2:A32
        점수 = df.iloc[1:32, 1:15].values  # B2:O32

        data = []
        for i in range(31):  # 학생 수 (행)
            for j in range(14):  # 과목 수 또는 열
                value = 점수[i][j]
                if isinstance(value, (int, float, np.integer, np.floating)):
                    학번 = f"{반정보[j]}반 {번호정보[i]}번"
                    data.append({
                        "학번": 학번,
                        "점수": float(value),
                        "반": 반정보[j],
                        "번호": 번호정보[i],
                        "시험": exam_name
                    })
        return pd.DataFrame(data)

    # 데이터프레임 생성
    df_mid = extract_scores(midterm_df, "중간고사")
    df_final = extract_scores(final_df, "기말고사")

    # 중간고사 히스토그램
    st.subheader("📊 중간고사 점수 히스토그램 (급간 1)")
    fig_mid = px.histogram(
        df_mid,
        x="점수",
        nbins=100,
        hover_data=["학번"],
        title="중간고사 점수 분포"
    )
    st.plotly_chart(fig_mid, use_container_width=True)

    # 기말고사 히스토그램
    st.subheader("📊 기말고사 점수 히스토그램 (급간 1)")
    fig_final = px.histogram(
        df_final,
        x="점수",
        nbins=100,
        hover_data=["학번"],
        title="기말고사 점수 분포"
    )
    st.plotly_chart(fig_final, use_container_width=True)

    # 중간 vs 기말 산포도용 병합
    st.subheader("📈 중간고사 vs 기말고사 산포도 (학번 툴팁 포함)")
    df_merged = pd.merge(df_mid, df_final, on=["반", "번호"], suffixes=("_중간", "_기말"))
    fig_scatter = px.scatter(
        df_merged,
        x="점수_중간",
        y="점수_기말",
        hover_data={"학번_중간": True},
        labels={"점수_중간": "중간고사", "점수_기말": "기말고사"},
        title="중간고사 vs 기말고사 산포도"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
