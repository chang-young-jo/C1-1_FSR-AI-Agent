from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from firebase_config import db
import os
import json

from dotenv import load_dotenv
from openai import OpenAI

from datetime import datetime

from fastapi.middleware.cors import CORSMiddleware

from fsr_service import (
    get_fsr_summary,
    get_fsr_list_from_firestore,
    search_fsr_for_question,
    get_keyword_count,
    get_filtered_analysis
)

class FSRCreate(BaseModel):
    FSR문서번호: str
    접수일: str
    실적월: Optional[str] = ""
    제품군: Optional[str] = "미분류"
    기종명: Optional[str] = "미분류"
    기종: Optional[str] = "미분류"
    호기: Optional[str] = "미분류"
    설치고객사명: Optional[str] = "미분류"
    거점: Optional[str] = "미분류"
    클레임_구분: Optional[str] = "미분류"
    현상_대: Optional[str] = "미분류"
    현상_중: Optional[str] = "미분류"
    현상_소: Optional[str] = "미분류"
    접수내용: Optional[str] = "내용 없음"
    기술비용: float = 0
    합계비용: float = 0

class FSRUpdate(BaseModel):
    접수일: Optional[str] = None
    실적월: Optional[str] = None
    제품군: Optional[str] = None
    기종명: Optional[str] = None
    기종: Optional[str] = None
    호기: Optional[str] = None
    설치고객사명: Optional[str] = None
    거점: Optional[str] = None
    클레임_구분: Optional[str] = None
    현상_대: Optional[str] = None
    현상_중: Optional[str] = None
    현상_소: Optional[str] = None
    접수내용: Optional[str] = None
    기술비용: Optional[float] = None
    합계비용: Optional[float] = None

load_dotenv()

openai_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


