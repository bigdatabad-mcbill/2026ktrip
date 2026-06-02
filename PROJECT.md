# CloseTrip MVP 개발 프로젝트 수행 문서 (Code Space 기준)

## 1. 프로젝트 개요

**CloseTrip**은 사용자의 근거리 여행/출퇴경 경험을 맞춤형으로 추천하고 다이어리 형태로 기록할 수 있는 모바일 웹/앱 서비스입니다. MVP 단계에서는 **추천 정확도보다 핵심 행동 유도가 우선**이며, 다음 5가지 흐름이 연결되는지를 추적하는 지표 체계가 핵심입니다 [countly]:

1. 온보딩 완료
2. 첫 가치 경험 (First Value Experience)
3. 재방문
4. 저장/공유
5. 다이어리 생성

***

## 2. MVP 목표 및 성공 지표

### 2.1 핵심 목표

> **“핵심 행동이 실제로 일어났는지”를 측정할 수 있는 지표 체계를 구축**

### 2.2 주요 성과 지표 (KPIs)

| 순위 | 지표 | 정의 | 목표치 (MVP 1개월) |
|------|------|------|-------------------|
| 1 | 온보딩 완료율 | 회원가입 + 위치 허용 + 첫 관심지 정하기까지 완료 비율 | ≥ 60% |
| 2 | 첫 가치 경험률 | 온보딩 후 24시간 내 “추천 장소 클릭 → 방문 기록 또는 저장” 발생 비율 | ≥ 40% |
| 3 | 7일 재방문율 | 첫 방문 후 7일 내 다시 앱/웹 접근 비율 | ≥ 25% |
| 4 | 저장/공유율 | 장소 저장 또는 SNS 공유 발생 비율 | ≥ 20% |
| 5 | 다이어리 생성율 | 최소 1개 이상 다이어리 작성 완료 비율 | ≥ 15% |

이 지표들은 Countly를 통해 추적하며, 각 이벤트는 이후 분석과 A/B 테스트의 기초가 됩니다 [countly].

***

## 3. 기술 스택 및 Code Space 환경

### 3.1 개발 환경

- **IDE**: GitHub Code Space (Cloud-based VS Code)
- **프론트엔드**: React + TypeScript + Vite
- **백엔드**: Node.js (Express) 또는 Next.js (API Routes)
- **데이터베이스**: PostgreSQL (Supabase 또는 Neon)
- **인증**: Supabase Auth 또는 NextAuth
- **위치 기반**: Google Maps API 또는 Naver Map API (Seoul 기준)
- **애너널리틱스**: Countly (자사 호스팅 또는 클라우드)
- **배포**: Vercel (프론트엔드), Render/ Railway (백엔드)

### 3.2 Code Space 설정

`.devcontainer/devcontainer.json`:

```json
{
  "name": "CloseTrip MVP",
  "image": "mcr.microsoft.com/devcontainers/javascript-node:1-20",
  "extensions": [
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode",
    "ms-vscode.vscode-typescript-next"
  ],
  "forwardPorts": [3000, 5000],
  "postCreateCommand": "npm install && cd server && npm install",
  "settings": {
    "editor.formatOnSave": true
  }
}
```

***

## 4. 핵심 기능 범위 (MVP)

### 4.1 필수 기능

| 기능 | 설명 | 연결 지표 |
|------|------|----------|
| 온보딩 워크플로우 | 회원가입 → 위치 허용 → 관심 지역/취향 선택 | 온보딩 완료율 |
| 근거리 추천 목록 | 현재 위치 기반 3~5개 장소 추천 (Seoul 기준 3km 이내) | 첫 가치 경험률 |
| 장소 상세 + 저장/공유 | 장소 정보, 저장 버튼, SNS 공유 | 저장/공유율 |
| 방문 기록 + 다이어리 생성 | 방문 후 간단한 사진/글 작성 | 다이어리 생성율 |
| 리터너션 푸시/알림 | 3일/7일 후 “새로운 근처 장소” 알림 | 재방문율 |

### 4.2 제외 기능 (MVP 이후)

