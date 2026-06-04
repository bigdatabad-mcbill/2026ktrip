# 🌍 CloseTrip Live - 인천 여행 플래너 앱

**CloseTrip Live**는 인천의 다양한 명소를 발견하고, 실시간으로 다른 여행자들과 연결되며, 여행 경험을 공유하는 **올인원 여행 플래닝 및 소셜 플랫폼**입니다.

[서비스 사업 계획서 보기](2026ktrip.md)

🇰🇷 **한국어** | 🇬🇧 **English** 지원  
📱 **모바일 최적화 설계** | 🌐 **반응형 웹앱**

---

## 📌 프로젝트 개요

### 🎯 핵심 기능

| 기능 | 설명 |
|------|------|
| **🗺️ 명소 탐색** | 인천의 21개 명소를 9개 카테고리(축제, 역사, 음식, 포토, 자연, 시장, 문화, 핫플)로 분류 |
| **📅 일정 관리** | 여행 일정을 시간별로 계획하고 저장하기 |
| **📍 실시간 체크인** | 현재 방문 중인 장소에 체크인하여 다른 여행자들과 연결 |
| **💬 경험 공유** | 방문 후기, 감정 점수, 팁을 피드에 공유하기 |
| **👥 장소 기반 모임** | 같은 장소에 있는 사람들과 실시간으로 만나고 모임 참여 |
| **⭐ 핫스팟 추천** | 실시간 인기도와 방문자 수를 기반으로 추천 장소 표시 |
| **🌍 다국어 지원** | 한국어/영어 이중 언어 및 확장 가능한 다언어 구조 |

### 💡 타겟 사용자

- 🇰🇷 **국내 여행자**: 주말/휴가 중 인천 여행 계획자
- 🌏 **외국인 관광객**: 인천 방문 외국인 관광객
- 📸 **SNS 활동가**: 여행 사진 촬영 및 공유에 관심 있는 사용자
- 👫 **사교활동자**: 여행 중 새로운 사람들과 만나고 싶은 사용자

---

## 🚀 빠른 시작

### 필수 요구사항

- **Python 3.8 이상**
- **pip** (Python 패키지 관리자)
- **웹 브라우저** (Chrome, Firefox, Safari 등)

### 📦 설치 방법

#### 1단계: 저장소 클론 또는 파일 다운로드

```bash
# Git 저장소 클론
git clone https://github.com/bigdatabad-mcbill/2026ktrip.git
cd 2026ktrip

# 또는 ZIP 파일 다운로드 후 압축 해제
unzip 2026ktrip-main.zip
cd 2026ktrip
```

#### 2단계: Python 가상 환경 생성 (권장)

```bash
# 가상 환경 생성
python -m venv venv

# 가상 환경 활성화
# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

#### 3단계: 의존성 설치

```bash
# requirements.txt의 모든 패키지 설치
pip install -r requirements.txt
```

설치되는 패키지:
- **Flask** (2.3.0+): 웹 서버 프레임워크
- **Flask-CORS** (3.1.0+): 크로스 오리진 요청 처리

### 🎬 구동 방법

#### 방법 1: 로컬 실행 (개발 모드)

```bash
# Python 앱 실행
python app.py
```

**출력 예시:**
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

브라우저에서 `http://localhost:5000` 또는 `http://127.0.0.1:5000` 접속

#### 방법 2: 다른 포트에서 실행

```bash
# 포트 8080에서 실행
FLASK_ENV=development FLASK_DEBUG=1 python -c "from app import app; app.run(host='0.0.0.0', port=8080)"
```

#### 방법 3: GitHub Codespaces에서 실행

```bash
# Codespaces 터미널에서
python app.py

# 또는 포트 포워딩으로
python -c "from app import app; app.run(host='0.0.0.0')"
```

#### 방법 4: 배포 환경 (프로덕션)

```bash
# Gunicorn 사용 (권장)
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# 또는 Waitress 사용
pip install waitress
waitress-serve --port=5000 app:app
```

---

## 🎨 주요 기능 상세 설명

### 1️⃣ 명소 탐색 (Location Discovery)

#### 지원하는 9개 카테고리

