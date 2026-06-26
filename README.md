# 🍳 냉장고 셰프 - Backend

> 냉장고 속 재료 기반 AI 레시피 추천 서비스의 백엔드 서버

## 기술 스택

- **Framework**: FastAPI (Python)
- **Database**: AWS RDS (PostgreSQL)
- **AI**: AWS Bedrock (Claude Haiku 4.5, Titan Text Embeddings V2)
- **Vector DB**: AWS S3 Vectors
- **Storage**: AWS S3
- **Deployment**: AWS EC2

## 프로젝트 구조
backend/

├── main.py              # FastAPI 앱 진입점

├── database.py          # DB 연결 설정

├── models.py            # SQLAlchemy 모델

├── requirements.txt     # 패키지 목록

├── .env.example         # 환경변수 예시

├── data/

│   ├── collect_recipes.py      # COOKRCP01 데이터 수집

│   ├── preprocess_recipes.py   # 데이터 전처리

│   ├── embed_and_upload.py     # 임베딩 생성 및 S3 Vectors 업로드

│   └── inspect_raw.py          # 원본 데이터 확인

└── routers/

├── auth.py          # 회원가입 / 로그인

├── recommend.py     # RAG 레시피 추천

├── recipes.py       # 레시피 목록 / 상세

├── fridge.py        # 냉장고 재료 관리

└── favorites.py     # 즐겨찾기

## RAG 파이프라인
재료 입력

↓

Titan Text Embeddings V2 (벡터 변환)

↓

S3 Vectors (유사 레시피 Top-5 검색)

↓

Claude Haiku 4.5 (레시피 생성)

## API 엔드포인트

| Method | Endpoint | 설명 |
|--------|----------|------|
| POST | /auth/register | 회원가입 |
| POST | /auth/login | 로그인 |
| POST | /recommend | AI 레시피 추천 |
| GET | /recipes | 레시피 목록 |
| GET | /recipes/{id} | 레시피 상세 |
| GET | /fridge | 냉장고 재료 조회 |
| POST | /fridge | 재료 추가 |
| DELETE | /fridge/{id} | 재료 삭제 |
| GET | /favorites | 즐겨찾기 조회 |
| POST | /favorites | 즐겨찾기 추가 |
| DELETE | /favorites/{id} | 즐겨찾기 삭제 |

## 시작하기

```bash
# 의존성 설치
pip install -r requirements.txt

# 환경변수 설정
cp .env.example .env
# .env 파일을 열어 값 입력

# 서버 실행
uvicorn main:app --reload
```

API 문서: http://localhost:8000/docs

## 데이터 수집 및 임베딩

```bash
# 1. 레시피 데이터 수집
python data/collect_recipes.py

# 2. 데이터 전처리
python data/preprocess_recipes.py

# 3. 임베딩 생성 및 S3 Vectors 업로드
python data/embed_and_upload.py
```