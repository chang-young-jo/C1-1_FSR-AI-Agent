import pandas as pd

file_path = "FSR_2010.01_1,082.xlsx"

df = pd.read_excel(file_path)

# AI Agent에서 사용할 핵심 컬럼 후보
selected_columns = [
    "FSR문서번호",
    "접수일",
    "실적월",
    "제품군",
    "기종명",
    "기종",
    "호기",
    "설치고객사명",
    "거점",
    "클레임 구분",
    "현상(대)",
    "현상(중)",
    "현상(소)",
    "접수내용",
    "기술비용",
    "합계비용"
]

print("원본 데이터")
print("행 개수:", len(df))
print("열 개수:", len(df.columns))

print("\n선택 컬럼 존재 여부")
for column in selected_columns:
    if column in df.columns:
        print(f"[OK] {column}")
    else:
        print(f"[없음] {column}")

# 실제 존재하는 컬럼만 선택
available_columns = [
    column for column in selected_columns
    if column in df.columns
]

fsr_df = df[available_columns].copy()

print("\n분석용 데이터")
print("행 개수:", len(fsr_df))
print("열 개수:", len(fsr_df.columns))

print("\n컬럼별 유효 데이터 / 결측치")
for column in fsr_df.columns:
    valid_count = fsr_df[column].notna().sum()
    missing_count = fsr_df[column].isna().sum()
    valid_rate = valid_count / len(fsr_df) * 100

    print(
        f"{column}: "
        f"유효 {valid_count}건 / "
        f"결측 {missing_count}건 / "
        f"유효율 {valid_rate:.1f}%"
    )


# --------------------------------------------------
# 데이터 전처리
# --------------------------------------------------

# 1. 분류형 데이터의 결측값 처리
category_columns = [
    "제품군",
    "기종명",
    "기종",
    "호기",
    "설치고객사명",
    "거점",
    "클레임 구분",
    "현상(대)",
    "현상(중)",
    "현상(소)"
]

for column in category_columns:
    if column in fsr_df.columns:
        fsr_df[column] = fsr_df[column].fillna("미분류")


# 2. 접수내용 결측값 처리
if "접수내용" in fsr_df.columns:
    fsr_df["접수내용"] = fsr_df["접수내용"].fillna("내용 없음")


# 3. 날짜 데이터 변환
if "접수일" in fsr_df.columns:
    fsr_df["접수일"] = pd.to_datetime(
        fsr_df["접수일"].astype(str).str.replace(".0", "", regex=False),
        format="%Y%m%d",
        errors="coerce"
    )

# 4. 비용 데이터 숫자형 변환
cost_columns = [
    "기술비용",
    "합계비용"
]

for column in cost_columns:
    if column in fsr_df.columns:
        fsr_df[column] = pd.to_numeric(
            fsr_df[column],
            errors="coerce"
        ).fillna(0)


# --------------------------------------------------
# 전처리 결과 확인
# --------------------------------------------------

print("\n==============================")
print("FSR 데이터 전처리 완료")
print("==============================")

print("총 데이터:", len(fsr_df), "건")

if "접수일" in fsr_df.columns:
    print("최초 접수일:", fsr_df["접수일"].min())
    print("최종 접수일:", fsr_df["접수일"].max())

if "제품군" in fsr_df.columns:
    print("\n제품군별 FSR")
    print(fsr_df["제품군"].value_counts())

if "현상(대)" in fsr_df.columns:
    print("\n현상(대) TOP 10")
    print(fsr_df["현상(대)"].value_counts().head(10))

if "합계비용" in fsr_df.columns:
    print("\n총 합계비용:", fsr_df["합계비용"].sum())
    print("평균 합계비용:", round(fsr_df["합계비용"].mean(), 2))

# --------------------------------------------------
# AI Agent용 FSR Summary 생성
# --------------------------------------------------

summary = {
    "total_fsr": len(fsr_df)
}

# 접수일 기준
if "접수일" in fsr_df.columns:
    valid_dates = fsr_df["접수일"].dropna()

    if not valid_dates.empty:
        summary["first_received_date"] = valid_dates.min().strftime("%Y-%m-%d")
        summary["last_received_date"] = valid_dates.max().strftime("%Y-%m-%d")

        january_2010 = fsr_df[
            (fsr_df["접수일"].dt.year == 2010) &
            (fsr_df["접수일"].dt.month == 1)
        ]

        summary["received_in_2010_01"] = len(january_2010)


# 제품군 TOP 5
if "제품군" in fsr_df.columns:
    summary["product_group_top5"] = (
        fsr_df["제품군"]
        .value_counts()
        .head(5)
        .to_dict()
    )


# 기종명 TOP 5
if "기종명" in fsr_df.columns:
    summary["model_top5"] = (
        fsr_df["기종명"]
        .value_counts()
        .head(5)
        .to_dict()
    )


# 현상(대) TOP 5
if "현상(대)" in fsr_df.columns:
    summary["symptom_large_top5"] = (
        fsr_df["현상(대)"]
        .value_counts()
        .head(5)
        .to_dict()
    )


# 현상(중) TOP 5
if "현상(중)" in fsr_df.columns:
    summary["symptom_middle_top5"] = (
        fsr_df["현상(중)"]
        .value_counts()
        .head(5)
        .to_dict()
    )


# 현상(소) TOP 5
if "현상(소)" in fsr_df.columns:
    summary["symptom_small_top5"] = (
        fsr_df["현상(소)"]
        .value_counts()
        .head(5)
        .to_dict()
    )


# 거점 TOP 5
if "거점" in fsr_df.columns:
    summary["service_center_top5"] = (
        fsr_df["거점"]
        .value_counts()
        .head(5)
        .to_dict()
    )


# 비용 통계
if "합계비용" in fsr_df.columns:
    summary["total_cost"] = float(fsr_df["합계비용"].sum())
    summary["average_cost"] = float(round(fsr_df["합계비용"].mean(), 2))
    summary["max_cost"] = float(fsr_df["합계비용"].max())


# --------------------------------------------------
# Summary 출력
# --------------------------------------------------

print("\n==============================")
print("AI Agent용 FSR Summary")
print("==============================")

for key, value in summary.items():
    print(f"{key}: {value}")


print("\n===== 접수일 날짜 확인 =====")

print("접수일 데이터 타입:")
print(fsr_df["접수일"].dtype)

print("\n접수일 앞 10건:")
print(fsr_df["접수일"].head(10))

print("\n연도별 건수:")
print(fsr_df["접수일"].dt.year.value_counts().sort_index())

print("\n2010년 월별 접수 건수:")
data_2010 = fsr_df[fsr_df["접수일"].dt.year == 2010]

print(
    data_2010["접수일"]
    .dt.month
    .value_counts()
    .sort_index()
)