| 카테고리 | 명소 수 | 예시 | 아이콘 |
|---------|--------|------|--------|
| **축제 (Festival)** | 2개 | 송도 펜타포트, 인천 아트페스티벌 | 🎵 |
| **역사 (History)** | 3개 | 개항장 문화재 야행, 개항박물관 | 🏛️ |
| **음식 (Food)** | 4개 | 영종도 해변, 오징어 거리, 신포 시장 | 🍜 |
| **포토존 (Photo)** | 3개 | 월미문화의거리, 송도 야경, 일출 촬영지 | 📸 |
| **자연 (Nature)** | 2개 | 소래산 등산로, 갯벌 생태공원 | 🌲 |
| **시장 (Market)** | 2개 | 신포국제시장, 먹거리골목 | 🏪 |
| **문화 (Culture)** | 2개 | 인천 차이나타운, 문화예술회관 | 🎭 |
| **핫플레이스 (Attraction)** | 3개 | 어린이박물관, 경인대교 조망 | ⭐ |

#### 각 명소 정보 구성

```json
{
  "id": 1,
  "name": "송도 펜타포트",
  "english_name": "Songdo Pentaport",
  "category": "Festival",
  "neighborhood": "송도",
  "description": "대한민국 최대 뮤직 페스티벌",
  "english_description": "Korea's largest music festival",
  "detail": "야간 공연, 푸드트럭, 라이브 아트",
  "english_detail": "Night concerts, food trucks, live art",
  "food_tip": "모텔식 꼬치와 식혜",
  "english_tip": "Spicy skewers and Sikhye",
  "transport": "센트럴파크역 도보 15분",
  "english_transport": "15 mins from Central Park Station",
  "image": "https://images.unsplash.com/...",
  "category_tags": ["Festival", "Music"]
}
```

### 2️⃣ 일정 관리 (Schedule Management)

#### 일정 추가하기

1. **"일정 추가" 버튼 클릭**
2. **여행 날짜 선택** (Day 1, Day 2, ... Day 7)
3. **방문 시간 입력** (예: 12:00)
4. **장소 선택** (21개 명소 중 선택)
5. **메모 추가 (선택사항)** (예: "뮤직페스타 첫 공연 보기")
6. **"저장" 버튼 클릭**

#### API 엔드포인트

```bash
# 일정 조회
GET /api/schedule

# 일정 추가
POST /api/schedule
Body: {
  "day": 2,
  "time": "12:00",
  "location_id": 1,
  "note": "송도 펜타포트 뮤직페스타 감상"
}

# 응답
{
  "schedule": [
    {
      "id": 401,
      "day": 2,
      "time": "12:00",
      "location_id": 1,
      "note": "송도 펜타포트 뮤직페스타 감상",
      "created_at": "2026-06-03T10:30:00"
    }
  ]
}
```

### 3️⃣ 실시간 체크인 (Real-time Check-in)

#### 체크인 프로세스

1. **명소 카드에서 "Check In" 버튼 클릭**
2. **자동으로 사용자 ID 생성** (예: `user_12345`)
3. **체크인 성공 토스트 알림** 표시
4. **다른 사용자와 실시간 연결**

#### 실시간 표시

```
🔴 실시간: 12명이 현재 이곳에 있어요!
[프로필 아이콘] [프로필 아이콘] [프로필 아이콘] ...
```

#### API 엔드포인트

```bash
# 위치별 현재 사용자 조회
GET /api/users/location/:location_id

# 체크인
POST /api/users/checkin/:location_id
Body: { "user_id": "user_12345" }

# 체크아웃
POST /api/users/checkout/:location_id
Body: { "user_id": "user_12345" }

# 응답
{
  "location_id": 1,
  "users": ["user_12345", "user_67890", ...],
  "count": 12
}
```

### 4️⃣ 경험 공유 피드 (Social Feed)

#### 피드 작성 및 공유

각 사용자는 방문 후 다음을 공유할 수 있습니다:

- **😊 감정 점수**: 0~100% (만족도)
- **📝 후기 텍스트**: "뮤직페스타 첫 공연 최고! 글로벌 푸드 정말 맛있어요"
- **💡 컨텍스트 팁**: "해변 바람 대비 아노락 필수"
- **📸 사진 (선택)**: 장소 사진 업로드
- **🏷️ 무드 태그**: Festival, Coastal, Shopping 등

#### 피드 구조

```json
{
  "id": 101,
  "author": "지은",
  "location_id": 1,
  "location": "송도 펜타포트",
  "emotion": 92,
  "time": "2시간 전",
  "story": "뮤직페스타 첫 공연 최고! 글로벌 푸드 정말 맛있어요",
  "context": "해변 바람 대비 아노락 필수",
  "mood": "Festival",
  "image": "https://images.unsplash.com/..."
}
```

