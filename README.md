# 2026ktrip

GitHub Codespaces 에서 **최적의 효율로 개발하기 위한 정책**을 Markdown 파일로 만들고 적용하는 방법을 단계별로 알려드립니다.

## 핵심 요약

개발 정책은 **두 가지 파일**로 구성합니다:
1. **`CODESPACES_POLICY.md`** (또는 `README.md`) - 팀이 따라야 할 개발 표준과 가이드라인을 문서화
2. **`.devcontainer/devcontainer.json`** - Codespaces 환경을 자동으로 설정하는 구성 파일

***

## 1단계: 개발 정책 Markdown 파일 만들기

리포지토리 루트에 `CODESPACES_POLICY.md` (또기 `DEVELOPMENT_POLICY.md`) 파일을 생성합니다:

```markdown
# GitHub Codespaces 개발 정책

## 1. 개발 환경 표준

### 필수 도구
- Python 3.11+ 또는 Node.js 18+
- Docker Desktop
- VS Code 확장: Prettier, ESLint, GitLens

### 코딩 스타일
-(indentation: 2 spaces (JavaScript/TypeScript), 4 spaces (Python)
- 라인 길이: 100 characters
- 자동 포맷팅 필수: `pre-commit` 훅 사용

## 2. Codespaces 설정 기준

### 최소 사양
| 프로젝트 유형 | CPU | 메모리 | 저장소 |
|--------------|-----|--------|--------|
| 웹 프론트엔드 | 2코어 | 4GB | 32GB |
| 백엔드/API | 4코어 | 8GB | 32GB |
| 머신러닝/데이터 | 8코어 | 16GB | 64GB |

### 권장 확장 프로그램
- Python (ms-python.python)
- Prettier (esbenp.prettier-vscode)
- ESLint (dbaeumer.vscode-eslint)
- GitLens (eamodio.gitlens)

## 3. 자동화 설정

### postCreateCommand 실행 항목
```bash
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
