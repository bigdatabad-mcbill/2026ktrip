Welcome to the 2026ktrip wiki!
# 다국어 여행 플랫폼 “CloseTrip(클로즈트립)” 서비스 설계 및 실행 명세서

---

## 1. 서비스 개요

### 1.1 서비스 한 줄 정의

실시간 로컬 날씨·무드 분석 기반의 **'장소 맞춤형 스타일링 가이드'** 및 '사진 메타데이터 연동형 자동 여정 기록'을 제공하는 글로벌 타임 크리티컬(Time-Critical) 모바일 여정 관리 솔루션입니다.

### 1.2 핵심 가치

* **Time-Efficiency (시간 효율성):** 첫 진입 3분 이내에 현지 기상 상황 및 사용자 취향을 반영한 맞춤형 코디(TPO)와 포토스폿 동선을 최적화하여 탐색 비용을 파괴합니다.
* **Contextual Relevance (맥락적 신뢰성):** 모호한 추천을 배제하고, 실시간 공공 기상/교통 데이터와 상권 혼잡도 데이터를 연합 연산하여 "왜 이 장소와 의상을 추천하는지" 명확한 인과관계를 설명합니다.
* **Zero-Effort Record (무노력 기록성):** 여행 중 스마트폰 카메라로 사진을 촬영하는 행위만으로 비식별 위치/시간 메타데이터를 파싱하여 개인화된 다이어리를 자동 생성합니다.

### 1.3 사용자 문제 해결

* **관광객의 Pain Point:** "오늘 비가 오고 바람이 부는데 송도 센트럴파크에 어떤 옷을 입고 가야 인생샷을 건질 수 있지? 내 가용 시간 4시간 안에 동선이 꼬이지 않을까?"
* **CloseTrip의 Solution:** 실시간 API로 바람·습도·기온을 결합한 감성 체감 온도를 연산하여 최적의 패션 스펙(OOTB)을 제안하고, 해당 날씨에 가장 채도가 높게 나오는 포토 스폿 동선을 실시간 혼잡도를 우회하여 설계합니다.

---

## 2. 타깃 사용자 정의

| 타깃 세그먼트 | 핵심 니즈 (Needs) | 행동 특성 (Behavioral Traits) |
| --- | --- | --- |
| **국내 주말 여행자** | 실패 없는 단기 여정, 날씨 변수에 따른 실시간 실내/외 대안 장소 신속 탐색 | 주말 오전 급격한 기상 변화 발생 시 앱 진입, 자차 또는 대중교통 기반 동선 위주 소비. |
| **외국인 관광객** | 한정된 체류 시간(Layover 등) 내 초정밀 동선, 다국어 지원, 직관적인 대중교통 연계 | 공항 입국 직후 활성화. 복잡한 텍스트보다 비주얼 아이콘 및 자국어 가이드 의존도 치명적으로 높음. |
| **여행 기록형 사용자** | 사후 기록 작성의 귀찮음 해결, 여정을 아카이빙하여 SNS에 공유하고 싶은 욕구 | 여행 중 사진을 다량 촬영하나 정리는 귀찮아함. 여행 종료 후 자동 푸시 알림을 통해 다이어리 검토 및 발행. |
| **패션/포토 중심 사용자** | 장소 무드와 매칭되는 인스타그래머블(Instagrammable) 포토스폿, 현지 맞춤형 OOTD 매칭 | 특정 필터나 구도 플러그인 요구. 의상 준비를 위해 여행 2~3일 전부터 가상 날씨 시뮬레이션을 적극 활용. |

---

## 3. 핵심 사용자 시나리오

```
[시나리오 1: 첫 실행 사용자 (외국인)]
앱 다운로드 → [온보딩] 언어/국적 선택 (10초) → 취향/스타일 태그 선택 (20초) → 현재 공항 위치 자동 인식 및 날씨·무드 대시보드 진입 (30초 완료)

[시나리오 2: 외국인 관광객 (인천공항 6시간 체류 환승객)]
공항 도착 → 가용 시간 '4시간' 입력 → AI 추천 동선(송도 센트럴파크 코스) 확인 → 추천 사유(실시간 정체 없음, 맑음) 검토 → 대중교통 연계 이동 → 현장 도착 및 추천 구도로 사진 촬영 → 복귀

[시나리오 3: 국내 주말 여행자]
토요일 오전 기상 → 영종도 카페 투어 계획 → 급작스러운 강풍 및 흐림 인지 → 앱 진입 → "흐린 날 뮤트 톤 무드에 어울리는 실내 대형 식물원 카페 코스" 우회 추천 수락 → 출발

[시나리오 4: 여행 기록 사용자]
여행 중 별도 앱 구동 없이 기본 카메라로 스폿별 사진 15장 촬영 → 여행 종료 후 리턴 홈 → "오늘의 영종도 여정이 완성되었습니다" 푸시 수신 → 자동 생성된 타임라인 다이어리 확인 및 1클릭 SNS 공유

```