#### API 엔드포인트

```bash
# 피드 전체 조회
GET /api/feed

# 특정 위치의 피드만 조회
GET /api/feed?location_id=1

# 피드 공유 (새 포스트 작성)
POST /api/feed/share
Body: {
  "author": "지은",
  "location_id": 1,
  "emotion": 92,
  "story": "뮤직페스타 첫 공연 최고!",
  "context": "해변 바람 대비 아노락 필수",
  "mood": "Festival"
}

# 응답
{
  "feed": [...]
}
```

### 5️⃣ 장소 기반 실시간 모임 (Location-based Meetup)

#### 모임 생성하기

1. **명소 선택**
2. **"모임 만들기" 버튼 클릭**
3. **모임 제목 입력** (예: "송도 펜타포트 공연 후 조개구이 함께 먹을 분!")
4. **참여자 수 제한 설정** (선택)
5. **메시지 추가** (선택)
6. **"모임 시작" 버튼**

#### 현재 진행 중인 모임

```json
[
  {
    "id": 201,
    "location_id": 1,
    "title": "송도 펜타포트 뮤직페스타 함께 봐요!",
    "mood": "Music",
    "participants": ["A", "B", "C", "D", "E"],
    "status": "모집중",
    "badge": "지금 5명 참여",
    "context": "야간 공연 함께 보고 스트릿푸드 먹어요"
  }
]
```

#### API 엔드포인트

```bash
# 모임 목록 조회
GET /api/meetups

# 특정 위치의 모임 조회
GET /api/meetups?location_id=1

# 새 모임 생성
POST /api/meetups
Body: {
  "location_id": 1,
  "title": "송도 펜타포트 뮤직페스타 함께 봐요!",
  "mood": "Music",
  "context": "야간 공연 함께 보고 스트릿푸드 먹어요"
}

# 모임 참가
POST /api/meetups/:id/join
Body: { "user_id": "user_12345" }
```

### 6️⃣ 핫스팟 & KPI 대시보드 (Analytics)

#### 대시보드 메트릭

```
📊 CloseTrip Live 대시보드
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌟 인기 명소       | 평균 방문자: 45명
📅 추천 일정       | 7개 인기 일정
💡 여행 팁         | 일일 업데이트
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

#### 핫스팟 순위

| 순위 | 명소 | 현재 방문자 | 뱃지 | 분위기 |
|------|------|-----------|------|--------|
| 1️⃣ | 송도 펜타포트 | 68명 | 24시간 | 🎵 |
| 2️⃣ | 개항장 야행 | 54명 | 18시간 | 🌙 |
| 3️⃣ | 신포국제시장 | 42명 | 15시간 | 🛍️ |
| 4️⃣ | 영종도 해변 | 31명 | 12시간 | 🌅 |
| 5️⃣ | 월미문화거리 | 27명 | 9시간 | 📸 |

#### API 엔드포인트

```bash
# KPI 통계 조회
GET /api/kpis

# 응답
{
  "avg_emotion": 88.5,
  "total_users": 450,
  "active_meetups": 12,
  "locations_visited": 18,
  "feed_posts": 156
}
```

---

## 🔧 기술 스택

### 백엔드

| 기술 | 버전 | 용도 |
|------|------|------|
| **Python** | 3.8+ | 프로그래밍 언어 |
| **Flask** | 2.3.0+ | 웹 프레임워크 |
| **Flask-CORS** | 3.1.0+ | 크로스 오리진 요청 처리 |

### 프론트엔드

| 기술 | 버전 | 용도 |
|------|------|------|
| **HTML5** | - | 마크업 언어 |
| **JavaScript (Vanilla)** | ES6+ | 인터랙티브 기능 |
| **Tailwind CSS** | 3.x (CDN) | 반응형 스타일링 |
| **FontAwesome** | 6.x (CDN) | 아이콘 라이브러리 |

### 기타

| 기술 | 용도 |
|------|------|
| **REST API** | 클라이언트-서버 통신 |
| **JSON** | 데이터 포맷 |
| **LocalStorage** | 클라이언트 데이터 저장 |

---

## 📂 프로젝트 구조

```
2026ktrip/
├── app.py                          # Flask 백엔드 서버
├── Index.html                      # 프론트엔드 SPA (단일 페이지)
├── requirements.txt                # Python 의존성
├── README.md                       # 이 파일
├── PROJECT.md                      # 프로젝트 상세 설명
├── DEVELOPMENT_CHECKLIST.md        # 개발 진행 상황
├── PHASE2_COMPLETION.md            # Phase 2 완성 현황
└── .git/                           # Git 저장소
```

### 백엔드 데이터 구조 (app.py)

```python
# 1. 위치/명소 데이터 (21개)
locations = [
    {"id": 1, "name": "송도 펜타포트", "category": "Festival", ...},
    ...
]

