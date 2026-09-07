import pandas as pd

FILE_PATH = "FSR_2010.01_1,082.xlsx"


def load_fsr_data():
    df = pd.read_excel(FILE_PATH)

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

    available_columns = [
        column for column in selected_columns
        if column in df.columns
    ]

    fsr_df = df[available_columns].copy()

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

    if "접수내용" in fsr_df.columns:
        fsr_df["접수내용"] = fsr_df["접수내용"].fillna("내용 없음")

    if "접수일" in fsr_df.columns:
        fsr_df["접수일"] = pd.to_datetime(
        fsr_df["접수일"].astype(str).str.replace(".0", "", regex=False),
        format="%Y%m%d",
        errors="coerce"
    )
        

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

    return fsr_df


def get_fsr_summary():
    fsr_df = load_fsr_data()

    summary = {
        "total_fsr": len(fsr_df)
    }

    if "접수일" in fsr_df.columns:
        valid_dates = fsr_df["접수일"].dropna()

        if not valid_dates.empty:
            summary["first_received_date"] = (
                valid_dates.min().strftime("%Y-%m-%d")
            )

            summary["last_received_date"] = (
                valid_dates.max().strftime("%Y-%m-%d")
            )

            january_2010 = fsr_df[
                (fsr_df["접수일"].dt.year == 2010) &
                (fsr_df["접수일"].dt.month == 1)
            ]

            summary["received_in_2010_01"] = len(january_2010)

    if "제품군" in fsr_df.columns:
        summary["product_group_top5"] = (
            fsr_df["제품군"]
            .value_counts()
            .head(5)
            .to_dict()
        )

    if "기종명" in fsr_df.columns:
        summary["model_top5"] = (
            fsr_df["기종명"]
            .value_counts()
            .head(5)
            .to_dict()
        )

    if "현상(대)" in fsr_df.columns:
        summary["symptom_large_top5"] = (
            fsr_df["현상(대)"]
            .value_counts()
            .head(5)
            .to_dict()
        )

    if "현상(중)" in fsr_df.columns:
        summary["symptom_middle_top5"] = (
            fsr_df["현상(중)"]
            .value_counts()
            .head(5)
            .to_dict()
        )

    if "현상(소)" in fsr_df.columns:
        summary["symptom_small_top5"] = (
            fsr_df["현상(소)"]
            .value_counts()
            .head(5)
            .to_dict()
        )

    if "거점" in fsr_df.columns:
        summary["service_center_top5"] = (
            fsr_df["거점"]
            .value_counts()
            .head(5)
            .to_dict()
        )

    if "합계비용" in fsr_df.columns:
        summary["total_cost"] = float(
            fsr_df["합계비용"].sum()
        )

        summary["average_cost"] = float(
            round(fsr_df["합계비용"].mean(), 2)
        )

        summary["max_cost"] = float(
            fsr_df["합계비용"].max()
        )

    return summary


def get_fsr_list(limit=20):
    fsr_df = load_fsr_data()

    result_df = fsr_df.head(limit).copy()

    if "접수일" in result_df.columns:
        result_df["접수일"] = result_df["접수일"].dt.strftime("%Y-%m-%d")

    result_df = result_df.fillna("")

    return result_df.to_dict(orient="records")

def get_fsr_list(limit=20):
    fsr_df = load_fsr_data()

    result_df = fsr_df.head(limit).copy()

    if "접수일" in result_df.columns:
        result_df["접수일"] = result_df["접수일"].dt.strftime("%Y-%m-%d")

    result_df = result_df.fillna("")

    return result_df.to_dict(orient="records")


from firebase_config import db


def get_fsr_list_from_firestore(limit=20):
    docs = (
        db.collection("fsr_data")
        .limit(limit)
        .stream()
    )

    result = []

    for doc in docs:
        data = doc.to_dict()

        data["id"] = doc.id

        result.append(data)

    return result

def search_fsr_for_question(question, limit=20):
    fsr_df = load_fsr_data()

    question = question.lower().strip()

    search_columns = [
        "제품군",
        "기종명",
        "기종",
        "설치고객사명",
        "거점",
        "현상(대)",
        "현상(중)",
        "현상(소)",
        "접수내용"
    ]

    mask = False

    for column in search_columns:
        if column in fsr_df.columns:
            column_mask = (
                fsr_df[column]
                .astype(str)
                .str.lower()
                .apply(lambda value: value in question or question in value)
            )

            mask = mask | column_mask

    result_df = fsr_df[mask].head(limit).copy()

    if "접수일" in result_df.columns:
        result_df["접수일"] = (
            result_df["접수일"]
            .dt.strftime("%Y-%m-%d")
        )

    return result_df.to_dict(orient="records")

def get_keyword_count(question):
    fsr_df = load_fsr_data()

    question_lower = question.lower()

    search_columns = [
        "제품군",
        "기종명",
        "기종",
        "설치고객사명",
        "거점",
        "현상(대)",
        "현상(중)",
        "현상(소)",
        "접수내용"
    ]

    result = {}

    for column in search_columns:
        if column not in fsr_df.columns:
            continue

        unique_values = (
            fsr_df[column]
            .dropna()
            .astype(str)
            .unique()
        )

        for value in unique_values:
            value_lower = value.lower()

            if value_lower in question_lower:
                count = (
                    fsr_df[column]
                    .astype(str)
                    .str.lower()
                    .eq(value_lower)
                    .sum()
                )

                result[value] = {
                    "column": column,
                    "count": int(count)
                }

    return result

def get_filtered_analysis(question):
    fsr_df = load_fsr_data()

    question_lower = question.lower()
    filtered_df = fsr_df.copy()

    applied_filters = {}

    # 제품군 조건 찾기
    if "제품군" in fsr_df.columns:
        product_groups = (
            fsr_df["제품군"]
            .dropna()
            .astype(str)
            .unique()
        )

        for value in product_groups:
            if value.lower() in question_lower:
                filtered_df = filtered_df[
                    filtered_df["제품군"]
                    .astype(str)
                    .str.lower()
                    .eq(value.lower())
                ]

                applied_filters["제품군"] = value
                break

    # 기종명 조건 찾기
    if "기종명" in fsr_df.columns:
        models = (
            fsr_df["기종명"]
            .dropna()
            .astype(str)
            .unique()
        )

        for value in models:
            if value.lower() in question_lower:
                filtered_df = filtered_df[
                    filtered_df["기종명"]
                    .astype(str)
                    .str.lower()
                    .eq(value.lower())
                ]

                applied_filters["기종명"] = value
                break

    result = {
        "applied_filters": applied_filters,
        "filtered_count": int(len(filtered_df))
    }

    # 조건 내 기종 TOP 10
    if "기종명" in filtered_df.columns:
        result["model_top10"] = (
            filtered_df["기종명"]
            .value_counts()
            .head(10)
            .to_dict()
        )

    # 조건 내 현상(대) TOP 10
    if "현상(대)" in filtered_df.columns:
        result["symptom_large_top10"] = (
            filtered_df["현상(대)"]
            .value_counts()
            .head(10)
            .to_dict()
        )

    # 조건 내 현상(중) TOP 10
    if "현상(중)" in filtered_df.columns:
        result["symptom_middle_top10"] = (
            filtered_df["현상(중)"]
            .value_counts()
            .head(10)
            .to_dict()
        )

    # 조건 내 비용
    if "합계비용" in filtered_df.columns:
        result["total_cost"] = float(
            filtered_df["합계비용"].sum()
        )

        result["average_cost"] = float(
            round(filtered_df["합계비용"].mean(), 2)
        )

    return result