app = FastAPI(
    title="FSR Quality Analysis AI Agent",
    description="공작기계 FSR 필드클레임 품질 데이터 분석 AI Agent",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {
        "message": "FSR Quality Analysis AI Agent API",
        "status": "running"
    }


@app.get("/api/data/summary")
def read_fsr_summary():
    summary = get_fsr_summary()

    related_data = search_fsr_for_question(
    request.message
)

    return summary

@app.get("/api/data")
def read_fsr_data(limit: int = 20):
    data = get_fsr_list_from_firestore(limit)

    return {
        "count": len(data),
        "data": data
    }

@app.post("/api/data")
def create_fsr_data(fsr: FSRCreate):
    data = {
        "FSR문서번호": fsr.FSR문서번호,
        "접수일": fsr.접수일,
        "실적월": fsr.실적월,
        "제품군": fsr.제품군,
        "기종명": fsr.기종명,
        "기종": fsr.기종,
        "호기": fsr.호기,
        "설치고객사명": fsr.설치고객사명,
        "거점": fsr.거점,
        "클레임 구분": fsr.클레임_구분,
        "현상(대)": fsr.현상_대,
        "현상(중)": fsr.현상_중,
        "현상(소)": fsr.현상_소,
        "접수내용": fsr.접수내용,
        "기술비용": fsr.기술비용,
        "합계비용": fsr.합계비용
    }

    db.collection("fsr_data").document(
        fsr.FSR문서번호
    ).set(data)

    return {
        "message": "FSR 데이터 등록 완료",
        "id": fsr.FSR문서번호
    }

@app.put("/api/data/{id}")
def update_fsr_data(id: str, fsr: FSRUpdate):
    doc_ref = db.collection("fsr_data").document(id)
    doc = doc_ref.get()

    if not doc.exists:
        return {
            "message": "수정할 FSR 데이터를 찾을 수 없습니다.",
            "id": id
        }

    update_data = {}

    if fsr.접수일 is not None:
        update_data["접수일"] = fsr.접수일

    if fsr.실적월 is not None:
        update_data["실적월"] = fsr.실적월

    if fsr.제품군 is not None:
        update_data["제품군"] = fsr.제품군

    if fsr.기종명 is not None:
        update_data["기종명"] = fsr.기종명

    if fsr.기종 is not None:
        update_data["기종"] = fsr.기종

    if fsr.호기 is not None:
        update_data["호기"] = fsr.호기

    if fsr.설치고객사명 is not None:
        update_data["설치고객사명"] = fsr.설치고객사명

    if fsr.거점 is not None:
        update_data["거점"] = fsr.거점

    if fsr.클레임_구분 is not None:
        update_data["클레임 구분"] = fsr.클레임_구분

    if fsr.현상_대 is not None:
        update_data["현상(대)"] = fsr.현상_대

    if fsr.현상_중 is not None:
        update_data["현상(중)"] = fsr.현상_중

    if fsr.현상_소 is not None:
        update_data["현상(소)"] = fsr.현상_소

    if fsr.접수내용 is not None:
        update_data["접수내용"] = fsr.접수내용

    if fsr.기술비용 is not None:
        update_data["기술비용"] = fsr.기술비용

    if fsr.합계비용 is not None:
        update_data["합계비용"] = fsr.합계비용

    doc_ref.update(update_data)

    return {
        "message": "FSR 데이터 수정 완료",
        "id": id,
        "updated_fields": update_data
    }

class ChatRequest(BaseModel):
    message: str

class ConversationCreate(BaseModel):
    title: str
    user_message: str
    assistant_message: str

@app.delete("/api/data/{id}")
def delete_fsr_data(id: str):
    doc_ref = db.collection("fsr_data").document(id)
    doc = doc_ref.get()

    if not doc.exists:
        return {
            "message": "삭제할 FSR 데이터를 찾을 수 없습니다.",
            "id": id
        }

    doc_ref.delete()

    return {
        "message": "FSR 데이터 삭제 완료",
        "id": id
    }

@app.post("/api/chat")
def chat_with_fsr_agent(request: ChatRequest):
    # 1. 실제 FSR Summary 가져오기
    summary = get_fsr_summary()

    # 2. 질문과 관련된 상세 데이터 검색
    related_data = search_fsr_for_question(
        request.message
    )

    keyword_count = get_keyword_count(
    request.message
    )

    filtered_analysis = get_filtered_analysis(
    request.message
    )

    summary_text = json.dumps(
        summary,
        ensure_ascii=False,
        indent=2
    )

    related_data_text = json.dumps(
        related_data,
        ensure_ascii=False,
        indent=2
    )

    keyword_count_text = json.dumps(
    keyword_count,
    ensure_ascii=False,
    indent=2
    )

    filtered_analysis_text = json.dumps(
    filtered_analysis,
    ensure_ascii=False,
    indent=2
    )


    # 3. AI Agent 역할 및 실제 데이터 주입
    system_prompt = f"""
당신은 공작기계 FSR(Field Service Report)
필드클레임 품질 데이터 분석 AI Agent입니다.

아래 실제 FSR 데이터를 근거로 사용자의 질문에 답변하세요.

[FSR 데이터 Summary]
{summary_text}

[질문 키워드 정확한 집계]
{keyword_count_text}

[조건별 FSR 분석]
{filtered_analysis_text}

[질문과 관련된 FSR 상세 데이터]
{related_data_text}

중요 규칙:
1. 제공된 데이터에 근거해서 답변하세요.
2. 건수 질문은 [질문 키워드 정확한 집계] 값을 우선 사용하세요.
3. 데이터에 없는 내용은 추측하지 마세요.
4. 알 수 없는 경우 데이터만으로 판단할 수 없다고 설명하세요.
5. FSR 전체가 반드시 품질 고장이라는 의미는 아닙니다.
6. 서비스 지원 및 교육 관련 FSR도 포함될 수 있습니다.
7. 한국어로 이해하기 쉽게 답변하세요.
8. 조건이 포함된 질문은 [조건별 FSR 분석] 결과를 우선 사용하세요.
"""

    # 4. OpenAI API 호출
    response = openai_client.responses.create(
        model="gpt-4.1-mini",
        instructions=system_prompt,
        input=request.message
        )

    answer = response.output_text

    conversation_data = {
        "title": request.message[:50],
        "user_message": request.message,
        "assistant_message": answer,
        "created_at": datetime.now()
}

    doc_ref = db.collection("conversations").document()
    doc_ref.set(conversation_data)

    return {
        "question": request.message,
        "answer": answer,
        "conversation_id": doc_ref.id
    }


@app.post("/api/conversations")
def create_conversation(conversation: ConversationCreate):
    data = {
        "title": conversation.title,
        "user_message": conversation.user_message,
        "assistant_message": conversation.assistant_message,
        "created_at": datetime.now()
    }

    doc_ref = db.collection("conversations").document()
    doc_ref.set(data)

    return {
        "message": "대화 저장 완료",
        "id": doc_ref.id
    }

@app.get("/api/conversations")
def get_conversations():
    docs = (
        db.collection("conversations")
        .order_by("created_at", direction="DESCENDING")
        .stream()
    )

    conversations = []

    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id

        if "created_at" in data:
            data["created_at"] = data["created_at"].isoformat()

        conversations.append(data)

    return {
        "count": len(conversations),
        "conversations": conversations
    }

@app.get("/api/conversations/{id}")
def get_conversation(id: str):
    doc_ref = db.collection("conversations").document(id)
    doc = doc_ref.get()

    if not doc.exists:
        return {
            "message": "해당 대화를 찾을 수 없습니다."
        }

    data = doc.to_dict()
    data["id"] = doc.id

    return data

@app.delete("/api/conversations/{id}")
def delete_conversation(id: str):
    doc_ref = db.collection("conversations").document(id)
    doc = doc_ref.get()

    if not doc.exists:
        return {
            "message": "해당 대화를 찾을 수 없습니다."
        }

    doc_ref.delete()

    return {
        "message": "대화 삭제 완료",
        "id": id
    }