# 2. 사용자 일정 데이터
schedules = [
    {"id": 401, "day": 2, "time": "12:00", "location_id": 1, ...},
]

# 3. 실시간 체크인 세션
user_sessions = {}  # {location_id: [user1, user2, ...]}

# 4. 핫스팟 데이터
hotspots = [
    {"id": 1, "name": "송도 펜타포트", "users": 68, ...},
]

# 5. 사용자 피드
feed_posts = [
    {"id": 101, "author": "지은", "emotion": 92, ...},
]

# 6. 모임 데이터
meetups = [
    {"id": 201, "location_id": 1, "title": "...", ...},
]
```

---

## 🌍 다국어 지원

### 현재 지원 언어

- 🇰🇷 **한국어** (완벽 지원)
- 🇬🇧 **English** (완벽 지원)

### 각 명소에 제공되는 정보

모든 명소는 다음 필드를 한영 이중으로 제공합니다:

```
한국어 정보                              영어 정보
─────────────────────────────────────────────────────
name: "송도 펜타포트"         →    english_name: "Songdo Pentaport"
description: "최대 뮤직 페스티벌"  →   english_description: "Korea's largest music festival"
detail: "야간공연, 푸드트럭"      →    english_detail: "Night concerts, food trucks"
food_tip: "모텔식 꼬치"          →    english_tip: "Spicy skewers"
transport: "센트럴파크역 도보"     →    english_transport: "15 mins from Central Park"
```

### 향후 확장 계획

- 🇯🇵 일본어 (準備中)
- 🇨🇳 중국어 간체 (準備中)
- 🇹🇼 중국어 번체 (準備中)
- 🇹🇭 태국어 (準備中)
- 🇻🇳 베트남어 (準備中)

---

## 📡 API 엔드포인트 완전 명세

### 기본 정보

**Base URL**: `http://localhost:5000`  
**응답 형식**: JSON  
**인증**: 없음 (현재 MVP)

### 엔드포인트 목록

#### 1. 명소 조회

```bash
# 모든 명소 조회
GET /api/locations
Response: { "locations": [...] }

# 카테고리별 필터링
GET /api/locations?category=Festival
Response: { "locations": [...], "category": "Festival" }
```

#### 2. 일정 관리

```bash
# 일정 조회
GET /api/schedule
Response: { "schedule": [...] }

# 일정 추가
POST /api/schedule
Content-Type: application/json
Body: {
  "day": 2,
  "time": "12:00",
  "location_id": 1,
  "note": "송도 펜타포트 뮤직페스타"
}
Response: { "schedule": [...], "message": "일정이 추가되었습니다." }
```

#### 3. 체크인 관리

```bash
# 위치별 사용자 조회
GET /api/users/location/:location_id
Response: { "location_id": 1, "users": [...], "count": 12 }

# 체크인
POST /api/users/checkin/:location_id
Body: { "user_id": "user_12345" }
Response: { "status": "success", "message": "체크인 되었습니다." }

# 체크아웃
POST /api/users/checkout/:location_id
Body: { "user_id": "user_12345" }
```

#### 4. 피드 관리

```bash
# 피드 조회
GET /api/feed
Response: { "feed": [...] }

# 피드 공유
POST /api/feed/share
Body: {
  "author": "지은",
  "location_id": 1,
  "emotion": 92,
  "story": "뮤직페스타 최고!",
  "context": "해변 바람 대비",
  "mood": "Festival"
}
```

#### 5. 모임 관리

```bash
# 모임 목록 조회
GET /api/meetups
Response: { "meetups": [...] }

# 모임 생성
POST /api/meetups
Body: {
  "location_id": 1,
  "title": "송도 펜타포트 함께 봐요!",
  "mood": "Music",
  "context": "야간 공연"
}

# 모임 참가
POST /api/meetups/:id/join
Body: { "user_id": "user_12345" }
```

