import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(layout="wide")

# GitHub의 엑셀 파일 경로 (사용자에 맞게 수정하세요)
GITHUB_BASE_URL = "https://raw.githubusercontent.com/Hamminjeong/seoulhsexam2/edit/main/"
GRADE_FILE_URL = GITHUB_BASE_URL + "지필평가 교과목별 일람표_2025 1학기 공통수학1.xlsx"
NAME_FILE_URL = GITHUB_BASE_URL + "1학년 명렬.xlsx"

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
