# Step 6: 컨테이너화 (Dockerfile)
# Base Image: python:3.9-slim
FROM python:3.9-slim

# 작업 디렉토리 /app 설정
WORKDIR /app

# 의존성 설치 (pip install -r requirements.txt)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 파일 복사
COPY . .

# 서버 실행 명령어 지정 (uvicorn main:app --host 0.0.0.0 --port 80)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