#### 6. 기타

```bash
# 헬스 체크 (서버 상태 확인)
GET /api/health
Response: { "status": "running", "timestamp": "2026-06-03T10:30:00" }

# KPI 통계
GET /api/kpis
Response: { "avg_emotion": 88.5, "total_users": 450, ... }
```

---

## 📊 현재 구현 현황

### ✅ 완료된 기능 (MVP - Phase 2)

- [x] 21개 명소 데이터베이스
- [x] 9개 카테고리 분류
- [x] 한영 이중언어 지원
- [x] 여행 일정 관리
- [x] 실시간 체크인 시스템
- [x] 여행 경험 공유 피드
- [x] 장소 기반 실시간 모임
- [x] 핫스팟 & KPI 대시보드
- [x] REST API (12개 엔드포인트)
- [x] 반응형 모바일 UI
- [x] 실시간 데이터 자동 갱신 (5초)

### 🟡 진행 중인 기능 (Phase 3)

- 🔄 추가 다국어 지원 (일본어, 중국어, 태국어)
- 🔄 배포 환경 준비 (Docker, AWS/GCP)
- 🔄 사용자 인증 (로그인/회원가입)
- 🔄 성능 최적화

### 🔴 향후 추진 기능 (Phase 4 이후)

#### 단계별 고도화 계획

**Phase 3 (예정)**
- ⭐ 사용자 계정 및 프로필 시스템
- ⭐ 실시간 채팅/DM 기능
- ⭐ 사용자 평가 및 후기 시스템
- ⭐ 장소 즐겨찾기 (저장 기능)
- ⭐ 고급 필터링 (시간대별, 예산별, 인원수별)

**Phase 4 (예정)**
- ⭐ 날씨 API 연동 (실시간 기상정보)
- ⭐ 지도 통합 (Kakao Map, Google Maps)
- ⭐ 길찾기/네비게이션 기능
- ⭐ 실시간 버스/지하철 정보
- ⭐ 음성 인식 검색

**Phase 5 (예정)**
- ⭐ AI 개인화 추천 엔진
- ⭐ 소셜 로그인 (구글, 카카오, 네이버)
- ⭐ 결제 시스템 (티켓/예약)
- ⭐ 푸시 알림
- ⭐ 이미지 업로드 & CDN 연동

**Phase 6 (예정)**
- ⭐ 모바일 앱 (iOS/Android 네이티브)
- ⭐ AR/VR 경험 (가상 둘러보기)
- ⭐ 커뮤니티 기능 (포럼, Q&A)
- ⭐ 여행 상품 마켓플레이스
- ⭐ 데이터 분석 & 비즈니스 인텔리전스

---

## 🔒 보안 및 개인정보 관리

### 현재 보안 수준 (MVP)

⚠️ **주의**: 현재 MVP는 로컬 개발 환경용입니다.

- ❌ 사용자 인증 없음 (향후 추가)
- ❌ 데이터 암호화 없음 (향후 추가)
- ❌ HTTPS 미지원 (배포 시 필수)
- ✅ CORS 보안 설정
- ✅ 입력 검증

### 프로덕션 배포 필수 사항

1. **HTTPS 적용** - 모든 통신 암호화
2. **인증 시스템** - JWT 토큰 기반 인증
3. **데이터베이스** - 관계형 DB(PostgreSQL) 또는 NoSQL(MongoDB)
4. **개인정보보호** - GDPR/CCPA 준수
5. **접근 제어** - Rate limiting, IP whitelist
6. **감사 로깅** - 모든 활동 기록

---

## 🐛 트러블슈팅

### 문제 1: 포트 5000 이미 사용 중

```bash
# 해결 방법 1: 다른 포트 사용
python -c "from app import app; app.run(port=8080)"

# 해결 방법 2: 기존 프로세스 종료 (Linux/Mac)
lsof -i :5000 | grep LISTEN | awk '{print $2}' | xargs kill -9

# 해결 방법 3: Windows에서 포트 확인
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### 문제 2: CORS 에러

```
Access to XMLHttpRequest at 'http://localhost:5000/api/locations' 
from origin 'http://localhost:3000' has been blocked by CORS policy
```

**해결**: `app.py`에서 CORS가 이미 활성화되어 있습니다. 확인:

```python
from flask_cors import CORS
CORS(app)  # 모든 오리진 허용
```

### 문제 3: 명소 데이터가 로드되지 않음

```bash
# 1. 서버 상태 확인
curl http://localhost:5000/api/health

