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

score\_file = st.file\_uploader("📄 성적 엑셀 파일 업로드", type=\["xlsx"], key="score")
name\_file = st.file\_uploader("📄 1학년 명렬표 업로드", type=\["xlsx"], key="name")

class\_col\_map = {
1: 2,  2: 3,  3: 4,  4: 6,
5: 7,  6: 8,  7: 9,  8: 11,
9: 13, 10: 15, 11: 16, 12: 17,
13: 18, 14: 19
}

if score\_file and name\_file:
score\_df = pd.read\_excel(score\_file, header=None)
name\_df = pd.read\_excel(name\_file, sheet\_name='학년별명렬')
name\_data = name\_df.iloc\[4:, 1:15].reset\_index(drop=True)

```
combined_data = []

for class_num, col_idx in class_col_map.items():
    scores = score_df.iloc[7:34, col_idx]
    for i, val in enumerate(scores):
        student_no = i + 1
        try:
            score = float(val)
            student_name = name_data.iloc[i, class_num - 1]
            label = f"[{class_num}반 {student_no}번 {student_name}]"
            combined_data.append({
                "Class": class_num,
                "StudentNo": student_no,
                "Score": score,
                "Label": label
            })
        except:
            continue

df = pd.DataFrame(combined_data)

# 산점도
fig = px.scatter(
    df,
    x="Score",
    y="Class",
    hover_name="Label",
    color=df["Class"].astype(str),
    color_discrete_sequence=px.colors.qualitative.Pastel,
    title="2025-1 Midterm: Mathematics1",
    labels={"Score": "Score", "Class": "Class"}
)
fig.update_yaxes(autorange="reversed")
st.plotly_chart(fig)

# 상자그림
fig_box = px.box(
    df,
    x="Class",
    y="Score",
    points="all",
    hover_name="Label",
    color=df["Class"].astype(str),
    color_discrete_sequence=px.colors.qualitative.Pastel,
    title="반별 점수 분포 (Box Plot)"
)
st.plotly_chart(fig_box)

st.markdown("""
**📊 상자그림(Box Plot)의 의미**

- **중앙값(2사분위수)**: 상자의 가로줄 — 전체 점수 중간값
- **1사분위수~3사분위수 (Q1~Q3)**: 상자의 아래쪽과 위쪽 — 점수의 중간 50% 범위
- **수염(Whiskers)**: 일반적인 범위 내의 최소/최대값
- **점으로 찍힌 값들**: 이상치(너무 높거나 낮은 특이 점수)

이 그래프를 통해 각 반의 점수 분포가 **고르게 분포되어 있는지**, **극단적인 점수가 있는지**,
**중간값이 높은 반은 어디인지** 등을 한눈에 비교할 수 있습니다.
""")
```

else:
st.info("두 개의 엑셀 파일을 모두 업로드해 주세요.")
