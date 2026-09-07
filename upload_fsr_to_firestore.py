from firebase_config import db
from fsr_service import load_fsr_data


def upload_fsr_data():
    fsr_df = load_fsr_data()

    collection_ref = db.collection("fsr_data")

    print("Firestore 업로드 시작")
    print("총 데이터:", len(fsr_df), "건")

    for index, row in fsr_df.iterrows():
        data = row.to_dict()

        # 날짜를 문자열로 변환
        if "접수일" in data and data["접수일"] is not None:
            try:
                data["접수일"] = data["접수일"].strftime("%Y-%m-%d")
            except Exception:
                data["접수일"] = ""

        # 문서 ID는 FSR문서번호를 우선 사용
        document_id = str(data.get("FSR문서번호", index))

        collection_ref.document(document_id).set(data)

        if (index + 1) % 100 == 0:
            print(f"{index + 1}건 업로드 완료")

    print("Firestore 업로드 완료")
    print("총 업로드:", len(fsr_df), "건")


if __name__ == "__main__":
    upload_fsr_data()