- 복잡한 필터링 (가격대, 테마별 등)
- المجتمات/커뮤니티 기능
- 프리미엄 구독 모델
- AI 기반 개인화 추천 (초기 규칙 기반 추천으로 대체)

***

## 5. 이벤트 추적 체계 (Countly 기반)

### 5.1 추적할 이벤트 목록

```js
// Пример envent tracking with Countly
const events = {
  ONBOARDING_START: 'onboarding_start',
  ONBOARDING_COMPLETE: 'onboarding_complete',
  LOCATION_ALLOWED: 'location_allowed',
  INTEREST_SELECTED: 'interest_selected',

  FIRST_VALUE_EXPERIENCE: 'first_value_experience', // 추천 장소 클릭 → 저장/방문 기록
  REVISIT_7D: 'revisit_7d',

  PLACE_SAVE: 'place_save',
  PLACE_SHARE: 'place_share',

  DIARY_CREATE_START: 'diary_create_start',
  DIARY_CREATE_COMPLETE: 'diary_create_complete'
};
```

### 5.2 Countly 설정 예시

```bash
npm install countly-sdk-web
```

```js
// src/analytics/countly.ts
import Countly from 'countly-sdk-web';

Countly.init({
  app_key: 'YOUR_APP_KEY',
  url: 'https://countly.yourdomain.com',
  device_id: 'USER_DEVICE_ID' // auth 후 설정
});

export const trackEvent = (key, segmentation = {}) => {
  Countly.recordEvent(key, segmentation);
};
```

각 핵심 이벤트는 `segmentation`에 `user_id`, `location`, `device_type` 등을 포함합니다 [countly].

***

## 6. 프로젝트 구조

```
clopsetrip-mvp/
├── .devcontainer/
│   └── devcontainer.json
├── client/                 # React + Vite
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   │   ├── Onboarding.tsx
│   │   │   ├── Home.tsx
│   │   │   ├── PlaceDetail.tsx
│   │   │   └── Diary.tsx
│   │   ├── analytics/
│   │   │   └── countly.ts
│   │   ├── App.tsx
│   │   └── main.tsx
│   └── package.json
├── server/                 # Express or Next.js API
│   ├── routes/
│   │   ├── auth.ts
│   │   ├── places.ts
│   │   └── diaries.ts
│   ├── controllers/
│   ├── models/
│   └── package.json
├── shared/
│   └── types.ts
├── README.md
└── .env.example
```

***

## 7. 개발 마일스톤 (4주 기준)

| 주차 | 목표 | délivrables |
|------|------|------------|
| 1 | Code Space 환경 세팅 + 온보딩 흐름 구현 | 온보딩 완료, Countly 연동, 이벤트 추적 |
| 2 | 근거리 추천 + 장소 상세 + 저장/공유 | 첫 가치 경험 추적, 저장/공유 이벤트 |
| 3 | 다이어리 생성 + 방문 기록 | 다이어리 생성 이벤트, DB 스키마 완성 |
| 4 | 리터션 흐름 + 지표 대시보드 | 7일 재방문 추적, Countly 대시보드 확인 |

***

## 8. 성공 측정 및Iteration

1. **주간 리뷰**: 각 KPI 실제 수치 확인 (Countly 대시보드)
2. **가설 검증**:  
   - “온보딩 단계를 3단으로 줄이면 완료율 ↑?”  
   - “첫 추천을 3개 → 5개로 늘리면 첫 가치 경험률 ↑?”
3. **A/B 테스트**: 온보딩 흐름, 추천 카드 디자인, 알림 문구 등
4. **피드백 루프**: 사용자 인터뷰 + 이벤트 유출 지점 분석

***

## 9. 참고 자료

- Countly 이벤트 추적 가이드 및 지표 설계 원칙 [countly]
- GitHub Code Space 문서: https://docs.github.com/en/codespaces
- Next.js + TypeScript 스타터: https://nextjs.org/docs

***

이 문서를 Code Space에서 프로젝트 초기화 시 `README.md` 또는 `PROJECT.md`로 저장하고, 개발 팀과 공유하여 MVP 개발 방향을 제시하세요.