# 2. 명소 API 직접 호출
curl http://localhost:5000/api/locations

# 3. 브라우저 개발자 도구 (F12) → 네트워크 탭 확인
# Status 200 이면 정상, 500이면 서버 에러
```

### 문제 4: 체크인이 작동하지 않음

```bash
# 직접 API 테스트
curl -X POST http://localhost:5000/api/users/checkin/1 \
  -H "Content-Type: application/json" \
  -d '{"user_id":"user_123"}'
```

---

## 📚 개발자 가이드

### 새로운 명소 추가하기

[app.py](app.py)의 `locations` 리스트에 다음 구조로 추가:

```python
{
    "id": 22,  # 새로운 ID
    "category": "Festival",
    "name": "새로운 축제",
    "english_name": "New Festival",
    "neighborhood": "강화도",
    "description": "한국어 설명",
    "english_description": "English description",
    "detail": "세부 사항",
    "english_detail": "Details",
    "food_tip": "음식 팁",
    "english_tip": "Food tip",
    "transport": "교통편",
    "english_transport": "Transportation",
    "category_tags": ["Festival", "Music"],
    "image": "https://images.unsplash.com/..."
}
```

### 새로운 API 엔드포인트 추가하기

```python
@app.route('/api/new-endpoint', methods=['GET', 'POST'])
def new_endpoint():
    if request.method == 'GET':
        return jsonify({'data': []})
    elif request.method == 'POST':
        data = request.get_json() or {}
        # 처리 로직
        return jsonify({'message': 'success'})
```

### 프론트엔드 JavaScript 수정

[Index.html](Index.html)의 `<script>` 섹션에서:

```javascript
// 1. API 호출 함수 수정
async function fetchLocations() {
    const response = await fetch('/api/locations');
    return response.json();
}

// 2. UI 업데이트 함수 추가
function renderLocations(locations) {
    // HTML 업데이트 로직
}

// 3. 이벤트 리스너 추가
document.getElementById('button-id').addEventListener('click', function() {
    // 클릭 처리
});
```

---

## 🚀 배포 가이드

### 1. Heroku 배포

```bash
# Heroku CLI 설치 후
heroku login
heroku create your-app-name
git push heroku main

# 또는 Procfile 생성 후
echo "web: gunicorn app:app" > Procfile
git push heroku main
```

### 2. GitHub Pages + Netlify Functions

```bash
# Netlify CLI 설치
npm install -g netlify-cli

# 배포
netlify deploy
```

### 3. Docker 배포

```bash
# Dockerfile 생성
cat > Dockerfile << 'EOF'
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
EOF

# 빌드 및 실행
docker build -t closetrip-live .
docker run -p 5000:5000 closetrip-live
```

---

## 📞 문제 신고 및 피드백

### 버그 신고

GitHub Issues를 통해 버그를 신고해주세요:
- 문제 상황 설명
- 재현 단계
- 예상 동작 vs 실제 동작
- 스크린샷/에러 메시지

### 기능 요청

다음 정보를 포함해 요청해주세요:
- 요청 기능 설명
- 사용 사례
- 우선순위

---

## 📄 라이선스

MIT License - 자유롭게 사용, 수정, 배포 가능합니다.

---

## 👥 기여자

- **개발**: BigData Bad (bigdatabad-mcbill)
- **디자인**: CloseTrip Team
- **기획**: 2026 여행 플래너 프로젝트

---

## 📞 연락처

- 📧 Email: bigdatabad-mcbill@github.com
- 🐙 GitHub: https://github.com/bigdatabad-mcbill/2026ktrip
- 💬 Discussions: GitHub Discussions에서 질문해주세요

---

## 🙏 감사의 말

- Unsplash: 고품질 이미지 제공
- Tailwind CSS: 빠른 스타일링
- Flask 커뮤니티: 훌륭한 프레임워크

---

**마지막 업데이트**: 2026년 6월 3일  
**버전**: 1.0 (MVP Phase 2)  
**상태**: 🟢 안정적으로 운영 중
# 의존성 설치
npm install  # 또는 pip install -r requirements.txt

# pre-commit 훅 설치
pre-commit install

# 환경 변수 확인
cp .env.example .env
```

