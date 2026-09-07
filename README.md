# 🤖 공작기계 FSR 필드클레임 품질 데이터 분석 AI Agent

## 1. 프로젝트 소개

본 프로젝트는 공작기계 출하 이후 고객 사용 과정에서 발생하는  
**FSR(Field Service Report)** 데이터를 기반으로 품질 및 서비스 현황을 분석하고,  
사용자가 자연어로 질문하면 AI가 실제 FSR 데이터를 기반으로 답변하는  
**공작기계 필드클레임 품질 데이터 분석 AI Agent**입니다.

분석 대상은 **2010년 1월 실적 FSR 1,082건**이며,  
Python, FastAPI, Firebase Firestore, OpenAI API를 활용하여 구현했습니다.

---

## 2. 프로젝트 개발 배경

공작기계 품질업무에서는 제품 출하 이후 고객 현장에서 발생하는  
다양한 서비스 및 품질 관련 정보가 FSR 형태로 축적됩니다.

하지만 많은 양의 FSR 데이터가 Excel 형태로 관리될 경우  
필요한 정보를 확인하기 위해 담당자가 직접 다음과 같은 작업을 수행해야 합니다.

- Excel 필터링
- 데이터 정렬
- 기종별 건수 집계
- 제품군별 현황 분석
- 고장현상 분류
- 고객 접수내용 검색
- 서비스 비용 분석

이러한 반복적인 데이터 조회 및 분석 업무를 줄이기 위해  
**자연어 질문만으로 FSR 데이터를 조회하고 분석할 수 있는 AI Agent**를 개발했습니다.

---

## 3. 프로젝트 목표

본 프로젝트의 주요 목표는 다음과 같습니다.

1. FSR Excel 데이터 전처리 및 분석
2. Firebase Firestore를 이용한 데이터 관리
3. FastAPI 기반 REST API 구축
4. FSR 데이터 CRUD 기능 구현
5. OpenAI API 기반 자연어 질의 기능 구현
6. 질문 조건에 따른 FSR 데이터 집계 및 분석
7. AI 질문 및 답변 대화 이력 저장
8. HTML/CSS/JavaScript 기반 사용자 인터페이스 구현
9. Backend 및 Frontend 클라우드 배포
10. 실제 품질업무에 활용 가능한 AI Agent 구현

---

## 4. 데이터 개요

### 분석 대상 데이터

파일명:

`FSR_2010.01_1,082.xlsx`

분석 대상:

**2010년 1월 실적 FSR 1,082건**

### 접수일 기준 데이터

- 2009년 접수 FSR: 270건
- 2010년 1월 접수 FSR: 812건
- 전체: 1,082건

> **주의:** `2010년 1월 실적 FSR 1,082건`과  
> `2010년 1월 접수 FSR 812건`은 서로 다른 기준입니다.  
> 본 프로젝트에서는 `실적월`과 `접수일`을 구분하여 분석합니다.

---

## 5. 주요 분석 항목

FSR 원본 데이터에서 AI 분석에 필요한 주요 항목을 선정했습니다.

- FSR문서번호
- 접수일
- 실적월
- 제품군
- 기종명
- 기종
- 호기
- 설치고객사명
- 거점
- 클레임 구분
- 현상(대)
- 현상(중)
- 현상(소)
- 접수내용
- 기술비용
- 합계비용

누락된 현상 분류 값은 임의로 추정하지 않고 `미분류`로 처리하며,  
접수내용이 없는 경우에는 `내용 없음`으로 처리하도록 구성했습니다.

---

## 6. 주요 데이터 분석 결과

### 제품군별 FSR

| 제품군 | 건수 |
|---|---:|
| TC | 485 |
| VMC | 460 |
| HMC | 134 |
| GRINDING | 3 |
| **합계** | **1,082** |

### 주요 기종

| 순위 | 기종명 | 건수 |
|---|---|---:|
| 1 | KIT450 | 96 |
| 2 | i-CUT380T | 63 |
| 3 | E200A | 56 |
| 4 | E200C | 46 |
| 5 | L210A | 45 |

### 주요 서비스 거점

| 순위 | 서비스 거점 | 건수 |
|---|---|---:|
| 1 | 서울직영센터 | 375 |
| 2 | 부산직영센터 | 261 |
| 3 | 창원직영센터 | 178 |
| 4 | 대구직영센터 | 157 |
| 5 | 천안직영센터 | 73 |

