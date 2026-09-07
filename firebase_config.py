import os
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


firebase_json = os.getenv("FIREBASE_CREDENTIALS")

if firebase_json:
    firebase_dict = json.loads(firebase_json)
    cred = credentials.Certificate(firebase_dict)
else:
    cred = credentials.Certificate("firebase-key.json")


if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()


def test_firestore_connection():
    try:
        collections = list(db.collections())

        print("Firestore 연결 성공")

        if len(collections) == 0:
            print("현재 생성된 컬렉션이 없습니다.")
        else:
            print("현재 컬렉션:")

            for collection in collections:
                print("-", collection.id)

    except Exception as e:
        print("Firestore 연결 실패")
        print(e)


if __name__ == "__main__":
    test_firestore_connection()