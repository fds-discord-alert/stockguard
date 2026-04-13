# 🚀 StockGuard: 실시간 주식 이상 거래 탐지 (FDS) 백엔드

주식 시장에서 발생하는 거래 데이터를 실시간으로 분석하고, **10억 원 초과 고액 거래**, **해외 접속**, **단시간 반복 거래(Velocity Check)** 등 이상 징후를 탐지하여 대응하는 클라우드 네이티브 기반 백엔드 애플리케이션입니다.

---

## 🛠️ 주요 탐지 룰
1.  **고액 거래 탐지**: 10억 원 초과 거래 시 즉각 차단
2.  **해외 접속 탐지**: 한국 이외 지역에서의 접속 시 즉각 차단
3.  **단시간 반복 거래 탐지**: **1초 이내**에 동일한 사용자가 3번 이상 거래 시 즉각 차단 (Redis 기반)

---

## 🧪 로컬 테스트 가이드

### 📋 사전 준비
- Python 3.9 이상 설치
- **Redis (Velocity Check용)**: Docker를 이용해 실행하거나 로컬에 설치되어 있어야 합니다.
- `curl` 도구 (대부분의 OS에 기본 설치됨)

---

### 🚀 1단계: 환경 구축 및 의존성 설치

제공된 `setup.sh` 파일을 실행하여 가상환경 구축 및 **Redis 컨테이너**를 실행합니다.

```bash
# 스크립트에 실행 권한 부여 (필요 시)
chmod +x setup.sh

# 환경 구축 및 Redis 실행
./setup.sh

# 가상환경 활성화
source .venv/bin/activate
```

---

### 🏃 2단계: FastAPI 서버 실행

서버를 실행하여 API 요청을 받을 준비를 합니다.

```bash
# uvicorn을 사용하여 서버 실행 (포트 8000번 사용)
python main.py
```

---

### 🔍 3단계: 기능 테스트 (API 호출)

모든 테스트는 로컬 개발 서버의 기본 포트인 **8000번**을 기준으로 진행합니다.

#### 1. 이상 거래: 10억 초과 고액 거래 (Blocked)
```bash
curl -X POST http://localhost:8000/trade \
     -H "Content-Type: application/json" \
     -d '{
       "user_id": "whale_user",
       "amount": 1500000000,
       "timestamp": "10:30",
       "location": "Korea",
       "stock_name": "Samsung Electronics"
     }'
```

#### 2. 이상 거래: 단시간 반복 거래 (Velocity Check)
**1초 이내**에 동일한 `user_id`로 **3번** 이상 요청을 보내면 탐지됩니다.

```bash
# 이 명령어를 1초 안에 아주 빠르게 3번 실행
curl -X POST http://localhost:8000/trade \
     -H "Content-Type: application/json" \
     -d '{
       "user_id": "fast_user",
       "amount": 10000,
       "timestamp": "15:00",
       "location": "Korea",
       "stock_name": "Nvidia"
     }'
```

---

## 🐳 4단계: Docker 컨테이너 빌드 및 실행

Docker 환경에서도 호스트의 **8000번 포트**를 통해 접속하도록 설정하는 것이 가장 안전합니다.

### 1. 이미지 빌드
```bash
docker build -t fds-backend .
```

### 2. 실행 (로컬 Redis와 연결 시)
- **Linux/Docker Desktop**: `host.docker.internal`을 사용해 호스트의 Redis에 접속합니다.
```bash
docker run -d -p 8000:80 \
  --name fds-app \
  -e REDIS_HOST=host.docker.internal \
  fds-backend
```

### 3. Docker Compose 사용 (권장)
앱과 Redis를 한 번에 실행하고 연동합니다.
```bash
# 실행
docker-compose up -d

# 테스트 (여전히 8000번 포트로 접속 가능)
curl -X GET http://localhost:8000/health
```

---

## 🔔 5단계: Discord 알림 (담당 팀원 구현 중)
`services/discord_bot.py`는 현재 빈 함수 상태이며, 구현이 완료되면 실시간 알림을 받을 수 있습니다.
