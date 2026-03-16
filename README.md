# SecureAgent v2 — Flask + SQLite/PostgreSQL

## 로컬 실행

```bash
# 1. 의존성 설치
pip install -r requirements.txt

# 2. 서버 실행
python app.py

# 3. 브라우저에서 접속
http://localhost:5000
```

---

## Render 배포 (무료)

### 1단계 — GitHub에 올리기
```bash
git init
git add .
git commit -m "SecureAgent v2"
git remote add origin https://github.com/아이디/secureagent.git
git push -u origin main
```

> ⚠️ `.env` 파일은 절대 올리지 마세요 (.gitignore에 포함됨)

### 2단계 — Render 설정
1. https://render.com 회원가입
2. **New → Blueprint** 선택
3. GitHub 저장소 연결
4. `render.yaml` 자동 감지 → Deploy 클릭

### 3단계 — 환경변수 확인
Render 대시보드 → Environment에서 아래 자동 설정됨:
- `DATABASE_URL` : PostgreSQL 연결 문자열 (자동)

### 4단계 — 접속
```
https://secureagent.onrender.com
```
(배포 완료까지 약 2~3분 소요)

---

## 구조

```
secureagent/
├── app.py           # Flask 서버 + API 라우트
├── database.py      # SQLite/PostgreSQL 모델 + 샘플데이터
├── requirements.txt # 의존성
├── render.yaml      # Render 배포 설정
├── .gitignore
├── .env.example     # 환경변수 예시
└── static/
    └── index.html   # 프론트엔드
```

## API 엔드포인트

| 메서드 | 경로 | 설명 |
|--------|------|------|
| POST | /api/chat | Claude API 중계 |
| GET/POST/DELETE | /api/history | 질문 히스토리 |
| GET/POST | /api/cache | 답변 캐시 |
| GET/POST | /api/bookmark | 북마크 |
| POST | /api/bookmark/memo | 메모 저장 |
| GET | /api/sample | 샘플 데이터 |