---

## 4. 화면별 UX 구조 (Information Architecture & Wireframe Spec)

### 4.1 글로벌 통합 정보 구조 (IA)

```
Root
├── 0. Onboarding (Language/Locale Selection -> Preference Taste)
├── 1. Home (실시간 날씨/감성 지수, 통합 대시보드, 퀵 OOTD 추천)
├── 2. Trip (시간 제약 조건형 여정 추천 및 라우팅)
├── 3. Style (날씨 매칭 TPO 코디북 및 패션 룩북 커머스 연계)
├── 4. Spot (날씨·시간대별 실시간 스코어링 인생샷 포토스폿 맵)
├── 5. Diary (사진 메타데이터 파싱 기반 자동 타임라인 기록 시스템)
└── 6. My/Settings (프로필, 언어/단위 전환 및 데이터 권한 관리)

```

### 4.2 하단 탭 구조 (Bottom Navigation Bar)

* `[Home]` - `[Trip]` - `[Style]` - `[Spot]` - `[Diary]` (직관적인 5탭 구성)

---

### 4.3 온보딩 (Onboarding)

* **목적:** 가입 장벽 제거 및 최초 진입 30초 내 언어/문화권 셋팅 및 개인화 벡터 수집.
* **주요 컴포넌트:** 시스템 언어 감지 기반 초기 언어 팝업, 국적/통화 선택 스크롤러, 스타일 취향 매트릭스(칩 선택형).
* **CTA:** `시작하기 / Get Started`
* **빈 상태/에러:** 네트워크 단절 시 오프라인 모드 진입 안내 문구 노출.
* **UX 문구 예시:**
* **KO:** "반가워요! 당신의 언어와 선호하는 여행 스타일을 알려주세요." (버튼: `분석 시작`)
* **EN:** "Welcome! Please select your language and preferred travel style." (Button: `Start Analysis`)



---

### 4.4 홈 (Home)

* **목적:** 현재 위치 기상/정체 환경 가시화 및 오늘의 요약 가치 전달.
* **주요 컴포넌트:** 실시간 체감 기온 및 '장소 무드 인덱스' 비주얼 그래픽 카드, 상단 실시간 추천 이유 위젯, 알림 벨.
* **CTA:** `추천 코디 보러가기`, `내 주변 스폿 탐색`
* **빈 상태/에러 문구:** 위치 권한 거부 시 `위치 정보를 불러올 수 없어 기본 설정인 '서울' 기준으로 노출됩니다.` / `Location services disabled. Showing default 'Seoul'.`
* **UX 문구 예시:**
* **KO:** "현재 송도는 강한 바람과 함께 흐림 무드(지수 45%). 차분한 베이지 톤 트렌치코트를 추천합니다."
* **EN:** "Songdo is currently windy & cloudy (Mood Index 45%). A calm beige trench coat is highly recommended today."



---

### 4.5 Trip (여정 탐색)

* **목적:** 가용 시간(Time Budget) 내 최적의 이동 동선 모델 제공.
* **주요 컴포넌트:** 시간 슬롯 입력 바(Slider), 타임라인형 이동 경로 카드(교통 수단별 소요 시간 표시), 실시간 우회 대안 스위치.
* **CTA:** `이 경로로 안내 시작 / Start Route`
* **UX 문구 예시:**
* **KO:** "환승 대기 시간 5시간에 최적화된 안전 보장 동선입니다. (공항 복귀 마진 90분 반영 완료)"
* **EN:** "Optimized safe route for your 5-hour layover. (90-min airport return buffer included)"



---

### 4.6 Style (TPO 코디)

* **목적:** 기상 수치에 따른 최적의 룩(Look) 제안 및 이커머스 연동.
* **주요 컴포넌트:** 매칭 의상 스튜디오 그리드 뷰, 원단 두께/방풍 기능성 체크 뱃지, 제휴 브랜드 원클릭 구매 연계 링크.
* **CTA:** `이 스타일 저장 / 무드 매칭 상품 보기`
* **UX 문구 예시:**
* **KO:** "습도 80%의 후텁지근한 날씨입니다. 통기성이 좋은 린넨 셔츠가 쾌적함을 유지해 줍니다."
* **EN:** "Humid conditions (80%). Breathable linen shirts will keep you comfortable throughout the journey."