### 현상(대) 주요 항목

| 순위 | 현상(대) | 건수 |
|---|---|---:|
| 1 | 고객 | 516 |
| 2 | ATC&MAGAZINE | 114 |
| 3 | 전장 | 110 |
| 4 | HEAD & 구동부 | 73 |
| 5 | 유압/윤활/순환장치 | 72 |

> **중요:** FSR 전체가 반드시 공작기계의 품질 고장을 의미하는 것은 아닙니다.  
> 고객 기술지원, 교육 등 서비스 관련 FSR도 포함되어 있으므로  
> 단순 FSR 건수를 모두 품질불량 건수로 해석하지 않도록 AI Agent에 규칙을 적용했습니다.

---

## 7. 주요 기능

### 7.1 FSR 데이터 조회

Firestore에 저장된 FSR 데이터를 API를 통해 조회할 수 있습니다.

### 7.2 FSR 데이터 등록

새로운 FSR 데이터를 Firestore에 등록할 수 있습니다.

### 7.3 FSR 데이터 수정

FSR 문서 ID를 이용하여 기존 데이터를 수정할 수 있습니다.

### 7.4 FSR 데이터 삭제

불필요한 FSR 데이터를 삭제할 수 있습니다.

### 7.5 FSR Summary 분석

전체 FSR 데이터의 주요 통계와 분석 결과를 Summary 형태로 제공합니다.

### 7.6 AI 자연어 질의

사용자가 일반적인 한국어 문장으로 FSR 데이터에 대해 질문할 수 있습니다.

예시 질문:

```text
KIT450은 총 몇 건이야?
```

AI 답변 예시:

```text
KIT450의 총 FSR 건수는 96건입니다.
```

또 다른 질문:

```text
VMC 중에서 가장 많은 기종은 뭐야?
```

AI 답변 예시:

```text
VMC 제품군에서 가장 많은 기종은 i-CUT380T이며,
총 63건입니다.
```

또 다른 질문:

```text
가장 많이 발생한 현상(대)은 무엇이고 몇 건이야?
```

AI는 실제 FSR 분석 데이터를 Context로 제공받아 답변하도록 구현했습니다.

---

## 8. AI Agent 동작 구조

AI Agent는 사용자의 질문을 바로 LLM에 전달하는 방식이 아니라  
FSR 데이터를 먼저 분석한 후 관련 데이터를 AI Context로 제공합니다.

```text
사용자 질문
    ↓
Frontend
    ↓
FastAPI /api/chat
    ↓
질문 분석
    ↓
FSR Summary 조회
    ↓
질문 키워드 집계
    ↓
조건별 FSR 데이터 분석
    ↓
관련 FSR 상세 데이터 검색
    ↓
분석 결과를 Context로 구성
    ↓
OpenAI API
    ↓
데이터 기반 AI 답변
    ↓
Firestore 대화 이력 저장
    ↓
사용자 화면에 결과 표시
```

이를 통해 AI가 데이터에 존재하지 않는 내용을 임의로 추측하는 것을 줄이고,  
실제 FSR 데이터를 근거로 답변하도록 구현했습니다.

---

## 9. 대화 이력 관리

AI Agent와의 질문 및 답변은 Firebase Firestore에 자동 저장됩니다.

저장 항목:

- 대화 제목
- 사용자 질문
- AI 답변
- 생성 시간
- Conversation ID

사용자는 웹 화면에서 다음 기능을 사용할 수 있습니다.

- 이전 대화 목록 조회
- 최신 대화 순 정렬
- 이전 질문 클릭
- 질문 및 답변 다시 보기
- 대화 삭제

---

## 10. 시스템 아키텍처

```text
┌──────────────────────────┐
│          사용자           │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│     Vercel Frontend      │
│   HTML / CSS / JS        │
└────────────┬─────────────┘
             │ HTTPS API
             ▼
┌──────────────────────────┐
│     Render Backend       │
│   Python + FastAPI       │
└───────┬──────────┬───────┘
        │          │
        ▼          ▼
┌──────────────┐  ┌──────────────┐
│ FSR 데이터   │  │ OpenAI API   │
│ 분석(Pandas) │  │ GPT-4.1-mini │
└──────────────┘  └──────────────┘
        │
        ▼
┌──────────────────────────┐
│   Firebase Firestore     │
│ FSR / Conversation 저장 │
└──────────────────────────┘
```