## 4. 보안 정책

- 포트 포워딩: `localhost` 만 허용 (Public 아님)
- 시크릿: `.env` 파일에 저장, Git 에 커밋하지 않음
- `.gitignore` 에 필수 항목 포함:
  ```
  .env
  __pycache__/
  node_modules/
  *.log
  ```

## 5. 비용 최적화

- 유휴 시간: 30 분 (기본값)
- Codespaces 자동 삭제: 7 일 미사용
- Machine type: 프로젝트 필요에 따라 최소 사양 사용

## 6. 팀 협업 규칙

- 브랜치 전략: `main` → `develop` → `feature/*`
- PR 전에 Codespaces 에서 로컬 테스트 필수
- `devcontainer.json` 변경 시 팀원과 공유 후 커밋
```



***

## 2단계: `.devcontainer/devcontainer.json` 생성

리포지토리 루트에 `.devcontainer` 폴더를 만들고 `devcontainer.json` 파일을 생성합니다:

```json
{
  "name": "Optimized Development Environment",
  
  // 기본 이미지 (언어별 선택)
  "image": "mcr.microsoft.com/devcontainers/python:3.11",
  
  // 또는 Dockerfile 사용
  // "build": { "dockerfile": "Dockerfile" },
  
  // 최소 머신 사양 (효율성을 위한 필수 설정)
  "hostRequirements": {
    "cpus": 4,
    "memory": "8gb",
    "storage": "32gb"
  },
  
  // VS Code 설정 (모든 개발자 일관성 확보)
  "settings": {
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.tabSize": 2,
    "files.eol": "\n",
    "terminal.integrated.defaultProfile.linux": "bash",
    "python.defaultInterpreterPath": "/usr/local/bin/python",
    "python.formatting.provider": "black"
  },
  
  // 필수 확장 프로그램 (팀 전체 동일한 환경)
  "extensions": [
    "ms-python.python",
    "ms-python.vscode-pylance",
    "esbenp.prettier-vscode",
    "dbaeumer.vscode-eslint",
    "eamodio.gitlens",
    "ms-vscode.vscode-typescript-next"
  ],
  
  // 포트 포워딩 (보안: localhost 만 허용)
  "forwardPorts": [3000, 8000],
  "portsAttributes": {
    "3000": { "protocol": "http" },
    "8000": { "protocol": "http" }
  },
  
  // 자동 실행 명령어 (온보딩 자동화)
  "postCreateCommand": "pip install -r requirements.txt && pre-commit install",
  
  // 컨테이너 시작 시 실행
  "postStartCommand": "echo 'Welcome to Codespaces!'",
  
  // 사용자 설정
  "remoteUser": "vscode",
  
  // 환경 변수 (선택 사항)
  "containerEnv": {
    "PYTHONUNBUFFERED": "1"
  },
  
  // 볼륨 마운트 (성능 최적화)
  "mounts": [
    "source=/var/run/docker.sock,target=/var/run/docker.sock,type=bind"
  ]
}
```



***

## 3단계: 추가 최적화 파일들

### `.devcontainer/Dockerfile` (커스텀 설정 필요 시)

```dockerfile
FROM mcr.microsoft.com/devcontainers/python:3.11

# 시스템 의존성 설치
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
    curl \
    git \
    build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 도구 설치 (예: uv, poetry)
RUN pip install uv pre-commit black flake8

# 사용자 지정 설정
USER vscode
WORKDIR /home/vscode
```



### `.devcontainer/post-create.sh` (복잡한 설정 자동화)

```bash
#!/bin/bash
echo "🚀 Setting up development environment..."

# 의존성 설치
pip install -r requirements.txt

# pre-commit 훅 설치
pre-commit install

# 환경 변수 복사
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ .env file created"
fi

# VS Code 설정 확인
echo "✅ Development environment ready!"
echo "📝 Run 'pre-commit run --all-files' before committing"
```

`devcontainer.json` 에서 참조:
```json
"postCreateCommand": "./.devcontainer/post-create.sh"
```



***

## 4단계: 적용 방법

### GitHub 에서 적용

1. **리포지토리에 커밋**
   ```bash
   git add .devcontainer/ CODESPACES_POLICY.md
   git commit -m "feat: add Codespaces development policy and config"
   git push origin main
   ```

2. **Codespaces 생성**
   - GitHub 리포지토리 → **Code** 버튼 → **Codespaces** 탭
   - **Create codespace on main** 클릭
   - 또는 딥 링크 사용: `https://github.com/codespaces/new?repo=YOUR_REPO_ID`