---

### 4.7 Spot (포토스폿 맵)

* **목적:** 현재 날씨 조건에서 가장 인스타그래머블한 사진 촬영 스폿 밀집도 제공.
* **주요 컴포넌트:** 고정밀 맵(Map) 인터페이스, 스폿별 '실시간 촬영 만족도 스코어' 마커, 추천 촬영 각도 가이드 오버레이.
* **CTA:** `내비게이션 연동 / 구도 가이드 확인`
* **UX 문구 예시:**
* **KO:** "현재 흐린 조도에서는 3번 스폿의 붉은 벽돌 배경이 인물의 대비를 가장 선명하게 살려줍니다."
* **EN:** "Under cloudy skies, the red brick background at Spot 3 delivers the sharpest contrast for portraits."



---

### 4.8 Diary (자동 여정 다이어리)

* **목적:** 사용자의 수동 입력 비용 제로화. 백라운드 사진 동기화 기반 아카이빙.
* **주요 컴포넌트:** 일자별 자동 생성 타임라인 뷰, 날씨 스탬프 이미지, AI 자동 생성 요약 저널 텍스트 박스, 편집/공유 컴포넌트.
* **빈 상태 (Empty State):** "아직 기록된 사진이 없습니다. 여행 중 평소처럼 사진을 촬영하시면 자동으로 기록이 시작됩니다." / "No photos captured yet. Just take photos with your default camera, and your diary will build itself."
* **UX 문구 예시:**
* **KO:** "2026년 6월 3일, 촉촉한 빗속의 송도 센트럴파크에서 시작된 당신의 감성 여정입니다."
* **EN:** "June 3, 2026. Your emotional journey standard-built at rainy Songdo Central Park."



---

## 5. 다국어 / 현지화(Localization) 정책

### 5.1 언어 우선순위 및 자동 전환 엔진

* **감지 매커니즘:** 시스템 OS 기본 언어를 1순위 감지하되, IP 주소 기반 지오펜싱(Geo-fencing)을 매칭하여 최초 실행 시 스플래시 화면 하단에 `[한국어 / English / 日本語 / 简体中文 / 繁體中文 / Tiếng Việt / ภาษาไทย]` 빠른 선택 시트(Action Sheet)를 강제 플로팅하여 셋팅 오류를 방지합니다.

### 5.2 단위(Unit) 및 포맷 표준화 아키텍처

| 구분 | 아시아 (KO/VN/TH 등) | 북미/유럽 권역 (EN) | 비고 |
| --- | --- | --- | --- |
| **날짜 표기** | `YYYY. MM. DD` (예: 2026. 06. 03) | `MMM DD, YYYY` (예: Jun 3, 2026) | 로케일 포맷터 분기 처리 |
| **시간 표기** | 24시간제 (예: 14:30) | 12시간제 + AM/PM (예: 2:30 PM) | 사용자 가독성 우선 |
| **온도 단위** | 섭씨 ($^\circ\text{C}$) | 화씨 ($^\circ\text{F}$) | EN 로케일 시 화씨 기본 매핑 |
| **거리 단위** | 미터법 ($\text{km}$, $\text{m}$) | 야드파운드법 ($\text{mi}$, $\text{ft}$) | 내비게이션 연동 시 필수 전환 |
| **통화 표기** | 원화 ($\backslash$, KRW) | 달러 ($\$$, USD) | 실시간 역산 고정 환율 API 적용 |

### 5.3 문화적 표현 차이 및 UI 레이아웃 정책 (LTR / RTL)

* **텍스트 확장 리스크 대응 (Text Expansion Factor):** 영문이나 베트남어 변환 시 한국어 대비 문자열 길이가 최대 35% 늘어나는 현상을 방지하기 위해 UI 컴포넌트의 가로 폭을 고정하지 않고 `flex-wrap` 및 고정 글자 크기 대신 가변형 `rem/em` 단위를 기본 설계합니다.
* **RTL(Right-to-Left) 아키텍처 확장성:** 향후 아랍권 확장을 고려하여 모든 컨테이너 레이아웃은 안드로이드 `ConstraintLayout`의 `start/end` 제약 조건 및 iOS의 `leading/trailing` 속성을 철저히 준수하여 코딩합니다.

---

## 6. 기술 아키텍처 (Technical Architecture Specifications)

