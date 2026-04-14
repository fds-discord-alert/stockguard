# 🚀 StockGuard: 실시간 주식 이상 거래 탐지 (FDS) 백엔드

주식 시장에서 발생하는 거래 데이터를 실시간으로 분석하고, **10억 원 초과 고액 거래**, **실제 IP 기반 해외 접속**, **단시간 반복 거래(Velocity Check)** 등 이상 징후를 탐지하여 대응하는 클라우드 네이티브 기반 백엔드 애플리케이션입니다.

---

## 🛠️ 주요 탐지 룰 (고도화 완료)

1. **고액 거래 탐지**: 1,000,000,000 KRW 초과 거래 시 즉각 차단 (심각도: CRITICAL)
2. **IP 기반 해외 접속 탐지**: `ip-api.com`을 연동하여 실제 IP의 국가를 조회, 한국 이외 지역일 경우 차단 (심각도: HIGH)
3. **단시간 반복 거래 탐지**: **1초 이내**에 동일한 사용자가 3번 이상 거래 시 즉각 차단 (심각도: WARNING)

---

## 🧪 로컬 테스트 가이드

### 📋 사전 준비

- Python 3.9 이상 설치
- **Redis (Velocity Check용)**: `setup.sh` 실행 시 Docker를 통해 자동으로 시작됩니다.
- **Discord Webhook**: 알림 수신을 위해 필요합니다.
- `curl` 도구

---

### 🚀 1단계: 환경 구축 및 설정

1. **환경 구축 및 Redis 실행**:

   ```bash
   chmod +x setup.sh
   ./setup.sh
   source .venv/bin/activate
   ```
2. **환경변수 설정 (`.env`)**:
   프로젝트 루트 디렉토리에 `.env` 파일을 생성하고 아래와 같이 본인의 디스코드 웹후크 URL을 입력합니다. (이 파일은 `docker compose` 실행 시 자동으로 컨테이너에 전달됩니다.)

   ```bash
   echo "webhook_url=https://discord.com/api/webhooks/..." > .env
   ```

---

### 🏃 2단계: FastAPI 서버 실행

```bash
# uvicorn을 사용하여 서버 실행 (기본 8000번 포트)
python main.py
```

---

### 🔍 3단계: 기능 테스트 (API 호출)

모든 테스트는 로컬 개발 서버의 기본 포트인 **8000번**을 기준으로 진행합니다.

#### 1. 헬스 체크 (Health Check)

```bash
curl -X GET http://localhost:8000/health
```

#### 2. 정상 거래 테스트 (Approved)

```bash
curl -X POST http://localhost:8000/trade \
     -H "Content-Type: application/json" \
     -d '{
       "user_id": "user123",
       "amount": 100000,
       "timestamp": "14:30",
       "location": "127.0.0.1",
       "stock_name": "Samsung Electronics"
     }'
```

#### 3. 이상 거래: 10억 초과 고액 거래 (Blocked)

```bash
curl -X POST http://localhost:8000/trade \
     -H "Content-Type: application/json" \
     -d '{
       "user_id": "whale_user",
       "amount": 1500000000,
       "timestamp": "10:30",
       "location": "127.0.0.1",
       "stock_name": "Samsung Electronics"
     }'
```

#### 4. 이상 거래: 해외 IP 접속 테스트 (실제 IP 조회)

`location` 필드에 실제 해외 IP(예: 8.8.8.8 - 미국)를 넣어 국가 조회 로직을 테스트합니다.

```bash
curl -X POST http://localhost:8000/trade \
     -H "Content-Type: application/json" \
     -d '{
       "user_id": "user_abroad",
       "amount": 50000,
       "timestamp": "10:00",
       "location": "8.8.8.8",
       "stock_name": "Tesla"
     }'
```

#### 5. 이상 거래: 단시간 반복 거래 (Velocity Check)

**1초 이내**에 동일한 `user_id`로 **3번** 이상 요청을 보내면 탐지됩니다. (1초 안에 빠르게 실행해 보세요.)

```bash
curl -X POST http://localhost:8000/trade \
     -H "Content-Type: application/json" \
     -d '{
       "user_id": "fast_user",
       "amount": 1000,
       "timestamp": "15:00",
       "location": "127.0.0.1",
       "stock_name": "Nvidia"
     }'
```

---

## 🐳 4단계: Docker 컨테이너 실행

### 1. 이미지 빌드

```bash
docker build -t fds-backend .
```

### 2. 단일 컨테이너 실행 (환경변수 수동 지정)

```bash
docker run -d -p 8000:80 \
  --name fds-app \
  --env-file .env \
  -e REDIS_HOST=host.docker.internal \
  fds-backend
```

### 3. Docker Compose 사용 (권장)

```bash
# 실행
docker compose up -d

# 로그 확인 (알림 전송 과정 확인 가능)
docker compose logs -f app

# 중지 및 제거
docker compose down
```

---

## 🔔 5단계: Discord 알림 (Embed 적용)

팀원의 로직 통합으로 단순 텍스트가 아닌 **상세 임베드(Embed) 메시지**가 전송됩니다.

- **심각도별 색상**: 빨강(Critical), 노랑(Warning), 파랑(High)으로 자동 구분.
- **디버깅 로그**: 서버 터미널에서 알림 전송 시도 성공/실패 여부를 실시간으로 확인할 수 있습니다.
