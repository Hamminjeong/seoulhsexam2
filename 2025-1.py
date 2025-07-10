import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(layout="wide")
st.title("📊 중간고사/기말고사 성적 분석")

# 파일 업로드
grade_file = st.file_uploader("📝 지필평가 성적 엑셀 파일 업로드", type="xlsx")
name_file = st.file_uploader("🧑‍🎓 1학년 명렬표 엑셀 파일 업로드", type="xlsx")

if grade_file and name_file:
    # 엑셀 로드
    xls_grade = pd.ExcelFile(grade_file)
    xls_name = pd.ExcelFile(name_file)

    df_midterm = xls_grade.parse("중간고사", header=None)
    df_final = xls_grade.parse("기말고사", header=None)
    df_names = xls_name.parse(0, header=None)

    # 이름 매핑
    def build_name_map(df):
        name_map = {}
        for row in df.itertuples(index=False):
            반, 번호, 이름 = row[:3]
            key = (int(반), int(번호))
            name_map[key] = 이름
        return name_map

    name_map = build_name_map(df_names)

    # 성적 추출
    def extract_scores(df, exam_name):
        반정보 = df.iloc[0, 1:15].values
        번호정보 = df.iloc[1:32, 0].values
        점수 = df.iloc[1:32, 1:15].values

        data = []
        for i in range(31):
            for j in range(14):
                value = 점수[i][j]
                if isinstance(value, (int, float, np.integer, np.floating)):
                    반 = int(반정보[j])
                    번호 = int(번호정보[i])
                    이름 = name_map.get((반, 번호), "")
                    학번표시 = f"{반}반 {번호}번 {이름}"
                    data.append({
                        "반": 반,
                        "번호": 번호,
                        "이름": 이름,
                        "학번": 학번표시,
                        "점수": float(value),
                        "시험": exam_name
                    })
        return pd.DataFrame(data)

    df_mid = extract_scores(df_midterm, "중간고사")
    df_final = extract_scores(df_final, "기말고사")

    # 병합
    df_merged = pd.merge(df_mid, df_final, on=["반", "번호"], suffixes=("_중간", "_기말"))
    df_merged["학번"] = df_merged["학번_중간"]

    # 📊 히스토그램
    st.subheader("📊 중간고사 점수 히스토그램")
    st.plotly_chart(px.histogram(df_mid, x="점수", nbins=100, hover_data=["학번"]), use_container_width=True)

    st.subheader("📊 기말고사 점수 히스토그램")
    st.plotly_chart(px.histogram(df_final, x="점수", nbins=100, hover_data=["학번"]), use_container_width=True)

    # 🎚️ 슬라이더
    st.subheader("📈 중간 vs 기말 산포도 + x+y=n 직선")
    n = st.slider("n 값을 선택하세요 (x+y=n)", min_value=0, max_value=200, value=100)

    df_merged["합"] = df_merged["점수_중간"] + df_merged["점수_기말"]
    count_all = len(df_merged)
    count_above = (df_merged["합"] > n).sum()
    rate = round(100 * count_above / count_all, 2) if count_all > 0 else 0

    fig = px.scatter(
        df_merged,
        x="점수_중간",
        y="점수_기말",
        hover_data=["학번"],
        labels={"점수_중간": "중간고사", "점수_기말": "기말고사"},
        title=f"x + y > {n} 인 학생 비율: {rate}%"
    )

    # 직선 추가 (x + y = n ⇒ y = n - x)
    fig.add_shape(
        type="line",
        x0=0, y0=n, x1=n, y1=0,
        line=dict(color="red", width=2, dash="dash"),
        name="x + y = n"
    )

    st.plotly_chart(fig, use_container_width=True)