---

## 11. 기술 스택

### Backend

- Python
- FastAPI
- Uvicorn
- Pandas
- OpenPyXL

### AI

- OpenAI API
- GPT-4.1-mini

### Database

- Firebase
- Firestore

### Frontend

- HTML
- CSS
- JavaScript

### Deployment

- Render
- Vercel

### Version Control

- Git
- GitHub

---

## 12. API 구성

### FSR Data API

| Method | Endpoint | 기능 |
|---|---|---|
| GET | `/api/data` | FSR 데이터 조회 |
| POST | `/api/data` | FSR 데이터 등록 |
| PUT | `/api/data/{id}` | FSR 데이터 수정 |
| DELETE | `/api/data/{id}` | FSR 데이터 삭제 |
| GET | `/api/data/summary` | FSR Summary 조회 |

### AI API

| Method | Endpoint | 기능 |
|---|---|---|
| POST | `/api/chat` | FSR 데이터 기반 AI 질의 |

### Conversation API

| Method | Endpoint | 기능 |
|---|---|---|
| POST | `/api/conversations` | 대화 저장 |
| GET | `/api/conversations` | 대화 목록 조회 |
| GET | `/api/conversations/{id}` | 대화 상세 조회 |
| DELETE | `/api/conversations/{id}` | 대화 삭제 |

---

## 13. 프로젝트 실행 방법

### 13.1 저장소 Clone

```bash
git clone https://github.com/chang-young-jo/C1-1_FSR-AI-Agent.git
```

프로젝트 폴더로 이동합니다.

```bash
cd C1-1_FSR-AI-Agent
```

### 13.2 Python 가상환경 생성

```bash
python -m venv venv
```

Windows PowerShell에서 가상환경을 실행합니다.

```powershell
.\venv\Scripts\Activate.ps1
```

### 13.3 패키지 설치

```bash
pip install -r requirements.txt
```

### 13.4 환경변수 설정

프로젝트 최상위 폴더에 `.env` 파일을 생성합니다.

```text
OPENAI_API_KEY=YOUR_OPENAI_API_KEY
```

Firebase 인증정보는 로컬 개발환경에서는 `firebase-key.json`을 사용하며,  
Render 배포환경에서는 다음 환경변수를 사용합니다.

```text
FIREBASE_CREDENTIALS
```

### 13.5 FastAPI 실행

```bash
uvicorn main:app --reload
```

로컬 Swagger:

```text
http://127.0.0.1:8000/docs
```

---

## 14. 프로젝트 구조

```text
C1-1_FSR-AI-Agent
│
├─ main.py
├─ fsr_service.py
├─ firebase_config.py
├─ analyze_fsr.py
├─ upload_fsr_to_firestore.py
├─ test_openai.py
├─ index.html
├─ style.css
├─ script.js
├─ requirements.txt
├─ FSR_2010.01_1,082.xlsx
├─ .gitignore
└─ README.md
```

보안 관련 파일은 GitHub Repository에서 제외됩니다.

```text
.env
firebase-key.json
venv/
```

---

## 15. 보안 관리

OpenAI API Key와 Firebase Service Account 인증정보는  
GitHub Repository에 직접 저장하지 않습니다.

`.gitignore` 설정:

```gitignore
venv/
.env
firebase-key.json
__pycache__/
*.pyc
```

Render 배포환경에서는 다음 환경변수를 사용합니다.

```text
OPENAI_API_KEY
FIREBASE_CREDENTIALS
```

이를 통해 API Key와 Firebase 인증정보가 소스코드에 노출되지 않도록 구성했습니다.

---

## 16. 배포 정보

### Frontend - Vercel

https://c1-1-fsr-ai-agent.vercel.app

### Backend - Render

https://c1-1fsr-ai-agent.onrender.com

### Swagger API Documentation

https://c1-1fsr-ai-agent.onrender.com/docs

### GitHub Repository

https://github.com/chang-young-jo/C1-1_FSR-AI-Agent

---

## 17. 배포 테스트 결과

실제 Vercel 배포환경에서 다음 질문을 테스트했습니다.

### 테스트 1

질문:

```text
KIT450은 총 몇 건이야?
```

