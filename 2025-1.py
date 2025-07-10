import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(layout="wide")

GRADE_FILE_PATH = "data/지필평가 교과목별 일람표_2025 1학기 공통수학1.xlsx"
NAME_FILE_PATH = "data/1학년 명렬.xlsx"


# 엑셀 파일 로드
@st.cache_data
def load_excel_data():
    xls_grade = pd.ExcelFile(GRADE_FILE_URL)
    xls_name = pd.ExcelFile(NAME_FILE_URL)

    df_midterm = xls_grade.parse("중간고사", header=None)
    df_final = xls_grade.parse("기말고사", header=None)
    df_names = xls_name.parse(0, header=None)
    return df_midterm, df_final, df_names

df_midterm, df_final, df_names = load_excel_data()

# 이름 매칭용 dict 생성
def build_name_map(df):
    name_map = {}
    for row in df.itertuples(index=False):
        반, 번호, 이름 = row[:3]
        key = (int(반), int(번호))
        name_map[key] = 이름
    return name_map

name_map = build_name_map(df_names)

# 점수 데이터 정제
def extract_scores(df, exam_name):
    반정보 = df.iloc[0, 1:15].values  # B1:O1
    번호정보 = df.iloc[1:32, 0].values  # A2:A32
    점수 = df.iloc[1:32, 1:15].values  # B2:O32

    data = []
    for i in range(31):  # 31명
        for j in range(14):  # 14열
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

# 히스토그램: 중간고사
st.subheader("📊 중간고사 점수 히스토그램 (급간 1)")
fig_mid = px.histogram(
    df_mid,
    x="점수",
    nbins=100,
    hover_data=["학번"],
    title="중간고사 점수 분포"
)
st.plotly_chart(fig_mid, use_container_width=True)

# 히스토그램: 기말고사
st.subheader("📊 기말고사 점수 히스토그램 (급간 1)")
fig_final = px.histogram(
    df_final,
    x="점수",
    nbins=100,
    hover_data=["학번"],
    title="기말고사 점수 분포"
)
st.plotly_chart(fig_final, use_container_width=True)

# 산포도: 중간 vs 기말
st.subheader("📈 중간고사 vs 기말고사 산포도 (O반 O번 이름 툴팁 포함)")
df_merged = pd.merge(df_mid, df_final, on=["반", "번호"], suffixes=("_중간", "_기말"))
df_merged["학번표시"] = df_merged["학번_중간"]  # hover에 표시할 학번 이름

fig_scatter = px.scatter(
    df_merged,
    x="점수_중간",
    y="점수_기말",
    hover_data={"학번표시": True},
    labels={"점수_중간": "중간고사", "점수_기말": "기말고사"},
    title="중간고사 vs 기말고사 산포도"
)
st.plotly_chart(fig_scatter, use_container_width=True)