### 6.1 하이브리드 앱 및 서버 아키텍처 구성

```
[Client App] React Native (Expo) - iOS/Android Single Codebase
   │
   ├──▶ [API Gateway] AWS API Gateway (라우팅, 속도 제한, JWT 검증)
         │
         ├──▶ [Compute Engine] AWS ECS Fargate (Node.js Express TypeScript)
         │     │
         │     ├──▶ [Database] AWS RDS PostgreSQL (PostGIS 공간 인덱스 탑재)
         │     ├──▶ [Cache Memory] AWS ElastiCache Redis (날씨 데이터, 유저 세션 캐싱)
         │     │
         │     └──▶ [Inference Model] Rule-Based Scheduler Engine ◀── [공공 API 연동]

```

### 6.2 데이터베이스 스키마 설계 (핵심 테이블 구조)

```sql
-- 1. 사용자 프로필 및 글로벌 로케일 마스터 테이블
CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    preferred_language VARCHAR(10) DEFAULT 'en',
    temperature_unit VARCHAR(5) DEFAULT 'C',
    distance_unit VARCHAR(5) DEFAULT 'km',
    style_preference VARCHAR(50)[], -- ['casual', 'minimal', 'street']
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. 사진 메타데이터 연동 다이어리 테이블 (PostGIS 활용 위치 기반)
CREATE TABLE automatic_diaries (
    diary_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    captured_at TIMESTAMP NOT NULL,
    geo_location GEOMETRY(Point, 4326), -- 정밀 위경도 매핑 공간 인덱스
    resolved_address_ko TEXT,
    resolved_address_en TEXT,
    weather_temperature NUMERIC(4,1),
    weather_condition VARCHAR(50),
    ai_summary_text TEXT,
    image_s3_url TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_diary_geo ON automatic_diaries USING gist(geo_location);

```

### 6.3 인과관계 설명 가능형 추천 및 자동 다이어리 생성 파이프라인

* **설명 가능성(XAI) 구현:** 무조건적인 추천 대신 파이썬 스케줄러 엔진에서 필터링된 기상 조건 매트릭스를 JSON 프롬프트 구조에 태워 LLM에 컨텍스트로 제공합니다.

```json
{
  "context": {
    "weather": {"temp_c": 14.5, "wind_speed_ms": 7.8, "rain_prob_pct": 10},
    "location": "Incheon Songdo Central Park",
    "selected_poi": "G-Tower Observatory"
  },
  "prompt_injection": "Generate a 2-sentence recommendation summary explaining that because the wind speed is high at 7.8m/s, an indoor observatory (G-Tower) is recommended over the windy outdoor park, matching with a windbreaker jacket style."
}

```

### 6.4 외부 오픈 API 장애 극복 전략 (Fault-Tolerance / Fallback Design)

* **날짜/기상 API 장애 시:** 기상청 대용량 API 장애 발생 우려 시 `Circuit Breaker` 패턴을 구성합니다. 3회 이상 타임아웃 발생 시 즉시 서드파티 글로벌 날씨 서비스(OpenWeatherMap API)로 트래픽을 자동 페일오버(Failover) 조치하며, 이마저도 유실될 경우 최악의 상태에서는 Redis 캐시에 저장된 최신 3시간 이내의 직전 과거 데이터를 `[3시간 전 관측 기준 정보]` 뱃지와 함께 하드코딩 노출하여 앱 크래시를 전면 방어합니다.
* **역지오코딩(Reverse Geocoding) 장애 시:** 사진 업로드 시 주소 변환 API(Google Maps / Kakao API)가 작동하지 않는 경우, 텍스트 주소 칸을 비우는 대신 사진의 EXIF 내 GPS 좌표값 자체(`Lat: 37.391, Lng: 126.634`)를 기재하고 사용자에게 `[오프라인 상태 - 위치 편집 가능]` UI를 동적 활성화합니다.

---

## 7. MVP 범위와 고도화 범위 (Scope & Priority)

### 7.1 구현 우선순위 및 로드맵 매트릭스