결과:

```text
KIT450의 총 FSR 건수는 96건입니다.
```

### 테스트 2

질문:

```text
VMC 중에서 가장 많은 기종은 뭐야?
```

결과:

```text
VMC 제품군에서 가장 많은 기종은 i-CUT380T이며,
총 63건입니다.
```

또한 AI 질문 후 대화가 Firestore에 자동 저장되고,  
웹 화면에서 대화 이력 조회 및 삭제가 정상적으로 동작하는 것을 확인했습니다.

---

## 18. 주요 구현 결과

본 프로젝트를 통해 다음 기능을 구현했습니다.

- FSR 1,082건 데이터 전처리 및 분석
- 100건 이상의 시계열 데이터 확보
- Firebase Firestore 데이터 저장
- FastAPI 기반 REST API 구축
- FSR 데이터 CRUD 구현
- FSR Summary API 구현
- OpenAI API 연동
- 자연어 기반 FSR 데이터 질의
- 질문 키워드 기반 정확한 건수 집계
- 제품군 등 조건별 데이터 분석
- AI 질문/답변 자동 저장
- 대화 이력 조회
- 대화 상세 조회
- 대화 삭제
- 생성시간 기준 최신순 정렬
- HTML/CSS/JavaScript 사용자 화면 구현
- CORS 설정
- 환경변수를 이용한 API Key 보안관리
- Render Backend 배포
- Vercel Frontend 배포
- Swagger API 문서 제공
- Git/GitHub 버전 관리

---

## 19. 프로젝트 기대효과

본 프로젝트를 실제 공작기계 품질업무에 적용할 경우  
담당자가 Excel 데이터를 반복적으로 검색하고 집계하는 시간을 줄일 수 있습니다.

기존 방식:

```text
FSR Excel 실행
→ 필터 설정
→ 조건 검색
→ 데이터 집계
→ 결과 확인
```

AI Agent 적용 방식:

```text
사용자 자연어 질문
→ AI Agent 분석
→ 결과 확인
```

예를 들어 사용자가 다음과 같이 질문할 수 있습니다.

```text
KIT450은 총 몇 건이야?
```

```text
VMC 중에서 가장 많은 기종은 뭐야?
```

```text
가장 많이 발생한 현상은 뭐야?
```

```text
서비스 거점별 FSR 현황을 알려줘.
```

이를 통해 품질 담당자가 데이터 검색보다  
**원인 분석과 품질 개선 활동에 더 집중할 수 있는 환경**을 구축할 수 있습니다.

---

## 20. 향후 개선 방향

현재 프로젝트는 2010년 1월 실적 FSR 데이터를 대상으로 구현했습니다.

향후 여러 연도의 FSR 데이터를 추가하면 다음 기능으로 확장할 수 있습니다.

- 연도별 FSR 발생 추이 분석
- 월별 FSR 증감 분석
- 제품군별 품질 추세 분석
- 기종별 반복 클레임 분석
- 고객별 반복 클레임 분석
- 서비스 거점별 품질 비교
- 비용 상위 클레임 자동 분석
- 고장현상 변화 추세 분석
- 신규 이상징후 탐지
- 반복 고장 패턴 탐지
- 품질 개선 우선순위 추천
- 품질 리포트 자동 생성

향후에는 단순한 데이터 조회 AI를 넘어  
**공작기계 품질 의사결정을 지원하는 AI Agent**로 확장하는 것을 목표로 합니다.

---

## 21. 프로젝트 개발 의의

본 프로젝트는 단순히 OpenAI API를 호출하는 챗봇이 아니라  
실제 공작기계 FSR 데이터를 분석하고 그 결과를 AI Context로 제공하여  
사용자의 자연어 질문에 데이터 기반으로 답변하도록 구현했습니다.

또한 FastAPI, Firebase Firestore, OpenAI API, HTML/CSS/JavaScript,  
Render, Vercel, GitHub를 하나의 서비스로 연결하여  
데이터 저장부터 AI 분석, 사용자 인터페이스, 클라우드 배포까지  
전체 AI Agent 서비스 개발 과정을 구현했습니다.

특히 실제 현업에서 사용하는 공작기계 필드 서비스 데이터를 활용함으로써  
AI 기술을 제조업 품질업무에 적용할 수 있는 가능성을 확인한 프로젝트입니다.