3. **환경 자동 설정**
   - Codespaces 가 `devcontainer.json` 을 읽어서 자동으로 환경 구성
   - `postCreateCommand` 가 자동으로 실행됨
   - 확장 프로그램이 자동으로 설치됨

 [docs.github](https://docs.github.com/ko/codespaces/setting-up-your-project-for-codespaces/setting-up-your-repository/facilitating-quick-creation-and-resumption-of-codespaces)

### 조직 정책 적용 (관리자 전용)

조직 레벨에서 Codespaces 정책을 강제할 수 있습니다:

| 정책 | 설정 위치 | 설명 |
|------|----------|------|
| 최대 Codespaces 수 | 조직 설정 → Codespaces | 사용당 최대 Codespaces 개수 제한  [github](https://github.blog/changelog/2023-06-15-maximum-codespaces-per-user-policy/) |
| 머신 타입 제한 | 조직 설정 → Codespaces → Machine types | 2코어/4코어/8코어 등 허용 사양 지정  [github](https://github.blog/changelog/2022-01-10-codespaces-now-offers-organization-policies-to-restrict-machine-types/) |
| 유휴 타임아웃 | 조직 설정 → Codespaces | 자동 종료 시간 (기본 30 분)  [github](https://github.blog/news-insights/product-news/whats-new-in-codespaces-for-organizations/) |
| 포트 가시성 | 조직 설정 → Codespaces | 포트 포워딩 보안 정책  [github](https://github.blog/news-insights/product-news/whats-new-in-codespaces-for-organizations/) |

 [github](https://github.blog/changelog/2023-06-15-maximum-codespaces-per-user-policy/)

***

## 5단계: 효율성 최적화 팁

### 성능 최적화

```json
// devcontainer.json 에 추가
{
  // Docker ignore 파일로 불필요한 파일 제외
  // .dockerignore 생성: node_modules/, __pycache__/, *.log
  
  // 멀티 스테이지 빌드 for 작은 이미지
  // Dockerfile 에서 사용
  
  // 볼륨 캐싱으로 빌드 시간 단축
  "mounts": [
    "source=${env:HOME}/.cache/pip,target=/home/vscode/.cache/pip,type=bind"
  ]
}
```



### 비용 최적화

- **적합한 머신 타입 선택**: `hostRequirements` 로 최소 사양 지정 [docs.github](https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/configuring-dev-containers/setting-a-minimum-specification-for-codespace-machines)
- **자동 종료 설정**: 조직 정책으로 30 분 유휴 시간 적용 [github](https://github.blog/news-insights/product-news/whats-new-in-codespaces-for-organizations/)
- **사용하지 않는 Codespaces 삭제**: GitHub Codespaces 페이지에서 관리

### 팀 일관성 유지

- `devcontainer.json` 을 Git 에 커밋하여 팀원 모두 동일한 환경
- `CODESPACES_POLICY.md` 를 README 에 링크:
  ```markdown
  ## 🚀 개발 환경
  
  [Codespaces 개발 정책 보기](./CODESPACES_POLICY.md)
  
  [
  ```

 [docs.github](https://docs.github.com/ko/codespaces/setting-up-your-project-for-codespaces/setting-up-your-repository/facilitating-quick-creation-and-resumption-of-codespaces)

***

## 요약

| 단계 | 작업 | 파일 |
|------|------|------|
| 1 | 개발 정책 문서화 | `CODESPACES_POLICY.md` |
| 2 | 환경 구성 정의 | `.devcontainer/devcontainer.json` |
| 3 | 커스텀 설정 (선택) | `.devcontainer/Dockerfile`, `post-create.sh` |
| 4 | Git 에 커밋 및 푸시 | - |
| 5 | Codespaces 생성 및 자동 설정 | GitHub UI |

이 구조를 적용하면 **팀 전체가 동일한 개발 환경**에서 작업할 수 있으며, **온보딩 시간이 90% 이상 단축**되고, **로컬 환경 차이로 인한 버그가 제거**됩니다. [medium](https://medium.com/@subhadeep.sen_5940/dev-containers-the-gateway-to-consistent-portable-development-environments-313cab0b0adb)