| 기능 분류 | 구현 항목 (Feature Name) | 우선순위 | 기술적 구현 스펙 및 이유 |
| --- | --- | --- | --- |
| **MVP 범위** | 언어 및 로케일 최초 수동/자동 전환 환경 | **P0 (필수)** | 가입 이탈 방지용 핵심 UX. 다국어 마스터 상수셋 연동. |
| **MVP 범위** | 룰 기반 기온별 OOTD 매칭 시스템 | **P0 (필수)** | AI 환상 배제. 기상청 온도 구간 격차별 8종 의상 매칭 Rule-Engine 구현. |
| **MVP 범위** | 사진 EXIF 메타데이터 파싱 및 타임라인 자동 나열 | **P0 (필수)** | 핵심 가치인 '무노력 기록' 증명을 위해 Client-side 단독 파싱 구현. |
| **MVP 범위** | Google/Kakao 기본 지도 연동 및 포토스폿 마킹 | **P1 (우선)** | 포토스폿 좌표 시각화를 위한 코어 모듈. |
| **고도화 범위** | 사용자 실시간 사진 스타일 딥러닝 기반 맞춤형 의상 피드 추천 | **P2 (보통)** | MVP 검증 후 진행. 개인화 협업 필터링 알고리즘 탑재 필요. 연산 비용 큼. |
| **고도화 범위** | LLM 연동 완전 자동 다이어리 저널 에세이 에디팅 생성기 | **P3 (낮음)** | API 비용 통제 및 할루시네이션 위험 통제를 위해 2차 론칭으로 격하. |

---

## 8. 비즈니스 모델 (Business & Monetization Model)

### 8.1 4대 수익화 스트림 및 결합 전략

1. **패션 이커머스 제휴 크로스 셀링 (Main BM):** 당일 날씨에 맞는 추천 룩북 카드 하단에 지그재그, 무신사, 파페치 등 글로벌 커머스 플랫폼의 유사 상품 구매 API 링크를 연계하여 구매 전환 매출의 **3~7% 수수료 분할(Revenue Share)** 모델을 취합니다.
2. **지역 소상공인 쿠폰 기반 B2G/B2B 광고:** 특정 날씨(예: 폭우)로 인해 실외 코스가 취소될 때, 인근 제휴 실내 카페나 복합문화공간의 할인 쿠폰을 컨텍스트 푸시로 발행하여 주변 상권 인입당 과금(CPA)을 실현합니다.
3. **프리미엄 구독형 오프라인 패키지:** 무제한 AI 다이어리 고화질 백업, 제휴 인생샷 스튜디오 무료 인화권, 오프라인 로컬 가이드 맵 다운로드 권한을 묶어 월 구독 모델 ($2.99/mo)을 운영합니다.

### 8.2 사용자 UX 가치와 수익화 충돌 방지 가이드라인

* **원칙:** 광고성 장소를 상단에 노출하기 위해 날씨 무드 매칭 추천 점수 알고리즘 조작을 절대 엄금합니다. 광고 제휴 스폿은 평점 순위 스코어 카드가 아닌, 오직 독립된 영역인 `[인근 제휴 혜택 장소]` 가이드 배너 형태로 분리 표기하여 유저 신뢰도의 손상을 전면 방어합니다.

---

## 9. 론칭 로드맵 (Go-To-Market Roadmap)

### 9.1 0단계: 사전 검증 (Pre-launch)

* **목적 및 행동:** Figma 프로토타입 기반 글로벌 인바운드 외국인 대상 길거리 사용성 테스트(UT) 수행.
* **KPI:** 온보딩 단계 가입 포기율 $5\%$ 이하 타깃.
* **진입 조건:** 핵심 유저 시나리오의 사용 수락률 $80\%$ 달성 시 개발 착수.

### 9.2 1단계: MVP 출시 및 로컬 검증 (Incheon Sandbox Launch)

* **목적 및 행동:** 영종·송도 관광 특구를 거점으로 국문/영문 알파 버전 스토어 론칭. 공공데이터 연합 엔진 안정성 확보.


* **KPI:** 주간 활성 사용자 수(WAU) 2,000명, 사진 권한 획득 승인율 $85\%$ 이상 확보.
* **진입 조건:** 기상 매칭 데이터 로딩 레이턴시 $1.5$초 이하 안정화 완료 시 다음 단계 진입.

### 9.3 2단계: 다국어 고도화 및 전국 확장 (Global Expansion)

* **목적 및 행동:** 일본어, 중국어, 태국어, 베트남어 다국어 로케일을 완전 탑재하고 서울, 제주, 부산 등 메이저 거점 도시 공간 인덱스 데이터 허브 구축.
* **KPI:** 외국인 사용자 비율 전체의 $40\%$ 달성, 앱스토어 평점 4.5 이상 유지.
* **진입 조건:** 글로벌 유저의 7일 차 리텐션(Retention Rate) $25\%$ 이상 증명 시 커머스 제휴 기능 전면 롤아웃.
